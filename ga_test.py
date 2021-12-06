import pygad
import numpy
import random
from subprocess import Popen

speeds = random.sample(range(30, 121), 20)
friction = random.sample(range(0, 21), 20)
traffic = random.sample(range(5, 51), 20)

function_inputs = [4, -2, 3.5, 5, -11, -4.7]
desired_output = 44


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


def fitness_func(solution, solution_idx):
    status = 1
    while(status != 0):
        print("started simulation")
        # TODO: write parameters to an xml file as scenario
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
                "50",  # TODO: replace with GA solution
                "--behavior",
                "custom",
                "--xodr-path",
                "../maps/bahrain_international_circuit.xodr",
                "--number-of-vehicles",
                "30",  # TODO: replace with GA solution
                "--weather",
                choose_weather(0)  # TODO: replace with GA solution
            ], cwd="examples"
        )
        status = p2.wait()
        print("finished simulation with status code " + str(status))
    output = 0  # TODO: run carla and get collisions
    fitness = 1.0 * output  # TODO: calculate fitness based on the output
    return fitness


ga_instance = pygad.GA(
    num_generations=100,
    num_parents_mating=4,
    fitness_func=fitness_func,
    sol_per_pop=8,
    num_genes=6,
    init_range_low=-2,
    init_range_high=5,
    gene_type=float,
    mutation_num_genes=1
)

ga_instance.run()
ga_instance.plot_fitness()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(
    solution_fitness=solution_fitness))

prediction = numpy.sum(numpy.array(function_inputs)*solution)
print("Predicted output based on the best solution : {prediction}".format(
    prediction=prediction))
