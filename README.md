# Ecommerce Analysis

##  1. Context:

### 1.1 Problem Statement

How could Olist improve it's profit? 

### 1.2 Who is Olist?
Olist is a leading e-commerce service that connects small businesses from all over Brazil to main marketplaces channels. Those merchants are able to sell their products through the Olist store and ship them diretly to the customers using Olist logistics parterns. 

After a customer purchases the product from Olist Store, the seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments.

Olist charges sellers a monthly subscription fee and a sales fee for each orders. 


### 1.3 Dataset

Dataset contains information on 100k orders from 2016 to 2018 made on Olist, covering various aspects such as status, price, products, payment methods, payment and freight performance, customer review scores, etc. 

### 1.4 P&L Rules

Revenues:
- Sales fee: Olist takes 10% cut on the product price (excl. freight) of each order delivered
- Subscription fees: Olist charges 80 BRL by month per seller

Reputation Cost: 

In the long term, bad customer experience has business implicatins: low repeat rate, immediate customer support cost, refunds or unfavourable word of mouth communication. We will have an estimate measure of the monetary cost for each bad review. 

## 2.Steps
1. Feature Engineering
2. Explatory Data Analysis
3. Conclusion

## FEATURE ENGINEERING

### Orders

👉 We have created the `get_training_data` method in `olist/order.py` which returns a DataFrame with the following features:

| feature_name              | type  | description                                                                 |
|:--------------------------|:-----:|:----------------------------------------------------------------------------|
| `order_id`                | str   | the id of the order                                                         |
| `wait_time`               | float | the number of days between order_purchase_timestamp and order_delivered_customer_date |
| `expected_wait_time`      | float | the number of days between order_purchase_timestamp and estimated_delivery_date |
| `delay_vs_expected`       | float | if the actual order_delivered_customer_date is later than the estimated delivery date, returns the number of days between the two dates, otherwise return 0 |
| `order_status`            | str   | the status of the order                                                     |
| `dim_is_five_star`        | int   | 1 if the order received a five-star review, 0 otherwise                     |
| `dim_is_one_star`         | int   | 1 if the order received a one_star, 0 otherwise                             |
| `review_score`            | int   | from 1 to 5                                                                 |
| `number_of_products`      | int   | number of products that the order contains                                  |
| `number_of_sellers`       | int   | number of sellers involved in the order                                     |
| `price`                   | float | total price of the order paid by customer                                   |
| `freight_value`           | float | value of the freight paid by customer                                       |
| `distance_customer_seller`| float | the distance in km between customer and seller (optional)                   |

### Sellers

👉 We have created the `get_training_data` method in `olist/seller.py` which returns a DataFrame with the following features:

| feature_name          | type   | description                                                              |
|-----------------------|--------|--------------------------------------------------------------------------|
| `seller_id`           | str    | the id of the seller **UNIQUE**                                           |
| `seller_city`         | str    | the city where seller is located                                          |
| `seller_state`        | str    | the state where seller is located                                         |
| `delay_to_carrier`    | float  | returns 0 if the order is delivered before the shipping_limit_date, otherwise the value of the delay |
| `wait_time`           | float  | average wait_time (duration of deliveries) per seller                     |
| `date_first_sale`     | datetime | date of the first sale on Olist                                         |
| `date_last_sale`      | datetime | date of the last sale on Olist                                          |
| `months_on_olist`     | float  | round number of months on Olist                                           |
| `share_of_five_stars` | float  | share of five-star reviews for orders in which the seller was involved     |
| `share_of_one_stars`  | float  | share of one-star reviews for orders in which the seller was involved      |
| `review_score`        | float  | average review score for orders in which the seller was involved           |
| `n_orders`            | int    | number of unique orders the seller was involved with                      |
| `quantity`            | int    | total number of items sold by this seller                                 |
| `quantity_per_order`  | float  | average number of items per order for this seller                         |
| `sales`               | float  | total sales associated with this seller (excluding freight value) in BRL   |

### Products

👉 We have created the `get_training_data` method in `olist/product.py` which returns a DataFrame with the following features:

| feature_name                  |  type   | description                                                                |
|:------------------------------|:-------:|:---------------------------------------------------------------------------|
| `product_id`                  |   str   | id of the product **UNIQUE**                                               |
| `category`                    |   str   | category name (in English)                                                 |
| `product_name_length`         |  float  | number of characters of a product name                                     |
| `product_description_length`  |  float  | number of characters of a product description                              |
| `product_photos_qty`          |   int   | number of photos available for a product                                   |
| `product_weight_g`            |  float  | weight of the product                                                      |
| `product_length_cm`           |  float  | length of the product                                                      |
| `product_height_cm`           |  float  | height of the product                                                      |
| `product_width_cm`            |  float  | width of the product                                                       |
| `price`                       |  float  | average price at which the product is sold                                 |
| `wait_time`                   |  float  | average wait time (in days) for orders in which the product was sold       |
| `share_of_five_stars`         |  float  | share of five-star review scores for orders in which the product was sold  |
| `share_of_one_stars`          |  float  | share of one-star review scores for orders in which the product was sold   |
| `review_score`                |  float  | average review score of the orders in which the product was sold           |
| `n_orders`                    |   int   | number of orders in which the product appears                              |
| `quantity`                    |   int   | total number of products sold for each product_id                          |
| `sales`                       |   int   | total sales (in BRL) for each product_id                                   |

[notebooks/EDA-orders.ipynb]
