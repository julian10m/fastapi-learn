from fastapi import FastAPI, Query
from typing import Annotated
from enum import Enum
from pydantic import BaseModel, AfterValidator

FAKE_ITEMS_DB = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class ModelName(Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

app = FastAPI()

@app.get('/')
async def root():
    return { 'message': 'Hello World!' }

@app.get('/items') # e.g. /items/?skip=1&limit=1&item-query=Loveaaaaaaaa
async def read_items(
    skip: int = 0,
    limit: int = 10,
    q: Annotated[str | None, Query(
        alias="item-query",
        min_length=10,
        max_length=50,
        pattern="^L",
        deprecated=True,
    )] = None, # optional
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    data = { 'items': FAKE_ITEMS_DB[skip : skip + limit] }

    if q:
        data.update({ 'q': q })

    if id:
        data.update({ 'id': id })

    return data

@app.get("/items2/")
async def read_items2(
    q: Annotated[
        str | None,
        Query(
            title="This was written by Julian",
            # alias='whatever',
            description="A nice description here",
            min_length=3
        )
    ]
): # required but can be None
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get('/items_list') # e.g. items_list?q=abc&q=def
async def read_items_list(q: Annotated[list[str] | None, Query()] = None): # optional list
    query_items = {"q": q}
    return query_items

@app.get('/items_list_defaults') # e.g. items_list?q=abc&q=def
async def read_items_list_defaults(
    q: Annotated[list[str] | None, Query()] = ['abc', 'def']
): # optional list, with defaults
    query_items = {"q": q}
    return query_items

@app.post('/items')
async def create_item(item: Item):
    item_dict = item.model_dump()

    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({ 'price_with_tax': price_with_tax })

    return item_dict

@app.get('/items/{item_id}') # /items/123?q=abc&short=1
async def get_item(item_id: int, q: str | None = None, short: bool = False):
    item = { 'item_id': item_id }

    if q:
        item.update({"q": q })

    if not short:
        item.update({ 'description': 'this is long!' })

    return item

@app.put('/items/{item_id}')
async def update_item(
    item_id: int, item: Item, q: str | None = None
):
    result = { 'item_id': item_id, **item.model_dump() }

    if q:
        result.update({ 'q': q })

    return result


@app.get('/users/me')
async def me():
    return { 'user': 'me' }

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