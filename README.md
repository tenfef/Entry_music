# Entry Music 

![](http://i.imgur.com/sIMR3FW.png)

A python script to run entry music based on IPs entering/exiting the network. 

## Limitations
In order for this to work each IP needs to be static so that it won't change the next time it connects to the network. A simple way to do this is lock a device to an IP using the routers DHCP settings. Alternatively you can set a static IP in the devices wifi settings.

This has been tested to work on Mac OS X and linux running on a Raspberry Pi

## Installation
Download the repository and run 
``pip install -r stable-req.txt``    

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

and put any song files in standard formats that you want in there for each user. mp3s, mp4as etc.
If there are multiple songs in the folder it will pick one at random.

Edit ``config.json`` to overide these settings
```
{ 	
	"song_timeout_secs" : 15,
	"away_timeout_mins" : 8
}
```

``away_timeout_mins`` Is the number of minutes a person has to be "unpingable" before the music will play on their return. I advise setting this to be 8mins or more to avoid false positives

``song_timeout_secs`` is the number of seconds the songs will play before they are cut off.

