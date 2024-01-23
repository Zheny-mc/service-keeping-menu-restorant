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
    menu_id: int

    class Config:
        from_attributes = True

class Dish(BaseModel):
    title: str
    description: str
    price: int
    submenu_id: int

    class Config:
        from_attributes = True