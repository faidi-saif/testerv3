to setup the tester follow these instructions : 

1- install the following packages :
     1- local machine : 
	* pip3 install bs4
	* pip3 install wget
	* pip3 install serial
	* pip3 install pyserial 
	* pip3 install paramiko
	* pip3 install requests 
	* pip3 install netifaces
    2- for jenkins :
        *there is a requirement.txt file which install all the packages automatically 

2- setup serial ports 
	* check the {idProduct} and {idVnedor} of your arduino and edit the file '94-serials.rules'
		-to find the informations about the usb port connected to the arduino :
		'udevadm info -a -p $(udevadm info -q path -n /dev/ttyusb_connected_to_arduino')
	* save the file '94-serials.rules ' in '/etc/udev/rules.d'
	* run : 'sudo udevadm control --reload-rules && udevadm trigger'
	* replug the usb (arduino , and usb fr rtos and linux on camera )

3- setup the power control
	* installation : 
		-clone the repos fllowing this link : https://www.yepkit.com/product/300115/YKUSHXS 
		-'sudo apt-get install libusb-1.0-0-dev '
		-'sudo apt-get install libusb-1.0-0 '
 		- In the root of the source code structure you will find the following two scripts:
    			build.sh
    			install.sh
		As the name indicates one builds the application and the other installs it.
		To build the application run: 'sudo ./build.sh '
		Finally install the hidapi shared libraries and the ykushcmd command by running the following script:
		'sudo ./install.sh' 

	* in '/etc/sudoers' add the following line : 'username  ALL=(ALL) NOPASSWD:/usr/bin/ykushcmd' with the appropriate username

	* setup the device serial_number : 
		- get the serial number using : 'sudo ykushcmd ykushxs -l' , example: {YKa1184} 
		- in ./network/arduinoSerializer edit the variable : "device_serial" to adapt it to 
		  your serial_number



 ATTRS{serial}=="0092AFEE"    ATTRS{serial}=="00945928"


