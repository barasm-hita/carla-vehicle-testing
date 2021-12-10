import os
import pygad
import random
from subprocess import Popen, TimeoutExpired
import signal

gene_space = [{'low': 30, 'high': 121}, {'low': 0, 'high': 1},
              {'low': 0, 'high': 51}, {'low': 0, 'high': 22}]
initial_population = None
population_num = 0


def choose_map(index):
    switcher = {
        0: "bahrain_international_circuit",
        1: "indianapolis_motor_speedway",
        2: "motorsport_arena_oschersleben",
        3: "shanghai_international_circuit",
        4: "suzuka_circuit"
    }
    return switcher.get(index, "bahrain_international_circuit")


def chosen_map_start_point(index):
    switcher = {
        0: "669.7,-92.7,3,242",
        1: "0,0,3,0",
        2: "0,0,3,0",
        3: "0,0,3,0",
        4: "0,0,3,0"
    }
    return switcher.get(index, "669.7,-92.7,3,242")


def chosen_map_end_point(index):
    switcher = {
        0: "1044.9,-1741.3,3",
        1: "0,0,3",
        2: "0,0,3",
        3: "0,0,3",
        4: "0,0,3"
    }
    return switcher.get(index, "670,-92,3")


def choose_weather(index):
    switcher = {
        1: "ClearNight",
        2: "ClearNoon",
        3: "ClearSunset",
        4: "CloudyNight",
        5: "CloudyNoon",
        6: "CloudySunset",
        7: "HardRainNight",
        8: "HardRainNoon",
        9: "HardRainSunset",
        10: "MidRainSunset",
        11: "MidRainyNight",
        12: "MidRainyNoon",
        13: "SoftRainNight",
        14: "SoftRainNoon",
        15: "SoftRainSunset",
        16: "WetCloudyNight",
        17: "WetCloudyNoon",
        18: "WetCloudySunset",
        19: "WetNight",
        20: "WetNoon",
        21: "WetSunset"
    }
    return switcher.get(index, "Default")


def vehicle_light_status(index):
    switcher = {
        1 or 4 or 7 or 11 or 13 or 16 or 19: "--car-lights-on",
    }
    return switcher.get(index, "")


def fitness_func(solution, solution_idx):
    status = -1
    while(status != -1):
        print("started simulation")
        try:
            p = Popen(
                [
                    "python",
                    "control_vehicle.py",
                    "--sync",
                    "--filter",
                    "vehicle.lincoln.mkz_2020",
                    "--speed",
                    str(solution[0]),
                    "--behavior",
                    "custom",
                    "--xodr-path",
                    "../maps/{chosen_map}.xodr".format(
                        chosen_map=choose_map(solution[1])),
                    "--number-of-vehicles",
                    str(solution[2]),
                    "--weather",
                    choose_weather(solution[3]),
                    vehicle_light_status(solution[3]),
                    "--start",
                    chosen_map_start_point(solution[1]),
                    "--end",
                    chosen_map_end_point(solution[1])
                ], cwd="examples", start_new_session=True
            )
            status = p.wait(timeout=300)
        except TimeoutExpired:
            status = -1
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        print("finished simulation with status code " + str(status))
    # TODO: write parameters to an xml file as scenario
    fitness = random.randint(1, 10)  # TODO: run carla and get score
    return fitness


def on_fitness(ga_instance, population_fitness):
    global population_num
    with open("populations.csv", "a", encoding="utf8") as file:
        file.write('%r,%r,%r\n' % (population_num,
                   str(ga_instance.population), str(population_fitness)))
    population_num += 1


ga_instance = pygad.GA(
    num_generations=10,
    num_parents_mating=4,
    fitness_func=fitness_func,
    sol_per_pop=8,
    num_genes=4,
    init_range_low=-2,
    init_range_high=5,
    gene_type=int,
    mutation_num_genes=1,
    gene_space=gene_space,
    initial_population=initial_population,
    on_fitness=on_fitness
)


ga_instance.run()
ga_instance.plot_fitness()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(
    solution_fitness=solution_fitness))
