from sqlalchemy.orm import Session
from geopy.distance import geodesic
import models, schemas


def create_address(db: Session, address: schemas.AddressCreate):
    """
    Create address

    Args:
        db (Session):
        address (schemas.AddressCreate):
    """
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address_by_id(db: Session, address_id: int):
    """
    Get address by id

    Args:
        db (Session):
        address_id (int):

    """
    return db.query(models.Address).filter(models.Address.id == address_id).one()


def get_address(db: Session, skip: int = 0, limit: int = 100):
    """
    Get address list
    Args:
        db (Session):
        skip (int, optional): Defaults to 0.
        limit (int, optional): Defaults to 100.

    """
    return db.query(models.Address).offset(skip).limit(limit).all()


def update_address(db: Session, address_id: int, address: schemas.Address):
    """
    update address

    Args:
        db (Session):
        address_id (int):
        address (schemas.Address):

    """
    db_address = db.query(models.Address).filter(models.Address.id == address_id).one()
    for field, value in address:
        setattr(db_address, field, value)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def delete_address(db: Session, address_id: int):
    """
    delete address

    Args:
        db (Session):
        address_id (int):

    """
    db_address = db.query(models.Address).filter(models.Address.id == address_id).one()
    db.delete(db_address)
    db.commit()
    return db_address


def get_addresses_inrange(db: Session, lat: float, long: float, radius: float):
    """
    get addresses in range

    Args:
        db (Session):
        lat (float):
        long (float):
        radius (float):
    """
    address_list = db.query(models.Address).all()

    # filter has been done using python geopy library
    # this part of code is not efficient as it reads whole the address table and then filter the nearby addresses,
    # it can be optimized using GeoAlchemy2 with PostgreSQL(which supports spatial databases)
    address_inrange = [
        address
        for address in address_list
        if location_in_range(address, lat, long, radius)
    ]
    return address_inrange


def location_in_range(
    address: models.Address, lat: float, long: float, radius: float
) -> bool:
    """
    function to check if a given location is within the radius

    Args:
        address (_type_):
        lat (_type_):
        long (_type_):
        radius (_type_):

    Returns:
        bool:
    """
    return get_distance(address, lat, long) <= radius


def get_distance(address: models.Address, lat: float, long: float) -> float:
    """
    calculate distance between a given address and a location(lat, long)

    Args:
        address (models.Address):
        lat (float):
        long (float):

    Returns:
        float: distance
    """
    return geodesic((address.lat, address.long), (lat, long)).km
