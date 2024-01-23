import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Menu as SchemaMenu
from schema import Submenu as SchemaSubmenu
from schema import Dish as SchemaDish

from models import Menu, Submenu, Dish

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get('/api/v1/menus')
async def get_all_menus():
    menus = db.session.query(Menu).all()
    return menus

@app.post('/api/v1/menus', response_model=SchemaMenu)
async def create_menu(menu: SchemaMenu):
    db_menu = Menu(title=menu.title, description=menu.description)
    db.session.add(db_menu)
    db.session.commit()
    return db_menu

@app.get('/api/v1/menus/{target_menu_id}')
async def get_menu_by_id(target_menu_id: int):
    db_menu = db.session.query(Menu).filter(Menu.id == target_menu_id).all()
    return db_menu

@app.patch('/api/v1/menus/{target_menu_id}', response_model=SchemaMenu)
async def update_menu_by_id(target_menu_id: str, menu: SchemaMenu):
    db_menu: Menu = db.session.query(Menu).filter(Menu.id == target_menu_id).first()
    db_menu.title = menu.title
    db_menu.description = menu.description
    db.session.commit()
    return db_menu

@app.delete('/api/v1/menus/{target_menu_id}')
async def delete_menu_by_id(target_menu_id: int):
    db_menu: Menu = db.session.query(Menu).filter(Menu.id == target_menu_id).first()
    db.session.delete(db_menu)
    db.session.commit()
    return db_menu

@app.get('/api/v1/menus/{target_menu_id}/submenus')
async def get_submenus(target_menu_id: int):
    db_menu: Menu = db.session.query(Menu).filter(Menu.id == target_menu_id).first()
    return db_menu.submenu



if __name__ == '__main__':
    uvicorn.run(app, port=8000)