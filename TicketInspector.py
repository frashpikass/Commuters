from Commuter import Commuter
import random as r


class TicketInspector(Commuter):
    EVIL_NAMES = ("Gargamel", "Mangiafuoco", "Vlad", "Leech", "Frieza", "Koopa", "Goomba", "De Sade",
                  "Darth Maul", "Blank Banshee")
    MAX_WORKTIME = 60
    MAX_IDLE_TIME = 30

    def __init__(self):
        super(TicketInspector, self).__init__()
        self.has_ticket = True
        self.name = self.generate_name()
        self.mark = "T"

        self.p_female_trickster_expulsion = r.random()
        self.p_male_trickster_expulsion = r.random()

        self.time_no_violation = 0

    def generate_name(self):
        """
        Generate a new name for this ticket inspector
        :return: a new name for this ticket inspector
        """
        return TicketInspector.EVIL_NAMES[r.randrange(len(TicketInspector.EVIL_NAMES))]

    def possessive_adjective(self):
        """
        Generates the correct possessive adjective for this Commuter
        :return: the possessive adjective string
        """
        return "their evil"

    def wants_to_drop(self):
        """
        A ticket inspector wants to drop from the bus if he travelled for MAX_WORKTIME or if they didn't find tricksters
        for more than MAX_IDLE_TIME
        :return: the intention to drop from the bus
        """
        return self.travel_time >= TicketInspector.MAX_WORKTIME \
               or self.time_no_violation >= TicketInspector.MAX_IDLE_TIME

    def expel_passenger(self, passenger):
        """
        Evaluates a passenger to decide whether it should be expelled from the bus
        :param passenger: the passenger to evaluate
        :return: True if the passenger doesn't have a valid ticket and is expelled
        """
        if not passenger.has_ticket:
            if passenger.mark == "M":
                return r.random() < self.p_male_trickster_expulsion
            if passenger.mark == "F":
                return r.random() < self.p_female_trickster_expulsion
        return False
