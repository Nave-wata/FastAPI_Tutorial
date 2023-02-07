from fastapi import FastAPI
from typing import Union

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# 「クエリパラメータ - FastAPI」：https://fastapi.tiangolo.com/ja/tutorial/query-params/


# パスパラメータ出ない関数パラメータを宣言 -> クエリパラメータ (このメソッドでは：skip, limit)
# デフォルト値の宣言が可能
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# デフォルト値を None にするとオプショナル（必須でない）クエリパラメータを宣言可能
@app.get("/items2/{item_id}")
async def read_item2(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# bool型も宣言可能
# True => [1, True, true, on, yes]
# False => True[:]以外すべて
@app.get("/items3/{item_id}")
async def read_item3(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 複数のパスパラメータとクエリパラメータを同時に宣言可能
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# デフォルト値を宣言しなければ必須のクエリパラメータになる
@app.get("/items4/{item_id}")
async def read_user_item2(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# 必須のクエリパラメータも同時に宣言可能
@app.get("/item5/{item_id}")
async def read_user_item3(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
