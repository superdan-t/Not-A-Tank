# Not-A-Tank
First-year undergrad project: This definitely isn't for a remote-controlled mini-tank with lasers or anything like that.

## Description
This was my first remote-vehicle project ever. I worked with a friend who was covering the hardware side. As many first-year computer science students do, I ambitiously attempted too much and this project got shoved aside eternally, so there isn't much here.

## Quick Software Overview
We wanted to control the tank over WiFi so that it could roam wherever the campus network was present. Since campus WiFi doesn't provide static IPs, we needed a way for the tank and controller to find each other. This was the role of the TankStatusServer, which could run on a third system that did have a static IP. The tank would tell the TankStatusServer its IP address when it came online, and the controller would request information about active tanks from the server.

There is little controller or tank code besides a video streaming prototype.

## What I Gained
* This was my first experience working with Raspberry Pi, a Zero W to be specific.
* While I didn't do anything mechanical myself, I learned about campus resources for things like 3D printing.
* I helped consider the electrical system and became familiar with battery management and voltage regulation
