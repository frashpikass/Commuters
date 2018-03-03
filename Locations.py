import random as r


LOCATIONS = ("Brescia", "Sarezzo", "Concesio", "Bergamo", "Flero", "Desenzano")


def get_random_source():
    """
    Generate a random source location from the available ones
    :return: A randomly chosen location (not the destination)
    """
    return LOCATIONS[r.randrange(1, len(LOCATIONS))]


def get_next(location):
    """
    Returns the next location in the tuple of available locations.
    Locations are considered to be in a loop, so the next location after the last one returns the first one.
    In case of location not found, returns the first location
    :param location: the location before the one to return
    :return: the next location
    """

    try:
        index = (LOCATIONS.index(location) + 1) % len(LOCATIONS)
        next_location = LOCATIONS[index]
    except ValueError:
        next_location = LOCATIONS[0]

    return next_location
