Documentation for laser_calibration package
=====

Introduction
-------
The main concept for the laser_calibration package is to provide a framework for moving mirror, storing mirror position, and obtaining ion response, so that the user can build customized optimization calibration routine. The key modules are Mirror and LaserCalibrationSystem modules. The package also provides a built-in grid_sweep_optimize and generic_optimize functions. Simulation mode is also provided, which can provide realistic simulation of ion response that takes into account of photon shot noise. 

Examples can be found in \examples\. Unit tests are found in \tests\. 

Improvements I envision, if I have more time, include:

- more sophisticated optimization algorithm, such as Bayesian optimization
- tracking mode, where the system will measure a response, and move in small steps and follow the gradient of response for steepest ascent. This is similar to the existing generic_optimize, which makes use of scipy's Optimize routine; however, the Optimize routine is not robust against present of noise (whether instrument or photon shot noise), so a custom routine needs to be built, which will be for a future effort.
- more comprehensive documentation. Due to time constraint, here I document the key functionalities. 


Mirror module
-------

The mirror module provides a class for controlling and storing mirror position. The ability to cache (store) the last position mirror is set to allows the ability to do tracking (this functionality is not built out in the current iteration), as well as necessary for simulation.

To import, run

    from laser_calibration.mirror import Mirror

To initiate a mirror instance, run

    mirror = Mirror(move_mirror_function)

where move_mirror_function is the function handle for moving mirror position. In simulation mode, one can simply do 

    mirror = Mirror()

Position can be obtained/set using the position property. E.g.

    mirror.position = 0.1

Will set mirror to position 0.1. Mirror position can be between -1 to 1. Running

    mirror.position

Will then return 0.1, the last mirror position.

LaserCalibrationSystem module
-------
This is the center piece of the codebase. An instance of LaserCalibrationSystem involves a set of Mirror instances, and an ion_response_function that measures the response from ions (number of photons). 

To import, run

    from laser_calibration.laser_calibration_system import LaserCalibrationSystem

To initiate, you must provide an ion_response_function. This would be the function that shoots the laser and measure number of photons. For simulation, see examples such as \examples\simulatiON-laser_calibration_system.2d.py.

To initiate run,

     syst = LaserCalibrationSystem(ion_response_function)


You will then want to add mirror. You need to provide a name, and a mirror instance or mirror movement function ``mirror1``:

    syst.add_mirror("mirror_name_1", mirror1)

If you provide a mirror movement function, a mirror instance will be created.

For working with real instruments, the ion_response_function needs to be a function that takes no argument. To use simulation mode, one needs provide ion_response_function that takes N number of arguments which correspond to position of mirrors. Furthermore, two additional commands need to be run. First, the simulation property needs to be set to be True:

        syst.simulation = True

Second, one needs to indicate which mirror correspond to which axis, in the form of list. E.g. to set "mirror_1" to be the first axis and "mirror_2" to be the second axis, one runs

    syst.simulation_mirror_set = ["mirror_1", "mirror_2"]


To get all the mirrors, run

    syst.get_all_mirror_names()

This will return a list of all the strings of mirror names.

To move mirrors and measure ion response, here is an example code

    syst.move_mirrors_and_measure(**{"mirror_name_1": 0.1, "mirror_name_2": -0.2})

Or 
    syst.move_mirrors_and_measure(mirror_name_1 = 0.1, mirror_name_2 = -0.2)

With this function, one can build up customized optimization algorithm.


grid_sweep_optimize function
-------
This is a built-in 
