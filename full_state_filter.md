# Full State Filter
Beyond the scope of just the airbrakes, I will conduct the research and development of the entire rockets and its environments prior to and throughout the flight.


## What is the state?
State in our rockets reference frame consists of the `attitude`, most commonly represented as a quaternion which includes the heading. Further, a three dimensional vector for the `position` (relative to the launch pad), the `velocity` and the `acceleration`. My model used for the airbrake simulation additionally included the `jerk` (change in acceleration or 3th derivative of position over time) which helped since the system does experience a change in acceleration due to a change in drag through dynamic airbrakes and velocity.

The attitude should be modeled as a third order system, since imperfect aerodynamic surfaces cause a torque being applied to the rocket along an axis which leads to a change in angular velocity ($\Delta \omega$)
Using a DCM (Direction Cosine Matrix) to model the attitude, would result in a 9x9 matrix for the attitude state alone and an equally big one for the variances and covariances. I will have to benchmark matrix operations on the `STM32F4` especially with FP operations, but an inital guess is that one multiplication of 9x9 ^2 will take on the order of microseconds. For now I'll however postbone decision on specific implementations of that math on the hardware.

## Intermediate Variables
Often sensor readings are converted to a more meaningful value to us. This includes pressure to altitude conversion. Temperature is another variable that appears in many equations and is returned by the IMU's, baro and magnetometer for drift correction.


## Kalman Filters
### Tune Variables Filter
These variables will be used from time to time (maybe every 200 cycles of the main control software) to adjust the coefficients in equations related to drag. We will have to be careful when using them however, since all of the sensors are placed inside of the avionics bay tube which will heat up compared to the outside cooling down. For logging purposes (of internal heat management) we will however keep filtering temperature inside the body.
The outside pressure is [related to the air density](https://en.wikipedia.org/wiki/Barometric_formula) which determines the amount of drag we experience. With regards to computational costs and accuracy we could also just derive the air pressure (and thereby density) using the aforelinked barometric pressure formula.
$$
x = \begin{bmatrix} \text{Temperature} \\ \text{Pressure} \end{bmatrix}
$$

### Attitude Filter
This one might be the most complex one. The state is a combination of measurements of both the two IMUs gyrosciopes (more frequent) and the magnetometer (less frequent). The gyros give us the first derivative of the heading. Mainly to avoid the most obvious problems with euler angles the attitude will be comprised of quaternions representing the 


### Ressources
- [Quaternion Kalman Filters](https://www.commsp.ee.ic.ac.uk/~mandic/research/CJ_CPM_Quaternion_WL_Kalman_IEEE_TNNLS_2014.pdf)
- [Quaternion kinematics for the error-state Kalman filter](https://arxiv.org/pdf/1711.02508)
- [Angles relative to the LTP](https://en.wikipedia.org/wiki/Local_tangent_plane_coordinates)