from enum import Enum
from fastapi import FastAPI

app = FastAPI()


# 「パスパラメータ - FastAPI」：https://fastapi.tiangolo.com/ja/tutorial/path-params/


# パスパラメータ{item_id}，型宣言
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# 先に宣言した方が優先
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


# "/users/me" はこのメソッドで処理されない
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# Enumクラスが利用可能
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# パスを含んだパスパラメータ（URL内で「/」が含まれるようなパラメータ）が利用可能
# "/files/foo/bar/" でアクセスすると，file_path="foo/bar"
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
