import pygad
import random
from subprocess import Popen

gene_space = [{'low': 30, 'high': 121}, {'low': 0, 'high': 5},
              {'low': 0, 'high': 51}, {'low': 0, 'high': 22}]
initial_population = None


def choose_map(index):
    switcher = {
        0: "bahrain_international_circuit",
        1: "indianapolis_motor_speedway",
        2: "motorsport_arena_oschersleben",
        3: "shanghai_international_circuit",
        4: "suzuka_circuit"
    }
    return switcher.get(index, "bahrain_international_circuit")


def choose_weather(index):
    switcher = {
        1: "ClearNight --car-lights-on",
        2: "ClearNoon",
        3: "ClearSunset",
        4: "CloudyNight --car-lights-on",
        5: "CloudyNoon",
        6: "CloudySunset",
        7: "HardRainNight --car-lights-on",
        8: "HardRainNoon",
        9: "HardRainSunset",
        10: "MidRainSunset",
        11: "MidRainyNight --car-lights-on",
        12: "MidRainyNoon",
        13: "SoftRainNight --car-lights-on",
        14: "SoftRainNoon",
        15: "SoftRainSunset",
        16: "WetCloudyNight --car-lights-on",
        17: "WetCloudyNoon",
        18: "WetCloudySunset",
        19: "WetNight --car-lights-on",
        20: "WetNoon",
        21: "WetSunset"
    }
    return switcher.get(index, "Default")


def fitness_func(solution, solution_idx):
    status = 1
    while(status != 0):
        print("started simulation")
        # _ = Popen(
        #     [
        #         "python",
        #         "scenario_runner.py",
        #         "--scenario",
        #         "bahrain_international_circuit"
        #     ], cwd="scenario_runner"
        # )
        # p2 = Popen(
        #     [
        #         "python",
        #         "manual_control.py",
        #         "-a"
        #     ], cwd="scenario_runner"
        # )
        p2 = Popen(
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
                choose_weather(solution[3])
            ], cwd="examples"
        )
        status = p2.wait(300)  # timeout after 300 seconds
        print("finished simulation with status code " + str(status))
    # TODO: write parameters to an xml file as scenario
    fitness = random.randint(1, 10)  # TODO: run carla and get score
    return fitness


def on_generation(ga_instance):
    print(ga_instance)


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
    on_generation=on_generation
)

print(ga_instance.population)

ga_instance.run()
ga_instance.plot_fitness()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(
    solution_fitness=solution_fitness))
