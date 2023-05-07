from sqlalchemy import Column, Integer, String, Float
from database import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lat = Column(Float)
    long = Column(Float)

    def __str__(self):
        return str(
            {"id": self.id, "name": self.name, "lat": self.lat, "long": self.long}
        )
