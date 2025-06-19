laser_calibration package
========================
Getting started
-------

This package provides code for laser calibration system. 

To install: at the home folder, run: ``pip install .`` or ``pip install -e .`` for editable install.

Detailed documentation is found in the subsequent sections.

To see examples, go to ``\examples\`` and run the scripts in that folder, e.g. ``python simulation_grid_optimization_2d.py``, ``python simulation_grid_optimization_1d.py`` , or ``python simulation_grid_optimization_ND.py``. These three are the primary examples that showcase the calibration functionality of this package; additional examples are also supplied. Note that if one wants to see plot, one needs to use, for example, Spyder or vscode to run them in order to display the plots. 

To run unit test, go to ``\tests\`` and run ``python -m unittest test.py``.

Introduction
-------
The main concept for the ``laser_calibration`` package is to provide a framework for moving mirror, storing mirror position, and obtaining ion response, so that the user can build customized optimization calibration routine. The key modules are ``Mirror`` and ``LaserCalibrationSystem`` classes. The package also provides a built-in ``grid_sweep_optimize``, ``grid_sweep_optimize_ND``, and ``generic_optimize`` functions. Simulation mode is also provided, with a generic ``IonResponseSimulation`` class and a ``GaussianIonResponseSimulation`` class, which can provide realistic simulation of ion response that takes into account of photon shot noise. 

Here are key assumptions in building this package:

- Mirror control function and ion response function is available from elsewhere. For simulation purpose, mirror control function is not needed, and I provide a framework for generating simulated ion response. 
- Mirror position can be -1 to 1. It is not necessarily an absolute unit, but rather a relative range
- Multiple sets of mirror systems may need to be calibrated in the same setting, and possibly the different sets of mirror systems may contain same mirrors. As a result, I provide LaserCalibrationSystem class to which one can add arbitrary sets of mirrors.
- Goal of calibration is to maximize intensity of ion response. Therefore, calibration routines will be built out as optimization routine. 
- Calibration routine provided in this package assumes a single ion present in the range of the mirror movement.
- Gaussian distribution is a good approximation of the intensity distribution of ion response. While Airy function should be a better approximation of the point-spread-function, Gaussian is a good model in experimental setting.  This is the basis for the ``grid_sweep_optimize`` and ``grid_sweep_optimize_ND``'s fitting the photon number distribution to Gaussian (using ``scipy``'s ``curve_fit`` function).

Two major questions are the following: 

- How to deal with failure mode? For example, in the case where there is actually no ion in the system, how should the code respond? Or, if photon number is too low or point-spread-function is too narrow, how should the code respond? Should the code simply exit? Should it attempt at another set of parameters? These would be important questions to clarify.
- What is the precision needed for the calibration to be considered to be successful? 

Improvements I envision, if I have more time, include:

- In the case of grid optimization followed by Gaussian fit, astigmatism (unequal width in x, y axes etc) are included, but not rotation. Rotation can be implemented with an additional parameter in the Gaussian.
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

To initiate, run::

     syst = LaserCalibrationSystem(ion_response_function)


You will then want to add mirror. You need to provide a name, and a mirror instance or mirror movement function ``mirror1``::

    syst.add_mirror("mirror_name_1", mirror1)

If you provide a mirror movement function, a mirror instance will be created.

For working with real instruments, the ``ion_response_function`` needs to be a function that takes no argument. To use simulation mode, one needs provide ``ion_response_function`` that takes N number of arguments which correspond to position of mirrors. Furthermore, two additional commands need to be run. First, the simulation property needs to be set to be ``True``::

        syst.simulation = True

Second, one needs to indicate which mirror correspond to which axis, in the form of list. E.g. to set `"mirror_1"` to be the first axis and `"mirror_2"` to be the second axis, one runs::

    syst.simulation_mirror_set = ["mirror_1", "mirror_2"]

All the examples in ``\examples\`` make use of simulation mode; one can see concrete example of how to use simulation in these examples.

To get all the mirrors, run::

    syst.get_all_mirror_names()

This will return a list of all the strings of mirror names.

With a ``LaserCalibrationSystem`` instantiated such as the one above, to move mirrors and measure ion response, one would run command such as the one below::

    syst.move_mirrors_and_measure(mirror_name_1 = 0.1, mirror_name_2 = -0.2)

This will move the mirror with the name ``"mirror_name_1"`` to position ``0.1``, and move the mirror with the name ``"mirror_name_2"`` to position ``-0.1``,

With this function, one can build up customized optimization algorithm.


IonResponseSimulation and GaussianIonResponseSimulation
-------
These are two built-in classes for providing simulated ion response. The ``IonResponseSimulation`` allows for generating generic spatial distribution of photon count. To import, one runs::

    from laser_calibration.ion_response_simulation import IonResponseSimulation

Then::

    sim = IonResponseSimulation(photon_distribution,use_poisson_distribution,measurement_noise)

Here, ``photon_distribution`` is a function that takes n-dimensional arguments corresponding to point in space, and return the average photon number. ``use_poisson_distribution`` is boolean, and tells ``IonResponseSimulation`` whether to generate photon count using Poisson distribution or simply the value from ``photon_distribution`` function. ``measurement_noise`` is a ``float`` that indicates noise level from instrument. 

Based on ``IonResponseSimulation``, I also provide ``GaussianIonResponseSimulation`` which essentially uses a 2D Gaussian distribution for ``photon_distribution``. Therefore, in setting up  ``GaussianIonResponseSimulation``, instead of supplying a function, one supplies parameters of the Gaussian distribution.

To import::

    from laser_calibration.ion_response_simulation import GaussianIonResponseSimulation

The one runs the command such as below::

    sim = GaussianIonResponseSimulation(photon_number=100,x_center=0.1,y_center=0.2,x_width=0.3,y_width=0.4)

This will setup `sim` as a function that generates a Gaussian profile with specified parameters. 

grid_sweep_optimize function
-------
This is one of the two primary calibration routines provided by this package, where up to 2 mirror-dimensions will be swept, with photon number recorded at each ``(x,y)`` location, and the photon number distribution ``n(x,y)`` is fitted to 1 or 2D Gaussian, and the center of the distribution is the location where the mirrors are set to.

This essentially has the same functionality as ``grid_sweep_optimize_ND`` (see below), except that this function has plotting capability.

The sweep range is fixed to be over the entire mirror range, -1 to 1. This is intentional. Without further information on the setup and how to use the code, I assume we want a more or less automatic algorithm. With more information on the use-case of the code, an implementation of the sweep range as user-supplied arguments would be appropriate. 

The user can supply ``step``, which is the step size of the sweep. The actual value swept is set by ``numpy``'s ``arange`` function.

The initial guesses for center and width are determined using the first (center-of-mass) and second moments, which provide very accurate guess as long as the response distribution is well-approximated by Gaussian and signal-to-noise is decent.

To import, run::

    from laser_calibration.grid_sweep_optimize import grid_sweep_optimize

To use, simply run::

    grid_sweep_optimize(syst)

Where ``syst`` is a ``LaserCalibrationSystem`` instance. 

Additional options exist; see the docstrings of the function.

grid_sweep_optimize_ND function
-------
This is the other primary calibration routine provided by this package. It is essentially the same as the ``grid_sweep_optimize`` function, but able to handle generic n-th dimensional space (and with no plotting). 

The sweep range and step can be set, see the doc-string of the function on how to use it. If these arguments are not provided, default range (-1 to 1) and step size (0.1) is used for all dimensions.
The actual value swept is set by ``numpy``'s ``arange`` function.

The initial guesses for center and width are determined using the first (center-of-mass) and second moments, which provide very accurate guess as long as the response distribution is well-approximated by Gaussian and signal-to-noise is decent.

To import, run::

    from laser_calibration.grid_sweep_optimize_ND import grid_sweep_optimize_ND



generic_optimize function
-------
This is a built-in calibration routine, not currently intended for actual usage but is included as a proof-of-principle. In this calibration routine, ``scipy``'s ``optimize`` module to optimize the photon number over up to 2 mirror-dimensions (generic N-dimension can be readily implemented as future effort). More specifically, the ``minimize`` function of ``optimize`` will be used to minimize the negative of the photon number (equivalent to maximizing photon number). This routine is purely for proof-of-principle purpose; during testing, it is found that it is not robust in the presence of any noise, including photon shot noise. Therefore, to use this, one has to use a noise-less photon distribution (without photon shot noise), which is not physical. Nevertheless, this function demonstrates the architecture for using a generic optimization routine for calibration. 

To import, run::

    from laser_calibration.generic_optimize import generic_optimize

To use, simply run::

    generic_optimize(syst)

Where ``syst`` is a ``LaserCalibrationSystem`` instance. 

Additional options exist; see the docstrings of the function.




