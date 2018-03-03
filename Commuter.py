import random as r
import Locations


class Commuter(object):
    old_id = 0
    MALE_NAMES = ("Derek", "Franz", "Pablo", "Andrea", "Jacob", "Ayeye Brazov", "Natale", "Carlo", "Marcello")
    FEMALE_NAMES = ("Tina", "Dana", "Consuelo", "Dominica", "Aurora", "Paola", "Deana", "Masha", "Sandra")
    MARKS = ("M", "F", "T")
    P_HAS_TICKET = 0.8
    P_MALE = 0.5
    PATIENCE = 60

    def __init__(self):
        self.id = Commuter.old_id
        Commuter.old_id = Commuter.old_id + 1

        self.sex = self.generate_sex()
        self.mark = Commuter.MARKS[self.sex]
        self.name = self.generate_name()

        self.hometown = Locations.get_random_source()
        self.position = self.hometown
        self.has_ticket = self.generate_ticket()
        self.travel_time = 0

    def generate_name(self):
        """
        Generate a random name for a Commuter
        :return: a randomly generated commuter name
        """
        if self.sex is 0:
            return Commuter.MALE_NAMES[r.randrange(len(Commuter.MALE_NAMES))]
        else:
            return Commuter.FEMALE_NAMES[r.randrange(len(Commuter.FEMALE_NAMES))]

    def generate_sex(self):
        """
        Generate a random sex for a Commuter
        :return: a randomly generated Commuter sex
        """
        return r.randrange(2)

    def generate_ticket(self):
        """
        Generate a random ticket for a Commuter (valid or not valid)
        :return: a randomly generated ticket for a Commuter
        """
        return r.random() <= Commuter.P_HAS_TICKET

    def age(self, time):
        """
        Increases travel time for the current commuter
        :param time: how much time has passed
        """
        self.travel_time = self.travel_time + time

    def wants_to_drop(self):
        """
        Check if this Commuter is tired and wants to drop
        :return: True if this commuter is tired and wants to drop
        """
        return self.travel_time >= Commuter.PATIENCE

    def possessive_adjective(self):
        # type: () -> str
        """
        Generates the correct possessive adjective for this Commuter
        :return: the possessive adjective string
        """
        if self.mark is "M":
            return "his"
        if self.mark is "F":
            return "her"
        else:
            return "their"

    def __str__(self):
        out = "Id: %s, Name: %s, Mark: %s, Has Ticket: %s, Hometown: %s, Travel time: %s" \
            % (self.id, self.name, self.mark, self.has_ticket, self.hometown, self.travel_time)
        return out

    def __cmp__(self, other):
        """
        Compare this Commuter to another commuter according to its id number
        :param other: the other commuter
        :return: the sign of the difference between the IDs of the two commuters,
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
