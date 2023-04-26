from sqlalchemy.orm import Session
from geopy.distance import geodesic
import models, schemas

def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address(db: Session,  skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()


def get_addresses_inrange(db: Session, lat: float, long: float, radius: float):
    address_list = db.query(models.Address).all()

    # filter has been done using python geopy library 
    # this part of code is not efficient as it reads whole the address table and then filter the nearby addresses, 
    # it can be optimized using GeoAlchemy2 with PostgreSQL(which supports spatial databases) 
    address_inrange = [address for address in address_list if location_in_range(address, lat, long, radius)]
    return address_inrange

def location_in_range(address, lat, long, radius) -> bool:
    return get_distance(address, lat, long) <= radius

def get_distance(address, lat, long):
    return geodesic(
        (address.lat, address.long),
        (lat, long)
    ).km
