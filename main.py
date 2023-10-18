from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


import controller, models, schemas
from database import engine
from logger import logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/address/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate):
    """
    Create Address API

    Args:
        address (schemas.AddressCreate): Address Schema object
    """
    # create address
    address_obj = models.Address.create(**address.dict())
    logger.info(f"Created address: {address_obj}")
    return address_obj


@app.get("/addresses/", response_model=list[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100):
    """
    Read Address List API

    Args:
        skip (int, optional): Defaults to 0.
        limit (int, optional): Defaults to 100.

    """
    # get and return address from database
    return models.Address.get().offset(skip).limit(limit).all()


@app.get("/address/{address_id}/", response_model=schemas.Address)
def read_address(address_id: int):
    """
    Read Address API

    Args:
        address_id (int):

    """
    try:
        # Get address from database by ID
        address_obj = models.Address.get(id=address_id).one()
    except NoResultFound:
        # Raise 404 if address not found
        logger.error(f"No address found, id: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    # Return success message
    return address_obj


@app.get("/nearby_addresses", response_model=list[schemas.Address])
def read_addresses_within_radius(
    latitude: float,
    longitude: float,
    radius: float,
):
    """
    Get nearby addresses API

    Args:
        latitude (float):
        longitude (float):
        radius (float):

    """
    # get the list of addresses within the range of given radius and return
    return controller.get_addresses_inrange(latitude, longitude, radius)


@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressUpdate):
    """
    Update address API

    Args:
        address_id (int):
        address (schemas.AddressUpdate):

    """

    try:
        # Get address from database by ID
        address_obj = models.Address.get(id=address_id).one()
        return address_obj.update(**address.dict())
    except NoResultFound:
        # Raise 404 if address not found
        logger.error(f"No address found, id: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    except IntegrityError:
        # Raise 400 if address already exists
        logger.error("Address already exists")
        raise HTTPException(status_code=400, detail="Address already exists")


@app.delete("/address/{address_id}/")
def delete_address(address_id: int):
    """
    Delete address API

    Args:
        address_id (int):
    """
    try:
        # delete address from database by ID
        address_obj = models.Address.get(id=address_id).one()
        address_obj = address_obj.delete()
        logger.info(f"Deleted address: {address_obj}")

    except NoResultFound:
        logger.error(f"No address found, id: {address_id}")
        # Raise 404 if address not found
        raise HTTPException(status_code=404, detail="Address not found")

    # Return success message
    return {"message": "Address deleted successfully"}
