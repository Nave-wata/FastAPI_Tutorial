from typing import Union
from fastapi import FastAPI, Path, Query


app = FastAPI()


# 「パスパラメータと数値検証」：https://fastapi.tiangolo.com/ja/tutorial/path-params-numeric-validations/


# PathはQueryと同じパラメータをすべて宣言できる
# Pathはパスパラメータ
# Queryはクエリパラメータ
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The Id of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# FastAPIはパスパラメータとクエリパラメータの順序を気にしない
@app.get("/items2/{item_id}")
async def read_items2(q: str, item_id: int = Path(title="THe ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# 関数の最初のパラメータとして「*」を渡すと，
# すべてのパラメータをキーワード引数として呼び出すことを強制できる
# （今までもクエリパラメータはキーと値のペアで渡していたので違いは不明）
@app.get("/items3/{item_id}")
async def read_items3(
    *, item_id: int = Path(title="THe ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# ge=1 は item_id の値が「1以上」の整数であることを強制できる
@app.get("/items4/{item_id}")
async def read_item4(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# gt=0 「0より大きくなければならない」
# le=1000 「1000以下でなければならない」
@app.get("/items5/{item_id}")
async def read_items5(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# ge=0「0以上」
# lt=10.5「10.5より小さい」
@app.get("/items7/{item_id}")
async def read_items7(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
