#Material
There are six materials needed to prepare.

* Raspberry pi 3 
* Dth11
	* Pin Configuration
		* 3.3v(1), out(gpio4), gnd(9)
* Speaker 
* [Voice detector sensor](https://www.taiwaniot.com.tw/product/聲音感測器模組-sound-detect-sensor/):
	* Pin Configuration 	
		* 5v(4), out(gpio27), gnd(20)
* [Pir motion sensor](https://maker.pro/raspberry-pi/tutorial/how-to-interface-a-pir-motion-sensor-with-raspberry-pi-gpio)
	* Pin Configuration 
		* 5v, out(gpio7), gnd
* Respberry pi camera module(v2):
	* take a picture : raspistill -v -o output.jpg
	* video  :  raspivid -o video.h264 -t 5000(5sec)
	
![Configuration](http://wordpress.bestdaylong.com/wp-content/uploads/2016/12/RPi-3的GPIO腳位_01.jpg)

#System Architect
##Identify_image
###[Demo video](https://www.youtube.com/watch?v=iWKzJXttQiE)
![Configuration](https://epl.tw/wp-content/uploads/2018/09/螢幕快照-2018-09-13-下午12.23.39.png)

* ButtonThenCamera.py
	* upload picture to S3
	* S3 bucketname : 'nthu-106062599'
* S3toLambda.py (python3.6)
	* S3 trigger Lambda to do rekognition then publish
	* This file be needed to put in AWS Lambda
* detect_label.py

##Detect_environment
###[Demo video](https://www.youtube.com/watch?v=BRCUmnfonFg)
![Configuration](https://epl.tw/wp-content/uploads/2018/09/螢幕快照-2018-09-13-下午12.24.03-1.png)

* basicPubSub.py
* TempDataFunc.py (python2.7) 
	* Dynamondb trigger Lambda to sned SNS(notify) to parents
	* This file be needed to put in AWS Lambda
* playMusic.py	
	* Pushing the APP button could choose the song that children like to stop crying.
	
#App:
## Sign in

<img src="https://epl.tw/wp-content/uploads/2018/09/螢幕快照-2018-08-31-下午3.11.14.png"  width="300">

## Display

<img src="https://epl.tw/wp-content/uploads/2018/09/螢幕快照-2018-08-31-下午3.10.37.png"  width="300">
<img src="https://epl.tw/wp-content/uploads/2018/09/螢幕快照-2018-08-31-下午3.11.06.png"  width="300">

