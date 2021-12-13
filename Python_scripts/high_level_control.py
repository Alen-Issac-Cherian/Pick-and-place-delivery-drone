#importing required libraries

#class DeliveryDrone

  #__init__(self)
        #initializing rosnode

        self.coordinates = [0, 0, 1]
        self.checkpoint = [5, 5, 1]

        self.Kp = [10, 10, 3.1]
        self.Ki = [0, 0, 0.11]
        self.Kd = [42, 42, 6.7]

        self.error = [0, 0, 0]
        self.prev_error = [0, 0, 0]
        self.error_difference = [0, 0, 0]
        self.error_sum = [0, 0, 0]
        self.pid_output = [0, 0, 0]
        self.max_value = [2000, 1024]
        self.min_value = [1000, 0]
        self.yaw_angle = 0

        self.sample_time = 0.001

        #publishing topics
        #subscribing topics

  #defining callback functions

  #pid function
        self.error[0] = self.checkpoint[0] - self.coordinates[0]
        self.error_difference[0] = self.error[0] - self.prev_error[0]
        self.error_sum[0] = self.error_sum[0] + self.error[0]

        self.error[1] = self.checkpoint[1] - self.coordinates[1]
        self.error_difference[1] = self.error[1] - self.prev_error[1]
        self.error_sum[1] = self.error_sum[1] + self.error[1]

        self.error[2] = self.checkpoint[2] - self.coordinates[2]
        self.error_difference[2] = self.error[2] - self.prev_error[2]
        if self.error[2] > -0.15 and self.error[2] < 0.15:
            self.error_sum[2] = self.error_sum[2] + self.error[2]

        self.pid_output[0] = (self.error[0] * self.Kp[0]) + (self.error_sum[0] * self.Ki[0]) + (self.error_difference[0] * self.Kd[0]/self.sample_time)
        self.pid_output[1] = (self.error[1] * self.Kp[1]) + (self.error_sum[1] * self.Ki[1]) + (self.error_difference[1] * self.Kd[1]/self.sample_time)
        self.pid_output[2] = (self.error[2] * self.Kp[2]) + (self.error_sum[2] * self.Ki[2]) + (self.error_difference[2] * self.Kd[2]/self.sample_time)

        self.cmd_drone.rcRoll = 1500 + self.pid_output[0]
        self.cmd_drone.rcPitch = 1500 + self.pid_output[1]
        self.cmd_drone.rcThrottle = 512 + self.pid_output[2]

        if self.cmd_drone.rcRoll > self.max_value[0]:
            self.cmd_drone.rcRoll = self.max_value[0]
        elif self.cmd_drone.rcRoll < self.min_value[0]:
            self.cmd_drone.rcRoll = self.min_value[0]       

        if self.cmd_drone.rcPitch > self.max_value[0]:
            self.cmd_drone.rcPitch = self.max_value[0]
        elif self.cmd_drone.rcPitch < self.min_value[0]:
            self.cmd_drone.rcPitch = self.min_value[0]

        if self.cmd_drone.rcThrottle > self.max_value[1]:
            self.cmd_drone.rcThrottle = self.max_value[1]
        elif self.cmd_drone.rcThrottle < self.min_value[1]:
            self.cmd_drone.rcThrottle = self.min_value[1]

        self.prev_error[0] = self.error[0]
        self.prev_error[1] = self.error[1]
        self.prev_error[2] = self.error[2]

