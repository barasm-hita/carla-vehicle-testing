# CARLA Vehicle Testing

**[CARLA](https://github.com/carla-simulator/carla "CARLA") is an open source simulator for every researcher in autonomous vehicles field.**

Some may go on with autonomous features and algorithms, or may go around development and testing CARLA itself. In this repo my purpose is testing CARLA simulators vehicle control using its own autonomous features.

### Requirements
------------
First go to CARLA [official repo](https://github.com/carla-simulator/carla "CARLA") and check hardware requirements to meet yours.

Then, you have to ready up the prerequisite as below:
- CARLA Simulation Server v0.9.12 (Get it [here](https://github.com/carla-simulator/carla/releases/tag/0.9.12 "CARLA Release 0.9.12"))
- Python v3.7
- Installation of pip packages from the [requirements.txt](https://github.com/barasm-hita/carla-vehicle-testing/blob/main/requirements.txt "requirements.txt")

### How to use
------------
If you take a look at downloaded CARLA server, you will find a directory named **PythonAPI**. This folder contains several python scripts that have various purposes.

In my project, **control_vehicle.py** is the main script that is very similar to the [automatic_control.py](https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/automatic_control.py "automatic_control.py") script under examples/PythonAPI, but mine is more complicated and has more options to use in the way of this project.
To find out about options and their values, use **`python control_vehicle.py --help`** in the command-line.

**Notice:** Scripts of agents folder in this project have been copied from CARLA official repo, but they **contain some customizations**. So, if you want to use this project beside other examples of CARLA PythonAPI directory, **replace** the customized agents folder with the official one. It **will not damage** any official script routine.

### License
------------
This project has been distributed under MIT license.