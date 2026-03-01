from fastapi import FastAPI
from enum import Enum

FAKE_ITEMS_DB = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class ModelName(Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'



app = FastAPI()

@app.get('/')
async def root():
    return { 'message': 'Hello World!' }

@app.get('/items/{item_id}') # /items/123?q=abc&short=1
async def get_item(item_id: int, q: str | None = None, short: bool = False):
    item = { 'item_id': item_id }
    
    if q:
        item.update({"q": q})
    
    if not short:
        item.update({ 'description': 'this is long!' })
    
    return item 

@app.get('/items') # e.g. /items/?skip=1&limit=1
async def read_items(skip: int = 0, limit: int = 10):
    return FAKE_ITEMS_DB[skip : skip + limit]


@app.get('/users/me')
async def me():
    return { 'user': 'me'}

@app.get('/users/{user_id}') # /users/1234
async def get_user(user_id: int):
    return { 'user_id': user_id }

@app.get('/users/{user_id}/items/{item_id}')
async def get_user_item(
    user_id: int, item_id: int, needy: str, q: str | None = None, short: bool = False
):
    item  = { 'item_id': item_id, 'user_id': user_id, 'needy': needy }

    if q:
        item.update({"q": q})
    
    if not short:
        item.update({ 'description': 'this is long!' })

    return item 


@app.get('/models/{model_name}') # /models/alexnet
async def get_model(model_name: ModelName):    
    if model_name is ModelName.alexnet:
        message = 'Alex'
    
    elif model_name is ModelName.lenet:
        message = 'Lacun'

    else: # ModelName.resnet
        message = 'Resnet'

    return { 'model_name': model_name, 'message': message}


@app.get('/files/{file_path:path}') # e.g. /files//home/pepo/file.txt
async def get_file(file_path: str): 
    return { 'file_path': file_path }