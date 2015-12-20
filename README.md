# bt4toy
This is simple script to show how to interact with bluetooth controlled toy that uses serial port profile. 

Some reverse engineering work was done to get the hci dump from bluetooth session with BMW Z4 bluetooth controlled car.
Such hci dump can be analyzed with wireshark to see what is actually send to device.

Prerequisites:
- pair with device
- define your BT device in /etc/bluetooth/rfcomm.conf:
rfcomm0 {
	bind no;
	# address of device
	device 8C:DE:52:01:78:26;  
	# rfcomm channel on which SPP profile is avialable, can be obtained with "sdptool browse" command
	channel	6;
	# some fancy name
	comment "BMW Z4 BT car serial port";
}
then:
-  rfcomm connect hci0
- lunch the python control.py script, and have fun.

