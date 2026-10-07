import math

import numpy as np
import constants
import scipy.constants


"""
 @brief Temperature as function of height.
 @param height Height above sea level in meters
 @return Temperature in Kelvin.
"""
def tempFromHeight(height: float) -> float:
    return -0.0065*height + constants.SURFACE_AIR_TEMPERATURE


"""
 @brief Air Pressure from height.
 @param height Height AGL
 @return Air pressure in pascal.
"""
def airPressureFromHeight(height:float) -> float:
    return constants.SURFACE_AIR_PRESSURE * math.exp(-(1/8400) * height)


"""
 @brief Air density from height
 @param height Height above ground level.
 @return Air density in kg/m³ 
"""
def airDensityFromHeight(height:float) -> float:
    air_pressure = constants.SURFACE_AIR_PRESSURE * math.exp(-(1/8400) * height) # could linearize this
    R_spec = scipy.constants.gas_constant / 0.0289652 # second number is molar mass of dry air
    temp = tempFromHeight(height)

    return air_pressure / (R_spec * temp)

"""
 @brief     Converts extension to additional exposed surface area.
 @details   This is an approximation, assuming a linear behaviour and the flaps
            being rectangular.
 @param     extension Value from 0 to 1 that defines how far the airbrakes are extended
 @return    New area perpendicular to air stream in m²
"""
def calculateAirbrakeSurfaceAreaFromExtension(extension: float) -> float:
    assert 0 <= extension and extension <= 1, "Invalid extension provided"
    
    maxArea: float = 3 * constants.AIRBRAKE_FLAP_HEIGHT * constants.AIRBRAKE_FLAP_WIDTH
    return extension * maxArea

"""
 @brief     Drag force due to airbrake extension
 @details   Assumes same air density as whole rocket.
 @return    Force in Newtons.
"""
def airbrakeAdditionalDragForce(airbrakeExtension:float, airbrakeCd: float,  velocity: float, spec_airdensity: float) -> float:
    airbrakeSurfaceArea: float = calculateAirbrakeSurfaceAreaFromExtension(airbrakeExtension)
    
    force = 0.5 * spec_airdensity * airbrakeSurfaceArea * airbrakeCd * (velocity ** 2)
    return force

"""
    @brief Custom G-H-Filter that allows for none-uniform time steps
"""
class GHFilterDeltaT:
    def __init__(self, x0: float, dx0: float, g: float, h: float):
        self.x = np.array([x0])
        self.dx = np.array([dx0])
        self.g_gain = g
        self.h_gain = h

    """
        @brief Update the state with variable delta time and the measurement
        @param dt Time since last update
        @param z  The new measurement
        @return filtered x and dx
    """
    def update(self, dt:float, z: float):        
        if dt == 0:
            return [self.x, self.dx]

        # Make prediction
        estimate_x = self.x + dt * self.dx

        # Check prediction
        residual = z - estimate_x
        try:
            # Update x and dx
            self.dx = self.dx + (self.h_gain*residual) / dt
            self.x = estimate_x + self.g_gain*residual
            return [self.x, self.dx]
        except ZeroDivisionError:
            print("ZDE")
            return [self.x, self.dx]


class GHKFilterDeltaT:
    """Second-order g-h-k filter for position, velocity, and acceleration."""

    def __init__(self, x0: float, dx0: float, ddx0: float,
                 g: float, h: float, k: float):
        self.x = np.array([x0])
        self.dx = np.array([dx0])
        self.ddx = np.array([ddx0])
        self.g_gain = g
        self.h_gain = h
        self.k_gain = k

    def update(self, dt: float, z: float):
        """Update the filter and return position, velocity, and acceleration."""
        if dt == 0:
            return [self.x, self.dx, self.ddx]

        # Predict with a constant-acceleration model.
        estimate_x = self.x + dt * self.dx + 0.5 * dt**2 * self.ddx
        estimate_dx = self.dx + dt * self.ddx
        residual = z - estimate_x

        # Correct each state with the appropriate time scaling.
        self.x = estimate_x + self.g_gain * residual
        self.dx = estimate_dx + (self.h_gain * residual) / dt
        self.ddx = self.ddx + (2 * self.k_gain * residual) / dt**2

        return [self.x, self.dx, self.ddx]
