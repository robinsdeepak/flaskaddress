from pydantic import BaseModel, validator


class AddressBase(BaseModel):
    name: str
    lat: float
    long: float


class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True


class AddressCreate(AddressBase):
    @validator("name")
    def validate_name(cls, v):
        if v == "":
            raise ValueError("name can't be empty!")
        return v

    @validator("lat")
    def validate_lat(cls, v):
        if v < -90 or v > 90:
            raise ValueError("latitute should be in range -90 to 90")

        return v

    @validator("long")
    def validate_long(cls, v):
        if v < -180 or v > 180:
            raise ValueError("longitute should be in range -180 to 180")

        return v


class AddressUpdate(AddressCreate):
    pass
