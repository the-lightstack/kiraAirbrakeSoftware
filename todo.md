# Improvements to the model

- [] Upgrade KF to EKF using linearized v² to change j estimate (better approx. bc of more system knowledge)
- [] Add *B* and *u* to EKF
- [] Include none deterministic transfer function from airbrake extension to added drag (as proposed in regularSampleFilter.ipynb)
- [] Add other IMU to the used data
- [] Add failed sensor detection w/ outlier detection
- [] Add functionality for only some measurements to be used
- [] Use smoothing to better predict using past values