Documentation for laser_calibration package
=====

Mirror module
-------

The mirror module provides a class for controlling and storing mirror position. The ability to cache (store) the last position mirror is set to allows the ability to do tracking (this functionality is not built out in the current iteration), as well as necessary for simulation.

To import, run

>> from laser_calibration.mirror import Mirror

To initiate a mirror instance, run

>> mirror = Mirror(move_mirror_function)

where move_mirror_function is the function handle for moving mirror position. In simulation mode, one can simply do 

>> mirror = Mirror()

Position can be obtained/set using the position property. E.g.

>> mirror.position = 0.1

Will set mirror to position 0.1. Mirror position can be between -1 to 1. Running

    mirror.position

Will then return 0.1, the last mirror position.

LaserCalibrationSystem module
-------
This is the center piece of the codebase. An instance of LaserCalibrationSystem involves a set of Mirror instances, and an ion_response_function that measures the response from ions (number of photons). 

To import, run

	from laser_calibration.laser_calibration_system import LaserCalibrationSystem


