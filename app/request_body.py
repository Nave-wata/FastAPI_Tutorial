from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI()


# 「リクエストボディ - FastAPI」：https://fastapi.tiangolo.com/ja/tutorial/body/


# データモデル
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


# データモデルをパラメータとして宣言（リクエストボディ）
@app.post("/items/")
async def create_item(item: Item):
    return item


# 関数内部でモデルすべての属性に直接アクセス可
@app.post("/items2")
async def create_item2(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# パスパラメータとリクエストボディを同時に宣言可能
@app.put("/items3/{item_id}")
async def create_item3(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# パスパラメータ・クエリパラメータ・リクエストボディを同時に宣言可能
@app.put("/items4/{item_id}")
async def create_item4(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
