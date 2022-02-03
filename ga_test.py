import datetime
import time
import pygad
import subprocess as sp
import signal

gene_space = [{'low': 30, 'high': 121}, {'low': 4, 'high': 5},
              {'low': 0, 'high': 51}, {'low': 1, 'high': 22}]
initial_population = None
population_num = 0
label = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
with open(f"scenarios_{label}.csv", "a", encoding="utf8") as file:
    file.write('speed,map,traffic,weather,fitness\n')


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
        1: "2.5,-662.5,3,83.8",
        2: "998,-7,3,-171.2",
        3: "586.5,-1250.3,3,27.6",
        4: "948.8,-993.8,3,-157.4"
    }
    return switcher.get(index, "669.7,-92.7,3,242")


def chosen_map_end_point(index):
    switcher = {
        0: "1044.9,-1741.3,3",
        1: "0,0,3",
        2: "0,0,3",
        3: "0,0,3",
        4: "1016.4,-989,3"
    }
    return switcher.get(index, "670,-92,3")


def choose_weather(index):
    switcher = {
        1: "ClearNoon",
        2: "CloudyNoon",
        3: "ClearSunset",
        4: "CloudySunset",
        5: "WetNoon",
        6: "ClearNight",
        7: "CloudyNight",
        8: "WetCloudyNoon",
        9: "WetSunset",
        10: "WetCloudySunset",
        11: "SoftRainNoon",
        12: "WetNight",
        13: "SoftRainSunset",
        14: "MidRainyNoon",
        15: "WetCloudyNight",
        16: "HardRainNoon",
        17: "MidRainSunset",
        18: "SoftRainNight",
        19: "HardRainSunset",
        20: "MidRainyNight",
        21: "HardRainNight",
    }
    return switcher.get(index, "Default")


def vehicle_light_status(index):
    if index in [6, 7, 12, 15, 18, 20, 21]:
        return "--car-lights-on"
    else:
        return ""


def fitness_func(solution, solution_idx):
    status = -1
    while(status == -1):
        print("started simulation")
        try:
            cmd = [
                "python",
                "control_vehicle.py",
                "--sync",
                "--filter",
                "vehicle.tesla.model3",
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
            ]
            print(' '.join(cmd))
            p = sp.Popen(' '.join(cmd), cwd="examples", start_new_session=True,
                         shell=True, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
            status = p.wait(timeout=150)
        except sp.TimeoutExpired:
            p.send_signal(signal.CTRL_BREAK_EVENT)
            time.sleep(5)
            status = p.poll()
        print("\033[2;31;40mfinished simulation with status code " +
              str(status) + "\033[0;0m")
        with open(f"scenarios_{label}.csv", "a", encoding="utf8") as file:
            file.write('%s,%s,%s,%s,%s\n' % (str(solution[0]), str(
                solution[1]), str(solution[2]), str(solution[3]), str(status)))
    fitness = status
    return fitness


def on_fitness(ga_instance, population_fitness):
    global population_num
    with open("populations.csv", "a", encoding="utf8") as file:
        file.write('%s,%s,%s\n' % (population_num,
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
