from sqlalchemy import Column, Integer, String, Float
from database import Base
from database import SessionLocal
from sqlalchemy import UniqueConstraint


class CRUDMixin:
    @classmethod
    def create(cls, **kwargs):
        with SessionLocal() as db:
            obj = cls(**kwargs)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

    def update(self, **kwargs):
        db = self._sa_instance_state.session
        for field, value in kwargs.items():
            print(field, value)
            setattr(self, field, value)
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    @classmethod
    def get(cls, **kwargs):
        with SessionLocal() as db:
            return db.query(cls).filter(
                *(getattr(cls, key) == value for key, value in kwargs.items())
            )

    def delete(self):
        db = self._sa_instance_state.session
        db.delete(self)
        db.commit()
        return self


class Address(Base, CRUDMixin):
    __tablename__ = "address"

    __table_args__ = (UniqueConstraint("lat", "long"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lat = Column(Float)
    long = Column(Float)

    def __str__(self):
        return str(
            {"id": self.id, "name": self.name, "lat": self.lat, "long": self.long}
        )
