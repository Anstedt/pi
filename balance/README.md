# Issues
- MPU6050.cpp:84,85 This assumes the robot is standing straight up at
  startup. At startup the gyro portion does not make sense to
  calibrate since it is based off of motion and the robot should not
  be moving. The acceleromterer should be used to determine the
  startup angle since it uses gravity.
 
  The acceleromterer can be manual calibrated by standing/sitting the
  robot straight up and getting the raw values from the acceleromterer.
  
