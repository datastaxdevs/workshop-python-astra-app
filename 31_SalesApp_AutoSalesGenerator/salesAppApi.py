import datetime
import uuid

from dbConnection import get_session
from fastapi import FastAPI, Depends
from pydantic import BaseModel

async def get_db_session():
    # this wraps getting the session in a way that works with the Depends injection
    yield cassConnect()

class Users(BaseModel):
    user_id: long
    user_email_id: str
    user_name: str
    user_phone_number: str
    user_platform: str
    user_state_code: str

class Products(BaseModel):
    product_id: long
    product_category: str
    product_code: str
    product_description: str
    product_name: str
    product_price: decimal
    product_qoh: long

class Orders(BaseModel):
    order_date: date
    order_date_hour: int
    order_timestamp: Datetime
    order_actual_shipping_date: Datetime
    order_code: uuid.UUID
    order_discount_percent: int
    order_estimated_shipping_date: Datetime
    order_grand_total: decimal
    order_number_of_products: int
    order_total: decimal
    user_email_id: text
    user_id: long
    user_name: str
    user_phone_number: str
    user_platform: str
    user_state_code: str

### API code proper

app = FastAPI()
