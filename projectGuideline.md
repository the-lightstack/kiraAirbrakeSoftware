## Airbrake System
To achieve a precise target apogee, our system model has to closely approximate the actual state. Therefore we need to know all about the inputs and outputs used to interactive with the physical world. 


We will not use all the sensors to simplify the model. For example, we could use the magnetometer and the gyroscope in the IMU to estimate the orientation and use that to derive the aerodynamic wet are for a better model of the rockets $C_D$ with and without the airbrakes extended. I will, however, refrain from doing this as the error due to the missing account of flow separation and turbulences would most likely leave the variance of the added measurements big enough to deem them unworthy of the invested time, compute ressources and opportunity for errors. 

### Sensory Inputs.

1) Primary IMU (LSM6DSO32)
 - Measurement Range (accelerometer): 32G down to 4G
 - ODR:  up to 6667 Hz (1667Hz can be used for model)
 - precision: (page 26 on datasheet) 3.2mg/RMS (will be better in high performance mode)

2) Secondary IMU (BMI088)
 - Measurement Range (accelerometer): 3G to 24G
 - precision: output noise density is 190 ug / sqrt(Hz), 
    so at a Bandwidth of 245Hz on the z-axis we get a stddev of 2.97m G or +- 0.0292 m/s²
    HOWEVER: if the x or y axis point up (IMU mounted parallel to the rocket frame) we have
    to use the x/y axis ND   (160ug/sqrt(Hz)) and get a stddev of +/- 2.5044mG (@245 Hz Bandwidth)
    *Assuming x mounted up: a sampling rate of 1600Hz gives an x-axis BW of 280Hz resulting in a stddev of +/- 0.0262644 m/s²*
 
 - ODR: up to 1600Hz (can use LPF first)

3) Barometer (DPS368)
 - precision: 0.35 ($Pa_rms$)
 - ODR: 26Hz (Standard precision)



### Kalman Filter Design.

#### Initial State (x & P).
Our model only starts when the motor burnout is detected, but we can get barometric readings before that, which are quite precise, so we take the last baro-reading as the inital guess for the height. Using the $Pa_rms$ precision from the data sheet we get $0.1225 Pa²$ for our height variance.
The openRocket model suggests, that our inital velocity is around $130 m/s$ so I will define the possible region to be with 99.7% certainty between 90 and 170 m/s. So 3 sigma is 40 m/s, therefore sigma = 13.3 m/s and our velocity variance comes out to $177.7 (m/s)²$.


$$
\mathbf x =\begin{bmatrix}x \\ \dot x\end{bmatrix} =  \begin{bmatrix}250 \\ 130\end{bmatrix}

$$
$$
\mathbf P = \begin{bmatrix}0.1225 & 0 \\ 0&177.7\end{bmatrix}
$$

We are neglecting the covariance between vertical velocity and height for now, but the filter will converge to appropriate values during the flight.

#### Process Model.
*Standard newtonian*, can add acceleration to it later. If we are going for an Extended Kalman filter we could also incorporate our knowledge of the drag force on the decceleration that is quadratically (not linearly) dependant on the velocity.

#### Process Noise.


### Control Input (u). 
The extension of the airbrakes as a scalar.

### Control Transfer Function (B).
The quadratic relation between velocity and the effects the (now computed) airbrake-extension produced drag has on the acceleration.


### Update Step.

#### Measurement Matrix. 
We can only measure acceleration and position, so velocity remains a hidden variable.

For a position measurement the equation for the updated $y = z - H \bar x$ with $\bar x$ being the prior. With $x$ as 
$$
\mathbf x =\begin{bmatrix}x \\ \dot x \\  \ddot x \end{bmatrix} 

\mathbf z =\begin{bmatrix}2.3 \\ 0 \\  0 \end{bmatrix} 

\mathbf H =\begin{bmatrix} 1 & 0 & 0  \end{bmatrix}
$$

$H$ just converts our current system state into measurement space.

#### Measurement Noise Matrix.
The covariances are hard to determine analyically (although the IMU's should be close to 1, as they should read the same values) we will leave them at 0 for now 
and focus on the variances of the sensors individually.
$$

\mathbf sensors =\begin{bmatrix} \text{IMU 1} \\ \text{IMU 2}  \\ \text{Baro} \end{bmatrix}


\mathbf R =\begin{bmatrix} 6.8982e{-4} & 0 & 0 \\ 0 & x & 0 \\ 0 & 0 & y   \end{bmatrix}
$$

We could also represent the measuremtent Matrix (section above) as a linear combination between the 2 IMU's to fuse them directly, but as we might not get the data
concurrently from both, we can also keep them separate.


### Simulation of physical servo extension
The servo used is the MG995R ([datasheet](https://www.alldatasheet.com/datasheet-pdf/view/1131873/ETC2/MG996R.html)) which lists a rotational speed of $0.17 \frac{s}{60°}$ when powered with 4.8V. 
As a proxy we will assume that 0° is 0% extension and 120° (max of the servo) corresponds to 100% extension. It needs 0.34s for the full extension, which involves extending each flap by $17.425mm$, so the linear velocity is $0.05125\frac{m}{s}$


