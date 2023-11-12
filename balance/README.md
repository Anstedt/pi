# Issues
- MPU6050.cpp:84,85 This assumes the robot is standing straight up at
  startup. At startup the gyro portion does not make sense to
  calibrate since it is based off of motion and the robot should not
  be moving. The acceleromterer should be used to determine the
  startup angle since it uses gravity.
 
  The acceleromterer can be manual calibrated by standing/sitting the
  robot straight up and getting the raw values from the acceleromterer.
  
  m_acc_Z_cal_ang is calculated and not used. Has no real value since
  robot is not standing straight on startup. See MPU6050.cpp:113 and
  above.
  
  Gyro data also calibrated with same issue. Assume standing straight
  up.
  
# Design
- Clean up code
- Do not start motors or legs till after MPU6050::calibrate(void) is complete.
- In robot manually re-calibrate m_acc_calibration_value, uncomment
  SLOG << "accel_raw_avg=" << accel_raw_avg << std::endl; then run
  robot and set m_acc_calibration_value to the negation of accel_raw_avg.
