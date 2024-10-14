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

## Steps
1. Feature Engineering
2. Explatory Data Analysis
3. Conclusion

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

