# arduino_mpu6050

The experiment components
- Arduino Nano x 1
- GY-521/MPU6050 x 2 (or 3)
- Codebase is from [jrowberg](https://github.com/jrowberg/i2cdevlib.git)

All MPU6050s are connected to the same I2C interface of Anrduino Nano. Try to read all MPU6050s data (accelerometer xyz and gyro xyz) 

## Installation
- [Install the Arduino Software (IDE) on on Linux](https://www.arduino.cc/en/main/software)

- I2C lib
    * Download the zip file of the git repository of i2c lib and MPU6050 driver from [here](https://github.com/jrowberg/i2cdevlib/tree/master/Arduino/MPU6050). The file name shall be i2cdevlib-master.zip.
    * Extract i2cdevlib-master from i2cdevlib-master.zip
    * Put i2c and mpu6050 into the path of Arduion libraries. Default is ~/Arduino/libraries
    ```
    cd i2cdevlib-master/Arduino
    mv I2CDev ~/Arduino/libraries
    mv MPU6050 ~/Arduino/libraries
    ```
- Serial port permissions<br>
    As normal user from terminal: ```ls -l /dev/ttyUSB*``` or ```ls -l /dev/ttyACM*```. You will get something like
    ```
    crw-rw---- 1 root uucp 188, 0  5 apr 23.01 ttyUSB0 or
    crw-rw---- 1 root dialout 188, 0  5 apr 23.01 ttyACM0
    ```
    The "0" might be a different number, or multiple entries might be returned. In the first case the data we need is uucp, in the second dialout. (this is the group owner of the file)
    Now we just need to add our user to the group:
    ```
    sudo usermod -a -G group-name username
    ```
    group-name is the data found before, and username is your Linux user name. **You will need to log out and in again for this change to take effect**.

- Screen for monitoring serial port
    ```
    sudo apt-get install screen
    screen /dev/ttyUSB0 115200
    ```

## Reference
- I2C and MPU6050 driver provided by Jeff Rowberg. [I2C lib](http://www.i2cdevlib.com/devices/mpu6050)
or [the latest code on GitHub](https://github.com/jrowberg/i2cdevlib/tree/master/Arduino/MPU6050)
- Arduino [MPU-6050 Accelerometer + Gyro](https://playground.arduino.cc/Main/MPU-6050)
- [Installing Additional Arduino Libraries](https://www.arduino.cc/en/Guide/Libraries)