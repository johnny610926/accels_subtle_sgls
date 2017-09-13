// I2C device class (I2Cdev) demonstration Arduino sketch for MPU6050 class
// 10/7/2011 by Jeff Rowberg <jeff@rowberg.net>
// Updates should (hopefully) always be available at https://github.com/jrowberg/i2cdevlib
//
// Changelog:
//      2013-05-08 - added multiple output formats
//                 - added seamless Fastwire support
//      2011-10-07 - initial release

/* ============================================
I2Cdev device library code is placed under the MIT license
Copyright (c) 2011 Jeff Rowberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
===============================================
*/

// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "SimpleTimer.h"
#include "I2Cdev.h"
#include "MPU6050.h"

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

// uncomment "OUTPUT_READABLE_ACCELGYRO" if you want to see a tab-separated
// list of the accel X/Y/Z and then gyro X/Y/Z values in decimal. Easy to read,
// not so easy to parse, and slow(er) over UART.
#define OUTPUT_READABLE_ACCELGYRO

// uncomment "OUTPUT_BINARY_ACCELGYRO" to send all 6 axes of data as 16-bit
// binary, one right after the other. This is very fast (as fast as possible
// without compression or data loss), and easy to parse, but impossible to read
// for a human.
//#define OUTPUT_BINARY_ACCELGYRO

#define RECEIVE_DATA_TIME_INTERVAL  10 // ms

#define LED_PIN 13

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro1((uint8_t)0x68); // <-- use for AD0 low
MPU6050 accelgyro2((uint8_t)0x69); // <-- use for AD0 high
MPU6050 *accelgyro_array[2];

int16_t ax[2], ay[2], az[2];
int16_t gx[2], gy[2], gz[2];

SimpleTimer ledTimer, recvI2CTimer;

void toggleLED() {
    static bool blinkState = false;
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);
}

void recvI2C() {
    #define ONLY_ACCEL  1
    
    unsigned long time_stamp = millis(); // micros();
    char databuf[128];

    // read raw accel/gyro measurements from device
    //accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    //accelgyro1.getMotion6(&ax[0], &ay[0], &az[0], &gx[0], &gy[0], &gz[0]);
    //accelgyro2.getMotion6(&ax[1], &ay[1], &az[1], &gx[1], &gy[1], &gz[1]);
    for(int i = 0; i < 2; i++) {
        #if ONLY_ACCEL == 1
        accelgyro_array[i]->getAcceleration(&ax[i], &ay[i], &az[i]);
        #else
        accelgyro_array[i]->getMotion6(&ax[i], &ay[i], &az[i], &gx[i], &gy[i], &gz[i]);
        #endif
    }
        
    // these methods (and a few others) are also available
    //accelgyro.getAcceleration(&ax, &ay, &az);
    //accelgyro.getRotation(&gx, &gy, &gz);
    
    #ifdef OUTPUT_READABLE_ACCELGYRO
        // display tab-separated accel/gyro x/y/z values
        for (int i = 0; i < 2; i++) {
            #if ONLY_ACCEL == 1
            sprintf(databuf,"%d\t%lu\t%d\t%d\t%d\n", i+1, time_stamp, ax[i], ay[i], az[i]);
            #else
            sprintf(databuf,"%d\t%lu\t%d\t%d\t%d\t%d\t%d\t%d\n", i+1, time_stamp, ax[i], ay[i], az[i], gx[i], gy[i], gz[i]);
            #endif
            Serial.print(databuf);
        }
    #endif
    
    #ifdef OUTPUT_BINARY_ACCELGYRO
        Serial.write((uint8_t)(ax >> 8)); Serial.write((uint8_t)(ax & 0xFF));
        Serial.write((uint8_t)(ay >> 8)); Serial.write((uint8_t)(ay & 0xFF));
        Serial.write((uint8_t)(az >> 8)); Serial.write((uint8_t)(az & 0xFF));
        Serial.write((uint8_t)(gx >> 8)); Serial.write((uint8_t)(gx & 0xFF));
        Serial.write((uint8_t)(gy >> 8)); Serial.write((uint8_t)(gy & 0xFF));
        Serial.write((uint8_t)(gz >> 8)); Serial.write((uint8_t)(gz & 0xFF));
    #endif
}

void setup() {
    accelgyro_array[0] = &accelgyro1;
    accelgyro_array[1] = &accelgyro2;

    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    //Serial.begin(38400);
    Serial.begin(115200);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro1.initialize();
    accelgyro2.initialize();

    // Default Accel and Gyro ranges are 2G and 250 deg/sec respectively.
    /*
    uint8_t range1 = accelgyro1.getFullScaleAccelRange();
    uint8_t range2 = accelgyro2.getFullScaleAccelRange();
    Serial.print("Accelerometer range = ");
    Serial.print(range1); Serial.print("\t");
    Serial.println(range2);
    range1 = accelgyro1.getFullScaleGyroRange();
    range2 = accelgyro2.getFullScaleGyroRange();
    Serial.print("Gyro range = ");
    Serial.print(range1); Serial.print("\t");
    Serial.println(range2);
    */

    /* MPU6050_ACCEL_FS_2 : 2G
     * MPU6050_ACCEL_FS_4 : 4G
     * MPU6050_ACCEL_FS_8 : 8G
     * MPU6050_ACCEL_FS_16 : 16G
     */
    //accelgyro1.setFullScaleAccelRange(MPU6050_ACCEL_FS_2)
    //accelgyro2.setFullScaleAccelRange(MPU6050_ACCEL_FS_2)

    /* MPU6050_GYRO_FS_250 : 250 degrees/sec
     * MPU6050_GYRO_FS_500 : 500 degrees/sec
     * MPU6050_GYRO_FS_1000 : 1000 degrees/sec
     * MPU6050_GYRO_FS_2000 : 2000 degrees/sec
     */
    //accelgyro1.setFullScaleGyroRange(MPU6050_GYRO_FS_250);
    //accelgyro2.setFullScaleGyroRange(MPU6050_GYRO_FS_250);
    
    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro1.testConnection() ? "MPU6050_1 connection successful" : "MPU6050_1 connection failed");
    Serial.println(accelgyro2.testConnection() ? "MPU6050_2 connection successful" : "MPU6050_2 connection failed");
    
    // use the code below to change accel/gyro offset values
    /*
    Serial.println("Updating internal sensor offsets...");
    // -76	-2359	1688	0	0	0
    Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    accelgyro.setXGyroOffset(220);
    accelgyro.setYGyroOffset(76);
    accelgyro.setZGyroOffset(-85);
    Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    */

    // configure Arduino LED for
    pinMode(LED_PIN, OUTPUT);

    ledTimer.setInterval(500, toggleLED);
    recvI2CTimer.setInterval(RECEIVE_DATA_TIME_INTERVAL, recvI2C); // read data every 10 ms
}

void loop() {
    recvI2CTimer.run();
    ledTimer.run();
}
