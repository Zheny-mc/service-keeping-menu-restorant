from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Menu as SchemaMenu
from schema import Submenu as SchemaSubmenu
from schema import Dish as SchemaDish
from schema import PrintMenu, PrintSubmenu

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
    lst_print_menu: List[PrintMenu] = []
    for m in menus:
        lst_print_menu.append(PrintMenu(
            title=m.title,
            description=m.description,
            count_submenu=len(m.submenu),
            count_dish=sum([len(i.dish) for i in m.submenu])
        ))
    return lst_print_menu

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
    return "ok"
# -------------------- crud submenu -------------------------------
@app.get('/api/v1/menus/{target_menu_id}/submenus')
async def get_submenus(target_menu_id: int):
    db_menu: Menu = db.session.query(Menu).filter(Menu.id == target_menu_id).first()
    lst_print_submenu: List[PrintSubmenu] = []
    for sm in db_menu.submenu:
        lst_print_submenu.append(PrintSubmenu(
            title=sm.title,
            description=sm.description,
            count_dish=sm.get_count_dish()
        ))
    return lst_print_submenu

@app.post('/api/v1/menus/{target_menu_id}/submenus', response_model=SchemaSubmenu)
async def create_submenus(target_menu_id: str, submenu: SchemaSubmenu):
    db_submenu: Submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=target_menu_id)
    db.session.add(db_submenu)
    db.session.commit()
    return db_submenu

@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=SchemaSubmenu)
async def get_submenus_by_id(target_menu_id: int, target_submenu_id: int):
    db_submenu = db.session.query(Submenu).filter(Submenu.menu_id == target_menu_id,
                                                  Submenu.id == target_submenu_id).first()
    return db_submenu

@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=SchemaSubmenu)
async def update_submenus_by_id(target_menu_id: int, target_submenu_id: int, submenu: SchemaSubmenu):
    db_submenu: Submenu = db.session.query(Submenu).filter(Submenu.menu_id == target_menu_id,
                                                  Submenu.id == target_submenu_id).first()
    db_submenu.title = submenu.title
    db_submenu.description = submenu.description
    db.session.commit()
    return db_submenu

@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def delete_submenus_by_id(target_menu_id: int, target_submenu_id: int):
    db_submenu = db.session.query(Submenu).filter(Submenu.menu_id == target_menu_id,
                                                  Submenu.id == target_submenu_id).first()
    db.session.delete(db_submenu)
    db.session.commit()
    return 'ok'

@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
async def get_all_dishs(target_menu_id: int, target_submenu_id: int):
    db_submenu: Submenu = db.session.query(Submenu).filter(Submenu.menu_id == target_menu_id,
                                                  Submenu.id == target_submenu_id).first()
    return db_submenu.dish

@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=SchemaDish)
async def create_dish(target_menu_id: int, target_submenu_id: int, dish: SchemaDish):
    db_dish = Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=target_submenu_id)
    db.session.add(db_dish)
    db.session.commit()
    return db_dish

@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=SchemaDish)
async def get_dish_by_id(target_menu_id: int, target_submenu_id: int, target_dish_id: int):
    db_dish: Dish = db.session.query(Dish).filter(Dish.submenu_id == target_submenu_id,
                                                  Dish.id == target_dish_id).first()
    return db_dish

@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=SchemaDish)
async def update_dish_by_id(target_menu_id: int, target_submenu_id: int, target_dish_id: int, dish: SchemaDish):
    db_dish: Dish = db.session.query(Dish).filter(Dish.submenu_id == target_submenu_id,
                                                  Dish.id == target_dish_id).first()
    db_dish.title = dish.title
    db_dish.description = dish.description
    db_dish.price = dish.price
    db.session.commit()
    return db_dish

@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def delete_dish_by_id(target_menu_id: int, target_submenu_id: int, target_dish_id: int):
    db_dish: Dish = db.session.query(Dish).filter(Dish.submenu_id == target_submenu_id,
                                                  Dish.id == target_dish_id).first()
    db.session.delete(db_dish)
    db.session.commit()
    return "ok"

if __name__ == '__main__':
    uvicorn.run(app, port=8000)