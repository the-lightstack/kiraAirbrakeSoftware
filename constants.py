import math
## Physical Environment
SURFACE_AIR_PRESSURE = 101_325 # Pascal
SURFACE_AIR_TEMPERATURE = 20 + 273.15 # Kelvin

## Simulation Specific
SIM_T0 = 3 # s
SIM_T0_VELOCITY = 129 # m/s
SIM_T0_HEIGHT = 250 # m

## Rocket Parameters
ROCKET_OUTER_DIAMETER_M = 0.124 # m
ROCKET_CSA = math.pi * (ROCKET_OUTER_DIAMETER_M/2)**2 # cross sectional area
ROCKET_BURNOUT_MASS = 15.59 # kg
AIRBRAKE_FLAP_HEIGHT = 72e-3 # m
AIRBRAKE_FLAP_WIDTH = 17.425e-3 #m
ROCKET_DEFAULT_CD = 0.34
ROCKET_AIRBRAKE_DEFAULT_CD = 1.17

# https://www.infineon.com/assets/row/public/documents/24/49/infineon-dps368-datasheet-en.pdf
BARO_RELATIVE_ACCURACY = 0.5 # meters
BARO_ABSOLUTE_ACCURACY = 8 # meters
