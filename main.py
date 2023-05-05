from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


import crud, models, schemas
from database import SessionLocal, engine
from logger import logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/address/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """
    Create Address API

    Args:
        address (schemas.AddressCreate): Address Schema object
        db (Session, optional): Defaults to Depends(get_db).

    """
    # create address
    db_address = crud.create_address(db=db, address=address)
    logger.info(f"Created address: {db_address}")
    return db_address


@app.get("/addresses/", response_model=list[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read Address List API

    Args:
        skip (int, optional): Defaults to 0.
        limit (int, optional): Defaults to 100.
        db (Session, optional): Defaults to Depends(get_db).

    """
    # get and return address from database
    return crud.get_address(db, skip=skip, limit=limit)


@app.get("/address/{address_id}/", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    """
    Read Address API

    Args:
        address_id (int):
        db (Session, optional): Defaults to Depends(get_db).

    """
    try:
        # Get address from database by ID
        db_address = crud.get_address_by_id(db=db, address_id=address_id)
    except NoResultFound:
        # Raise 404 if address not found
        logger.error(f"No address found, id: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    # Return success message
    return db_address


@app.get("/nearby_addresses", response_model=list[schemas.Address])
def read_addresses_within_radius(
    latitude: float, longitude: float, radius: float, db: Session = Depends(get_db)
):
    """
    Get nearby addresses API

    Args:
        latitude (float):
        longitude (float):
        radius (float):
        db (Session, optional): Defaults to Depends(get_db).

    """
    # get the list of addresses within the range of given radius and return
    return crud.get_addresses_inrange(db, latitude, longitude, radius)


@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(
    address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)
):
    """
    Update address API

    Args:
        address_id (int):
        address (schemas.AddressUpdate):
        db (Session, optional): Defaults to Depends(get_db).

    """

    try:
        # Get address from database by ID
        return crud.update_address(db, address_id=address_id, address=address)
    except NoResultFound:
        # Raise 404 if address not found
        logger.error(f"No address found, id: {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")
    except IntegrityError:
        # Raise 400 if address already exists
        logger.error("Address already exists")
        raise HTTPException(status_code=400, detail="Address already exists")


@app.delete("/address/{address_id}/")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete address API

    Args:
        address_id (int):
        db (Session, optional): Defaults to Depends(get_db).
    """
    try:
        # delete address from database by ID
        db_address = crud.delete_address(db=db, address_id=address_id)
        logger.info(f"Deleted address: {db_address}")

    except NoResultFound:
        logger.error(f"No address found, id: {address_id}")
        # Raise 404 if address not found
        raise HTTPException(status_code=404, detail="Address not found")

    # Return success message
    return {"message": "Address deleted successfully"}
