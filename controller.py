from geopy.distance import geodesic
import models


def get_addresses_inrange(lat: float, long: float, radius: float):
    """
    get addresses in range

    Args:
        db (Session):
        lat (float):
        long (float):
        radius (float):
    """

    address_list = models.Address.get().all()

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
