laser_calibration package
========================
Getting started
-------

This package provides code for laser calibration system. 

To install: at the home folder, run: ``pip install .`` or ``pip install -e .`` for editable install.

Detailed documentation is found in the subsequent sections.

To see examples, go to ``\examples\`` and run the scripts in that folder, e.g. ``python simulation_grid_optimization_1d.py``. Note that if one wants to see plot, one needs to use, for example, Spyder or vscode to run them in order to display the plots. 

To run unit test, go to ``\tests\`` and run ``python test.py``.

Introduction
-------
The main concept for the ``laser_calibration`` package is to provide a framework for moving mirror, storing mirror position, and obtaining ion response, so that the user can build customized optimization calibration routine. The key modules are ``Mirror`` and ``LaserCalibrationSystem`` classes. The package also provides a built-in ``grid_sweep_optimize`` and ``generic_optimize`` functions. Simulation mode is also provided, with a generic ``IonResponseSimulation`` class and a ``GaussianIonResponseSimulation`` class, which can provide realistic simulation of ion response that takes into account of photon shot noise. 

Examples can be found in ``\examples\``.

Improvements I envision, if I have more time, include:

- currently, calibration over two-dimensional mirror movement is supported. General N-dimensional calibration should be readily feasible, with small changes to the codebase, which is for future effort.
- Integrate some kind of asynchronous operation for setting multiple mirrors in parallel
- more sophisticated optimization algorithm, such as Bayesian optimization
- tracking mode, where the system will measure a response, and move in small steps and follow the gradient of response for steepest ascent. This is similar to the existing ``generic_optimize``, which makes use of ``scipy``'s ``optimize`` module; however, the ``optimize`` routine is not robust against presence of noise (whether instrument or photon shot noise), so a custom routine needs to be built, which will be for a future effort.
- more comprehensive documentation. Due to time constraint, here I document the key functionalities. 


Mirror class
-------

The ``Mirror`` class provides a class for controlling and storing mirror position. The ability to cache (store) the last position mirror is set to allows the ability to do tracking (this functionality is not built out in the current iteration), as well as necessary for simulation.

To import, run::

    from laser_calibration.mirror import Mirror

To initiate a mirror instance, run::

    mirror = Mirror(move_mirror_function)

where ``move_mirror_function`` is the function handle for moving mirror position. In simulation mode, one needs not supply this function, and to instantiate a ``Mirror`` object, can simply do::

    mirror = Mirror()

Position can be obtained/set using the ``position`` property. E.g.::

    mirror.position = 0.1

Will set mirror to position 0.1. Mirror position can be between -1 to 1. Subsequently, running::

    mirror.position

In this case will return the value ``0.1``, the last mirror position.

LaserCalibrationSystem class
-------
This is the center piece of the codebase. An instance of `LaserCalibrationSystem` involves a set of ``Mirror`` instances, and an ``ion_response_function`` that measures the response from ions (number of photons). 

To import, run::

    from laser_calibration.laser_calibration_system import LaserCalibrationSystem

To initiate, you must provide an ``ion_response_function``. This would be the function that shoots the laser and measure number of photons. 

To initiate run::

     syst = LaserCalibrationSystem(ion_response_function)


You will then want to add mirror. You need to provide a name, and a mirror instance or mirror movement function ``mirror1``::

    syst.add_mirror("mirror_name_1", mirror1)

If you provide a mirror movement function, a mirror instance will be created.

For working with real instruments, the ``ion_response_function`` needs to be a function that takes no argument. To use simulation mode, one needs provide ``ion_response_function`` that takes N number of arguments which correspond to position of mirrors. Furthermore, two additional commands need to be run. First, the simulation property needs to be set to be True::

        syst.simulation = True

Second, one needs to indicate which mirror correspond to which axis, in the form of list. E.g. to set `"mirror_1"` to be the first axis and `"mirror_2"` to be the second axis, one runs::

    syst.simulation_mirror_set = ["mirror_1", "mirror_2"]

All the examples in ``\examples\`` make use of simulation mode; one can see concrete example of how to use simulation in these examples.

To get all the mirrors, run::

    syst.get_all_mirror_names()

This will return a list of all the strings of mirror names.

With a LaserCalibrationSystem instantiated such as the one above, to move mirrors and measure ion response, one would run command such as the one below::

    syst.move_mirrors_and_measure(mirror_name_1 = 0.1, mirror_name_2 = -0.2)

This will move the mirror with the name ``"mirror_name_1"`` to position ``0.1``, and move the mirror with the name ``"mirror_name_2"`` to position ``-0.1``,

With this function, one can build up customized optimization algorithm.


IonResponseSimulation and GaussianIonResponseSimulation
-------
These are two built-in classes for providing simulated ion response. The ``IonResponseSimulation`` allows for generating generic spatial distribution of photon count. To import, one runs::

    from laser_calibration.ion_response_simulation import IonResponseSimulation

Then::

    sim = IonResponseSimulation(photon_distribution,use_poisson_distribution,measurement_noise)

Here, ``photon_distribution`` is a function that takes two arguments, ``x`` and ``y``, and return the average photon number. ``use_poisson_distribution`` is boolean, and tells ``IonResponseSimulation`` whether to generate photon count using Poisson distribution or simply the value from ``photon_distribution`` function. ``measurement_noise`` is a ``float`` that indicates noise level from instrument. 

Based on ``IonResponseSimulation``, I also provide ``GaussianIonResponseSimulation`` which essentially uses a Gaussian distribution for ``photon_distribution``. Therefore, in setting up  ``GaussianIonResponseSimulation``, instead of supplying a function, one supplies parameters of the Gaussian distribution.

To import::

    from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation

The one runs the command such as below::

    sim = GaussianIonResponseSimulation(photon_number=100,x_center=0.1,y_center=0.2,x_width=0.3,y_width=0.4)

This will setup `sim` as a function that generates a Gaussian profile with specified parameters. 

grid_sweep_optimize function
-------
This is a built-in calibration routine where up to 2 mirror-dimensions (generic N-dimension can be readily implemented as future effort) will be swept, with photon number recorded at each ``(x,y)`` location, and the photon number distribution ``n(x,y)`` is fitted to 1 or 2D Gaussian, and the center of the distribution is the location where the mirrors are set to.

To import, run::

    from laser_calibration.grid_sweep_optimize import grid_sweep_optimize

To use, simply run::

    grid_sweep_optimize(syst)

Where ``syst`` is a ``LaserCalibrationSystem`` instance. 

Additional options exist; see the docstrings of the function.

generic_optimize function
-------
This is a built-in calibration routine where ``scipy``'s ``optimize`` module to optimize the photon number over up to 2 mirror-dimensions (generic N-dimension can be readily implemented as future effort). More specifically, the ``minimize`` function of ``optimize`` will be used to minimize the negative of the photon number (equivalent to maximizing photon number). This routine is purely for proof-of-principle purpose; during testing, it is found that it is not robust in the presence of any noise, including photon shot noise. Therefore, to use this, one has to use a noise-less photon distribution (without photon shot noise), which is not physical. Nevertheless, this function demonstrates the architecture for using a generic optimization routine for calibration. 

To import, run::

    from laser_calibration.generic_optimize import generic_optimize

To use, simply run::

    generic_optimize(syst)

Where ``syst`` is a ``LaserCalibrationSystem`` instance. 

Additional options exist; see the docstrings of the function.




