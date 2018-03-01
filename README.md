# remoterobot
remotely control a robotic arm

## Installation
The software and hardware used for this project should all work across Linux, Windows and Mac. But it's only been
tested on Linux so far. Follow the steps below to get started:

  * create a python3 virtualenv.
  * Install packages in the projects requirements file.
  * Plug in the uArm Swift Pro into your machine's USB port.
  * Plug in the Sony PS4 controller into your machine's USB port.


## Run the Client and Server
Once you activate the virtualenv execute the client and server scripts in different terminals with the following commands:

```bash
./client.py
./server.py
```
Now you can control the robot. The client can connect to a remote server when the host command line argument is provided.

## Latency
There is a helper script called latency.py which can be run to measure the network latency between the client and server.
Below is an example of the output the command will generate.

```bash
$ ./latency.py 
seq:  1  time: 3.04 ms (excluded from stats)
seq:  2  time: 1.14 ms 
seq:  3  time: 0.93 ms 
seq:  4  time: 0.92 ms 
seq:  5  time: 0.91 ms 
seq:  6  time: 1.09 ms 
seq:  7  time: 0.89 ms 
seq:  8  time: 0.84 ms 
seq:  9  time: 0.84 ms 
seq: 10  time: 0.88 ms 
-------- SUMMARY --------
  max: 1.14 ms
  avg: 0.94 ms
  min: 0.84 ms
```


## Video
making a cucumber and cheese sandwich with the robot. 

![robot_sandwich](https://user-images.githubusercontent.com/3801994/36819470-b7a68fa2-1cfa-11e8-8db2-7a55b2a3420d.gif)

**Youtube version**

[![robot_sandwich video](http://img.youtube.com/vi/pStqqR5TLCc/0.jpg)](http://www.youtube.com/watch?v=pStqqR5TLCc)


