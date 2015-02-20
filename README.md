# Entry Music 
A python script to run entry music based on IPs entering the network.
It's important to lock the DHCP settings for each users MAC address on your router to make sure every time they leave or enter the network they have the same IP.

To run create a ```users.json``` file in the root with your users names and local IP addresses eg:
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
