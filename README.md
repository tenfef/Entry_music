# Entry Music 

![](http://i.imgur.com/sIMR3FW.png)

A python script to run entry music based on IPs entering/exiting the network. 

## Limitations
In order for this to work each IP needs to be static so that it won't change the next time it connects to the network. A simple way to do this is lock a device to an IP using the routers DHCP settings. Alternatively you can set a static IP in the devices wifi settings.

This has been tested to work on Mac OS X and a Raspberry Pi

## Installation
Download the repository and run ```pip install``    

run: ```python run.py``` to run

To run create a ```users.json``` file in the root with your users names and local static IP addresses eg:
```
[{
	"name" : "Jack",
	"ip" : "192.168.1.xxx"		
},
{ 
	"name" : "Jill",
	"ip" : "192.168.1.xxx"		
}]
```

Then create a themes directory and put in potential entry music based on the names. Eg. for jack you would create a directory: **themes/Jack/**

and put any mp3s you want in there

Currently tested on Mac OS X

Edit config.json to overide these settings
```
{ 	
	"song_timeout_secs" : 15,
	"away_timeout_mins" : 8
}
```
