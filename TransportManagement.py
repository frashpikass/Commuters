from prettytable import PrettyTable
import random as R
import Locations
import Commuter as C
import TicketInspector as T
import Bus as B

# Default values
P_INSPECTOR = 0.1
P_BUS_ADVANCEMENT = 0.95
INITIAL_ACTORS = 5
INITIAL_BUSES = 2
DELTA_T = 5
MAX_T = 60 * 3
SPAWN_DELAY = 10
COMMUTERS_RAGE_THRESHOLD = 10
SPAWN_NEW_BUS_THRESHOLD = 5


class TransportManagement(object):
    def __init__(
            self,
            max_t=MAX_T,
            delta_t=DELTA_T,
            p_inspector=P_INSPECTOR,
            p_bus_advancement=P_BUS_ADVANCEMENT,
            initial_actors=INITIAL_ACTORS,
            initial_buses=INITIAL_BUSES,
            spawn_delay=SPAWN_DELAY,
            commuters_rage_threshold=COMMUTERS_RAGE_THRESHOLD,
            spawn_new_bus_threshold=SPAWN_NEW_BUS_THRESHOLD
    ):
        """
        Constructor and setup method
        :param max_t: maximum simulation time (in time units)
        :param delta_t: number of time units for each simulation step
        :param p_inspector: probability of a new actor to be a ticket inspector
        :param p_bus_advancement: probability of a bus advancing to the next stop at each new turn
        :param initial_actors: number of initial actors
        :param initial_buses: number of initial buses
        :param spawn_delay: delay in time units between actor spawn events
        :param commuters_rage_threshold: number of commuters on a bus to start a riot
        :param spawn_new_bus_threshold: number of commuters at a bus stop to spawn a new bus
        """
        # Simulation constants
        self.max_t = max_t
        self.delta_t = delta_t
        self.p_inspector = p_inspector
        self.p_bus_advancement = p_bus_advancement
        self.initial_actors = initial_actors
        self.initial_buses = initial_buses
        self.spawn_delay = spawn_delay
        self.commuters_rage_threshold = commuters_rage_threshold
        self.spawn_new_bus_threshold = spawn_new_bus_threshold

        # Private variables
        self.global_time = 0
        self.last_spawn_time = 0
        self.actors = list()
        self.buses = list()
        self.event_strings = list()

        # Setup: spawn initial actors (Commuters and Inspectors)
        for i in range(self.initial_actors):
            self.spawn_actor()

        # Setup: spawn initial buses
        bus_starting_points = R.sample(Locations.LOCATIONS, self.initial_buses)
        for place in bus_starting_points:
            self.spawn_bus(place)

        # Setup: turn on simulation
        self.simulation_on = True

    # Method to create a new actor
    def spawn_actor(self):
        # type: () -> str
        """
        Create a new actor, which can be a Commuter or a Ticket Inspector
        :return the event string
        """

        event_string = "It was {time} o'clock when ".format(time=self.global_time)

        if R.random() > self.p_inspector:
            new_actor = C.Commuter()
            event_string = event_string \
                           + "{name} ({id}) walked up to the stop of {place} and started to wait for {poss} ride." \
                               .format(name=new_actor.name, id=new_actor.id, place=new_actor.hometown,
                                       poss=new_actor.possessive_adjective())
        else:
            new_actor = T.TicketInspector()
            event_string = event_string \
                           + "Ticket inspector {name} ({id}) marched up to the stop of {place} and started to wait for {poss} ride." \
                               .format(name=new_actor.name, id=new_actor.id, place=new_actor.hometown,
                                       poss=new_actor.possessive_adjective())

        self.actors.append(new_actor)
        self.last_spawn_time = self.global_time
        return event_string

    def spawn_bus(self, location):
        """
        Create a new bus, spawning it at the specified location
        :param location: the location where to spawn the new bus
        """
        self.buses.append(B.Bus(location, self.p_bus_advancement))

    def drop(self, bus, passengers_to_drop):
        """
        Drops all specified passengers from the bus and from the simulation too
        :type bus: B.Bus
        :type passengers_to_drop: list
        :param passengers_to_drop: the list of passengers to remove
        :param bus: the bus we need to remove the passengers from
        """
        bus.drop_all_passengers(passengers_to_drop)
        # Remove all dropped passengers from the simulation
        for passenger in passengers_to_drop:
            self.actors.remove(passenger)
        pass

    def destroy_bus(self, bus):
        """
        Destroys the specified bus, removing it and all of its passenger (Commuters) from the simulation
        :param bus: the bus to destroy
        """
        for passenger in bus:
            self.actors.remove(passenger)
        self.buses.remove(bus)

    def status_table(self):
        """
        Generates the table displaying information about actor and bus status
        :return: the table displaying information about actor and bus status
        """

        # Generate tables for actors and buses
        self.actors.sort()
        actors_table = PrettyTable()
        actors_table.field_names = ["Id", "Name", "Hometown", "Position", "Travel time", "Ticket", "Mark"]
        for a in self.actors:
            actors_table.add_row([a.id, a.name, a.hometown, a.position, a.travel_time, a.has_ticket, a.mark])

        self.buses.sort()
        buses_table = PrettyTable()
        buses_table.field_names = ["Id", "Last recorded position", "Is at a bus stop",
                                   "Passengers", "Tricksters", "Inspectors"]
        for b in self.buses:
            buses_table.add_row([b.id, b.last_position, b.is_at_bus_stop,
                                 len(b.passengers), len(b.get_tricksters()), len(b.get_inspectors())])

        out = "\nSITUATION AT TIME {}".format(self.global_time) + "\nActors:\n" + str(
            actors_table) + "\nBuses:\n" + str(buses_table)

        return out

    def print_status(self):
        """
        Prints the current status in a fancy text-adventure and tabular form
        """
        # Intro line
        print("\nBuses ran and ran, or rather crawled, over the jammed roads...")

        # Event lines
        for line in self.event_strings:
            print(line)

        print(self.status_table())

    def process_turn(self):
        """
        Analyzes the current situation and updates data structures.
        Also prepares the event_strings for display.
        """

        # Resetting event strings
        self.event_strings = list()

        # Eventually spawning a new actor
        if (self.global_time - self.last_spawn_time) >= self.spawn_delay:
            self.event_strings.append(self.spawn_actor())

        # Check if we have buses at a bus stop
        for bus in [b for b in self.buses if b.is_at_bus_stop]:
            self.event_strings.append(
                "\nAfter what felt like an eternity, bus {} made it to {}.".format(bus.id, bus.last_position)
            )

            # Check if the bus at the bus stop has reached the destination
            if bus.last_position is Locations.LOCATIONS[0]:
                if len(bus.passengers) > 0:
                    self.event_strings.append("The final stop looked like a mirage. "
                                              "Everyone felt relieved for a moment.")
                else:
                    self.event_strings.append("The final stop looked like a mirage. "
                                              "What a shame no passenger was there to see it.")

                # Drop all passengers on the bus, since we're at the base station
                passengers_to_drop = [p for p in bus if p.mark != "T"]
                self.drop(bus, passengers_to_drop)
                if len(passengers_to_drop) > 0:
                    self.event_strings.append(
                        "But happiness is vain for those who are now gloomily proceeding to walk to their "
                        "workplace:\n{} "
                            .format(str([(p.name, p.id) for p in passengers_to_drop]))
                    )

            else:  # If the bus is not at the destination, but it's at a bus stop
                # If there is an inspector on board, check for tricksters and try to jettison one of them
                if bus.has_inspector():
                    graced = 0
                    expelled = 0
                    for inspector in bus.get_inspectors():
                        for trickster in bus.get_tricksters():
                            if inspector.expel_passenger(trickster):
                                self.drop(bus, [trickster])
                                self.event_strings.append(
                                    "After a short quarrel, inspector"
                                    + " {} managed to fine and jettison trickster {} ({:d}) from bus {:d}."
                                    .format(inspector.name, trickster.name, trickster.id, bus.id)
                                    + "\nGood riddance!"
                                    + "\n(Also, the inspector seems to be satisfied and unwilling to check other "
                                      "passengers for now.)"
                                )
                                expelled = expelled + 1
                                break
                            else:
                                graced = graced + 1
                                self.event_strings.append(
                                    "{} ({:d}) on bus {:d} had no ticket, but inspector {} ({:d}) pretended not to notice."
                                        .format(trickster.name, trickster.id, bus.id, inspector.name, inspector.id)
                                )

                    if graced > 0 and expelled == 0:
                        self.event_strings.append("Sometimes fortune favours the brave, in this crazy world of ours.")
                    elif graced > 0 and expelled > 0:
                        self.event_strings.append("Some days you win, some days you lose."
                                                  + "\nBut when all is said and done, having no ticket is just a calculated risk.")

                # Collect new passengers from the bus stop
                to_collect = [p for p in self.actors if p.position is bus.last_position]
                bus.collect_all_passengers(to_collect)
                len_to_collect = len(to_collect)
                if len_to_collect > 1:
                    self.event_strings.append(
                        "{:d} lost souls were collected from the bus stop.".format(len_to_collect)
                    )
                elif len_to_collect == 1:
                    self.event_strings.append("One lost soul was collected from the bus stop.")

                # Tired passengers and inspectors who have finished their job should be dropped right away
                tired_passengers = [p for p in bus if p.wants_to_drop()]
                self.drop(bus, tired_passengers)
                if len(tired_passengers) > 0:
                    self.event_strings.append(
                        "{:d} passengers couldn't make it anymore, so they willingly left the bus. Let's wish them a good walk: {} "
                            .format(len(tired_passengers), str([p.id for p in tired_passengers]))
                    )

        # Commuters' Rage Event: too many commuters on a bus
        buses_to_destroy = list()
        for bus in self.buses:
            if len(bus.passengers) > self.commuters_rage_threshold:
                self.event_strings.append("\nBus {} was a little too overcrowded.".format(bus.id) +
                                          "\nThe {} passengers decided to go berserk and eventually destroy the bus."
                                          .format(len(bus.passengers)) +
                                          "\nLook at them, they've made a bonfire out of gasoline and bus chairs!"
                                          "\nAren't they lively? Don't you wish you were having fun with them?")
                buses_to_destroy.append(bus)
        for b in buses_to_destroy:
            self.destroy_bus(b)

        # Spawn new bus: too many commuters at a bus stop
        spawn_new_bus = False
        for bus_stop in Locations.LOCATIONS:
            if len([c for c in self.actors if (c.position == bus_stop)]) > self.spawn_new_bus_threshold:
                self.event_strings.append(
                    "\nThe main office of the Public Transportation System noticed from its security cameras\n"
                    "that the bus stop in {} was too crowded, so they decided to send a new bus from {} before anyone "
                    .format(bus_stop, Locations.LOCATIONS[0]) +
                    "got angry.\nAs if they weren't already..."
                )
                spawn_new_bus = True
                break
        if spawn_new_bus:
            self.spawn_bus(Locations.LOCATIONS[0])

    def step_forward(self):
        """
        Steps forward in the simulation: buses and global time will advance, actors will age by delta T.
        If the simulation has to stop, the self.simulation_on is set to False
        """

        # After dropping passengers and collecting new passengers, all buses must try to advance
        for bus in self.buses:
            bus.try_to_advance()

        # Increase simulation time
        self.global_time = self.global_time + self.delta_t
        # Age actors
        for a in self.actors:
            a.age(self.delta_t)

        # Check if the simulation has to continue or not
        if self.global_time > self.max_t:
            print("Timeout!\nIf you're not at your office desk by now, "
                  "you have won a free ride to the \"job market (TM)\". Congratulations!")
            self.simulation_on = False

        if len([c for c in self.actors if (c.mark != "T")]) == 0:
            print("It appears that all the workers are producing GDP right now."
                  "\nAnother incredible success story for Public Transportation!"
                  "\n(This is _so_ going to be on all papers tomorrow!)")
            self.simulation_on = False
