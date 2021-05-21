# Crazyflie Firmware Instrumentation

This project instruments the crazyflie firmware to analyze how the controllers bahave with different amount of jitter.

## Building and Flashing
See the [building and flashing instructions](docs/building-and-flashing/build.md) from the original projects github docs folder.

## List of Modifications
* Stabilizer.c : Added psuedo random number generator, function lcg(), and event based logging in the while(1) loop. For future use, instead of using the psuedo random number generator, one can include <stdlib.h> and use the rand() function

* Added folder 'python_tests' with python and matlab scripts:
  * log_flight: Contains scripts for the used flight paths
  * cfusdlog: Decode gathered data (provided by Bitcraze)
  * decode_logs: Decodes data with help of function in cfusdlog and saves it
  * modelling_shifts.m: MATLAB script to analyse decoded data. Data has to be formatted as a time series (not dictionary)

* tools/usdlog/config.txt: File to be (manually) copied to the uSD-card for logging
