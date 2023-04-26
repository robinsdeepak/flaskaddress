from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session


import crud, models, schemas
from database import SessionLocal, engine

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
    return crud.create_address(db, address=address)


@app.get("/address/", response_model=list[schemas.Address])
def read_address(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_address(db, skip=skip, limit=limit)

@app.get('/nearby_addresses', response_model=list[schemas.Address])
def read_addresses_within_radius(latitude: float, longitude: float, radius: float, db: Session = Depends(get_db)):
    return crud.get_addresses_inrange(db, latitude, longitude, radius)

