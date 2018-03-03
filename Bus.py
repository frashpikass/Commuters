import random as r

import Locations


class Bus(object):
    old_id = 0

    def __init__(self, position, probability_of_advancing):
        # type: (str, float) -> None
        self.id = Bus.old_id
        Bus.old_id = Bus.old_id + 1

        self.last_position = position
        """Pointer to the last bus stop visited"""

        self.is_at_bus_stop = True
        self.probability_of_advancing = probability_of_advancing

        self.passengers = list()

    def __contains__(self, passenger):
        """
        Returns True if the given passenger is on board
        :param passenger: the passenger to check for
        :return: True if the given passenger is on board
        """
        return passenger in self.passengers

    def has_inspector(self):
        """
        Checks if this bus has an inspector on board
        :return: True if this bus has an inspector on board, False otherwise
        """
        return len(self.get_inspectors()) > 0

    def get_tricksters(self):
        """
        If the bus has some tricksters on board, return them
        :return: tricksters on board
        """
        return [trickster for trickster in self if not trickster.has_ticket]

    def get_inspectors(self):
        """
        If the bus has some tricksters on board, return them
        :return: tricksters on board
        """
        return [inspector for inspector in self if inspector.mark is "T"]

    def should_advance(self):
        """
        Returns true if the bus should advance to the next bus stop
        :return: true if the bus has to advance
        """

        if r.random() <= self.probability_of_advancing:
            return True
        else:
            return False

    def try_to_advance(self):
        """
        Try to advance with this bus, the Italian way. If the bus is travelling, it won't be at a bus stop.
        If it has arrived somewhere, it will be at the next bus stop from the last position recorded.
        Advancement is random
        :return:
        """
        if self.should_advance():
            self.last_position = Locations.get_next(self.last_position)
            self.is_at_bus_stop = True
        else:
            self.is_at_bus_stop = False

    def drop_all_passengers(self, passengers):
        """
        Drops all passengers specified
        :param passengers: list of passengers to drop
        """
        for passenger in passengers:
            self.passengers.remove(passenger)

    def collect_all_passengers(self, passengers):
        """
        Collects all passengers in the provided list of passengers and registers them on board
        :param passengers: list of passengers to collect
        """
        for p in passengers:
            self.passengers.append(p)
            p.position = str(self)

    def __str__(self):
        return "Bus %d" % self.id

    def __iter__(self):
        return iter(self.passengers)

    def __cmp__(self, other):
        """
        Compare this Bus to another according to its id number
        :param other: the other bus
        :return: the sign of the difference between the IDs of the two buses,
        -1 if x < y, returns 0 if x == y and 1 if x > y
        """
        comparison = self.id - other.id
        if comparison < 0:
            return -1
        elif comparison > 0:
            return 1
        else:
            return -1

    def __eq__(self, other):
        return self.id == other.id
