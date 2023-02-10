from typing import Union
from fastapi import FastAPI, Query
from pydantic import Required


app = FastAPI()


# 「クエリパラメータと文字列の検証」：https://fastapi.tiangolo.com/ja/tutorial/query-params-str-validations/


# ペラメータの追加情報とバリデーションを宣言することができる
@app.get("/items/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Queryを利用して様々なバリデーションを使用できる（最大長）
@app.get("/items2/")
async def read_items2(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"items": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Queryを利用して様々なバリデーションを使用できる（最小長）
@app.get("/items3")
async def read_items3(
    q: Union[str, None] = Query(default=None, min_length=3, max_length=50)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Queryを利用して様々なバリデーションを使用できる（正規表現）
@app.get("/items4/")
async def read_items4(
    q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, regex="^fixedquery$"
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# デフォルト値にはNone以外も指定できる
@app.get("/items5/")
async def read_item5(q: str = Query(default="fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# デフォルト値は省略記号（...）で値を必須にできる
@app.get("/items6/")
async def read_item6(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# パラメータがNoneを受け入れることができるが，必須である場合
@app.get("/items7/")
async def read_item7(q: Union[str, None] = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# パラメータがNoneを受け入れることができるが，必須である場合
# 省略記号の代わりにRequiredを使用することができる
# ほとんどの場合，defaultパラメータを省略できるため，省略記号もRequiredも使用する必要がない
@app.get("/items8/")
async def read_item8(q: Union[str, None] = Query(default=Required, min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# http://localhost:8000/items9/?q=foo&q=bar
# の様に複数の値を許可する（list）
@app.get("/items9/")
async def read_items9(q: Union[list[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items


# listもデフォルト値を定義できる
@app.get("/items10/")
async def read_items10(q: list[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# パラメータに関する情報を追加することができる
# この情報はドキュメントのユーザインターフェースや外部のツールで使用される
# title, description
@app.get("/items11/")
async def read_items11(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# aliasを使用するとパラメータの値を任意のものに変更できる
# http://localhost:8000/items12/?item-query=foo
# ここでは item-query で，qに値が入る
@app.get("/items12/")
async def read_items12(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 非推奨パラメータ
# deprecated=True
@app.get("/items13/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
