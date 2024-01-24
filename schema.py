# build a schema using pydantic
from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True

class Submenu(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True

class Dish(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        from_attributes = True

class PrintMenu(BaseModel):
    title: str
    description: str
    count_submenu: int
    count_dish: int

class PrintSubmenu(BaseModel):
    title: str
    description: str
    count_dish: int