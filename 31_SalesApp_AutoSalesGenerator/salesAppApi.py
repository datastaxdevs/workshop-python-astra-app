import datetime
import uuid

from dbConnection import get_session
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from datetime import date

async def get_db_session():
    # this wraps getting the session in a way that works with the Depends injection
    yield get_session()

class User(BaseModel):
    user_id: int
    user_email_id: str
    user_name: str
    user_phone_number: str
    user_platform: str
    user_state_code: str

class Product(BaseModel):
    product_id: int
    product_category: str
    product_code: str
    product_description: str
    product_name: str
    product_price: Decimal
    product_qoh: int

class Order(BaseModel):
    order_date: date
    order_date_hour: int
    order_timestamp: datetime
    order_actual_shipping_date: datetime
    order_code: uuid.UUID
    order_discount_percent: int
    order_estimated_shipping_date: datetime
    order_grand_total: Decimal
    order_number_of_products: int
    order_total: Decimal
    user_email_id: str
    user_id: int
    user_name: str
    user_phone_number: str
    user_platform: str
    user_state_code: str

class SalesOrderProduct(BaseModel):
    order_date: date
    order_code: uuid.UUID
    product_id: int
    product_category: str
    product_code: str
    product_name: str
    product_price_each: Decimal
    product_price_total: Decimal
    product_sold_quantity: int

prepared_user_select = None
def get_prepared_user_select(session):
    global prepared_user_select
    if prepared_user_select is None:
        prepared_user_select = session.prepare("SELECT user_id, user_email_id, user_name, user_phone_number, user_platform, user_state_code FROM users WHERE user_id = ?")

    return prepared_user_select

prepared_product_select = None
def get_prepared_product_select(session):
    global prepared_product_select
    if prepared_product_select is None:
        prepared_product_select = session.prepare("SELECT product_id, product_category, product_code, product_description, product_name, product_price, product_qoh FROM products WHERE product_id = ?")

    return prepared_product_select

prepared_order_select = None
def get_prepared_order_select(session):
    global prepared_order_select
    if prepared_order_select is None:
        prepared_order_select = session.prepare("SELECT order_date, order_date_hour, order_timestamp, order_code, order_actual_shipping_date, order_discount_percent, order_estimated_shipping_date, order_grand_total, order_number_of_products, order_total, user_email_id, user_id, user_name, user_phone_number, user_platform, user_state_code FROM sales_orders WHERE order_date = ? AND order_date_hour = ?")

    return prepared_order_select

prepared_sales_order_product_select = None
def get_prepared_sales_order_product_select(session):
    global prepared_sales_order_product_select
    if prepared_sales_order_product_select is None:
        prepared_sales_order_product_select = session.prepare("SELECT order_date, order_code, product_id, product_category, product_code, product_name, product_price_each, product_price_total, product_sold_quantity FROM sales_order_products WHERE order_date = ? AND order_code = ?")

    return prepared_sales_order_product_select

### API code proper

app = FastAPI()

@app.get('/user/{id}')
async def get_user(id: int, session=Depends(get_db_session)):
    prepared = get_prepared_user_select(session)

    return [
        {
            'user_id': user.user_id,
            'user_email_id': user.user_email_id,
            'user_name': user.user_name,
            'user_phone_number': user.user_phone_number,
            'user_platform': user.user_platform,
            'user_state_code': user.user_state_code,
        }
        for user in session.execute(prepared_user_select, (int(id),))
    ]

@app.get('/users/{limit}')
async def get_users(limit: int, session=Depends(get_db_session)):

    strCQL = "SELECT user_id, user_email_id, user_name, user_phone_number, user_platform, user_state_code FROM users LIMIT " + str(limit)
    return [
        {
            'user_id': user.user_id,
            'user_email_id': user.user_email_id,
            'user_name': user.user_name,
            'user_phone_number': user.user_phone_number,
            'user_platform': user.user_platform,
            'user_state_code': user.user_state_code,
        }
        for user in session.execute(strCQL)
    ]

@app.get('/product/{id}')
async def get_product(id: int, session=Depends(get_db_session)):
    prepared = get_prepared_product_select(session)

    return [
        {
            'product_id': product.product_id,
            'product_category': product.product_category,
            'product_code': product.product_code,
            'product_description': product.product_description,
            'product_name': product.product_name,
            'product_price': product.product_price,
            'product_qoh': product.product_qoh,
        }
        for product in session.execute(prepared_product_select, (int(id),))
    ]

@app.get('/products/{limit}')
async def get_products(limit: int, session=Depends(get_db_session)):

    strCQL = "SELECT product_id, product_category, product_code, product_description, product_name, product_price, product_qoh FROM products LIMIT " + str(limit)
    return [
        {
            'product_id': product.product_id,
            'product_category': product.product_category,
            'product_code': product.product_code,
            'product_description': product.product_description,
            'product_name': product.product_name,
            'product_price': product.product_price,
            'product_qoh': product.product_qoh,
        }
        for product in session.execute(strCQL)
    ]

@app.get('/orders/date/{order_date}/hour/{hour}')
async def get_orders_date_hour(order_date: date, hour: int, session=Depends(get_db_session)):
    prepared = get_prepared_order_select(session)

    return [
        {
            'order_date': order.order_date,
            'order_date_hour': order.order_date_hour,
            'order_timestamp': order.order_timestamp,
            'order_actual_shipping_date': order.order_actual_shipping_date,
            'order_code': order.order_code,
            'order_discount_percent': order.order_discount_percent,
            'order_estimated_shipping_date': order.order_estimated_shipping_date,
            'order_grand_total': order.order_grand_total,
            'order_number_of_products': order.order_number_of_products,
            'order_total': order.order_total,
            'user_id': order.user_id,
            'user_email_id': order.user_email_id,
            'user_name': order.user_name,
            'user_phone_number': order.user_phone_number,
            'user_platform': order.user_platform,
            'user_state_code': order.user_state_code,
        }
        for order in session.execute(prepared_order_select, (order_date, hour))
    ]

@app.get('/orders/{limit}')
async def get_orders(limit: int, session=Depends(get_db_session)):

    strCQL = "SELECT order_date, order_date_hour, order_timestamp, order_code, order_actual_shipping_date, order_discount_percent, order_estimated_shipping_date, order_grand_total, order_number_of_products, order_total, user_email_id, user_id, user_name, user_phone_number, user_platform, user_state_code FROM sales_orders LIMIT " + str(limit)
    return [
        {
            'order_date': order.order_date,
            'order_date_hour': order.order_date_hour,
            'order_timestamp': order.order_timestamp,
            'order_actual_shipping_date': order.order_actual_shipping_date,
            'order_code': order.order_code,
            'order_discount_percent': order.order_discount_percent,
            'order_estimated_shipping_date': order.order_estimated_shipping_date,
            'order_grand_total': order.order_grand_total,
            'order_number_of_products': order.order_number_of_products,
            'order_total': order.order_total,
            'user_id': order.user_id,
            'user_email_id': order.user_email_id,
            'user_name': order.user_name,
            'user_phone_number': order.user_phone_number,
            'user_platform': order.user_platform,
            'user_state_code': order.user_state_code,
        }
        for order in session.execute(strCQL)
    ]

@app.get('/orderproducts/date/{order_date}/code/{order_code}')
async def get_orders_date_hour(order_date: date, order_code: uuid.UUID, session=Depends(get_db_session)):
    prepared = get_prepared_sales_order_product_select(session)

    return [
        {
            'order_date': salesorderproduct.order_date,
            'order_code': salesorderproduct.order_code,
            'product_id': salesorderproduct.product_id,
            'product_category': salesorderproduct.product_category,
            'product_code': salesorderproduct.product_code,
            'product_name': salesorderproduct.product_name,
            'product_price_each': salesorderproduct.product_price_each,
            'product_price_total': salesorderproduct.product_price_total,
            'product_sold_quantity': salesorderproduct.product_sold_quantity,
        }
        for salesorderproduct in session.execute(prepared_sales_order_product_select, (order_date, order_code))
    ]
