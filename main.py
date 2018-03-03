#!/usr/bin/env python

import TransportManagement as tm

# Setup
simulation = tm.TransportManagement(
            max_t=60*3,
            delta_t=5,
            p_inspector=0.1,
            p_bus_advancement=0.75,
            initial_actors=10,
            initial_buses=2,
            spawn_delay=10,
            commuters_rage_threshold=10,
            spawn_new_bus_threshold=5
)

print("Welcome to the Commuter simulation. Here's the current situation: " + simulation.status_table())

not_stopped = True
while not_stopped:
    simulation.process_turn()
    simulation.print_status()
    simulation.step_forward()

    # Get user input
    user_choice = raw_input("\nHit Return to continue, anything else to quit: ")
    if user_choice:
        not_stopped = False
        print("Even if you decided to close this Matrix, there's no guarantee you aren't trapped in a higher level "
              "simulation."
              "\nTake care...")
    else:
        # See if the simulation has ended
        not_stopped = simulation.simulation_on

print("End of Commuter simulation.")