from pydantic import BaseModel


class AddressBase(BaseModel):
    name: str
    lat: float
    long: float

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True

class AddressCreate(AddressBase):
    pass

