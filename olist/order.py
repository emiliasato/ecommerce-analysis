import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist
from datetime import timedelta
from functools import reduce


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified otherwise
        """
        orders = self.data['orders']
        #filter on delivered orders
        if is_delivered:
            delivered = orders[orders['order_status']=='delivered'].copy()
        #parsing string to datetime
        delivered['order_purchase_timestamp'] = pd.to_datetime(delivered['order_purchase_timestamp'])
        delivered['order_approved_at'] = pd.to_datetime(delivered['order_approved_at'])
        delivered['order_delivered_carrier_date'] = pd.to_datetime(delivered['order_delivered_carrier_date'])
        delivered['order_delivered_customer_date'] = pd.to_datetime(delivered['order_delivered_customer_date'])
        delivered['order_estimated_delivery_date'] = pd.to_datetime(delivered['order_estimated_delivery_date'])
        #getting wait_time (# of days between order_purchase_timestamp and order_delivered_customer_date)
        delivered['wait_time'] = (delivered['order_delivered_customer_date'] - delivered['order_purchase_timestamp'])/ np.timedelta64(1, 'D')
        #getting expected wait time (the number of days between order_purchase_timestamp and estimated_delivery_date)
        delivered['expected_wait_time'] = (delivered['order_estimated_delivery_date']- delivered['order_purchase_timestamp'])/ np.timedelta64(1, 'D')
        #getting delay_vs_expected
        #if the actual order_delivered_customer_date is later than the estimated delivery date,
        #returns the number of days between the two dates, otherwise return 0
        delivered['delay_vs_expected'] = (delivered['order_delivered_customer_date'] - delivered['order_estimated_delivery_date'])/ np.timedelta64(1, 'D')
        delivered['delay_vs_expected'] = delivered['delay_vs_expected'].map(lambda x: 0 if x < 0 else x)

        return delivered[['order_id','wait_time','expected_wait_time','delay_vs_expected','order_status']]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'].copy()
        reviews['dim_is_five_star'] = reviews['review_score'].map(lambda x: 1 if x == 5 else 0 )
        reviews['dim_is_one_star'] = reviews['review_score'].map(lambda x: 1 if x == 1 else 0 )

        return reviews[['order_id','dim_is_five_star','dim_is_one_star','review_score']]

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        product_count_df = self.data['order_items'].groupby(by='order_id').count()[['order_item_id']]
        product_count_df.rename(columns={'order_item_id':'number_of_products'},inplace=True)
        product_count_df.sort_values(by='number_of_products',inplace=True)
        product_count_df.reset_index(inplace=True)
        return product_count_df

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        seller_count_df = self.data['order_items'].groupby(by='order_id').nunique()[['seller_id']]
        seller_count_df.rename(columns={'seller_id':'number_of_sellers'},inplace=True)
        seller_count_df.sort_values(by='number_of_sellers',inplace=True)
        seller_count_df.reset_index(inplace=True)
        return seller_count_df

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        price_freight_df = self.data['order_items'].groupby(by='order_id').agg(sum)[['price','freight_value']]
        price_freight_df.sort_values(by='freight_value',inplace=True)
        price_freight_df.reset_index(inplace=True)
        return price_freight_df

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        data=self.data
        orders = data['orders']
        order_items = data['order_items']
        sellers = data['sellers']
        customers = data['customers']

        # Since one zip code can map to multiple (lat, lng), take the first one
        geo = data['geolocation']
        geo = geo.groupby('geolocation_zip_code_prefix',
                          as_index=False).first()

        # Merge geo_location for sellers
        sellers_mask_columns = [
            'seller_id', 'seller_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'
        ]

        sellers_geo = sellers.merge(
            geo,
            how='left',
            left_on='seller_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[sellers_mask_columns]

        # Merge geo_location for customers
        customers_mask_columns = ['customer_id', 'customer_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']

        customers_geo = customers.merge(
            geo,
            how='left',
            left_on='customer_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[customers_mask_columns]

        # Match customers with sellers in one table
        customers_sellers = customers.merge(orders, on='customer_id')\
            .merge(order_items, on='order_id')\
            .merge(sellers, on='seller_id')\
            [['order_id', 'customer_id','customer_zip_code_prefix', 'seller_id', 'seller_zip_code_prefix']]

        # Add the geoloc
        matching_geo = customers_sellers.merge(sellers_geo,
                                            on='seller_id')\
            .merge(customers_geo,
                   on='customer_id',
                   suffixes=('_seller',
                             '_customer'))
        # Remove na()
        matching_geo = matching_geo.dropna()

        matching_geo.loc[:, 'distance_seller_customer'] =\
            matching_geo.apply(lambda row:
                               haversine_distance(row['geolocation_lng_seller'],
                                                  row['geolocation_lat_seller'],
                                                  row['geolocation_lng_customer'],
                                                  row['geolocation_lat_customer']),
                               axis=1)
        # Since an order can have multiple sellers,
        # return the average of the distance per order
        order_distance =\
            matching_geo.groupby('order_id',
                                 as_index=False).agg({'distance_seller_customer':
                                                      'mean'})

        return order_distance
        # $CHALLENGIFY_END

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        wait_df = Order().get_wait_time(is_delivered)
        review_df = Order().get_review_score()
        prodnum_df = Order().get_number_products()
        sellernum_df = Order().get_number_sellers()
        pricefreight_df = Order().get_price_and_freight()

        dfs = [wait_df,review_df,prodnum_df,sellernum_df,pricefreight_df]
        merged_df = reduce(lambda left, right: pd.merge(left, right, on='order_id', how='inner'), dfs)
        merged_df = merged_df[~merged_df['wait_time'].isna()]

        if with_distance_seller_customer:
            merged_df = merged_df.merge(
                self.get_distance_seller_customer(), on='order_id')

        return merged_df.dropna()
