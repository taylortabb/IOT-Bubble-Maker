# Bubbles Right Now: An IOT Bubble Maker!

![Bubblemaker and bubbles cover photo](https://github.com/taylortabb/IOT-Bubble-Maker/raw/master/docs/wall.jpg)

Making an Internet of Things Bubble Maker is a surefire way to make any space more exciting. For most, following these instructions shouldn't take more than an afternoon. [Here](https://imgur.com/a/gs9m4LL) is what it all looks like.

### Overview

Our goal is a bubble maker that can be controlled from the web, just like [pittsbubble.com]. We'll be using Python on a Raspberry Pi to start a server so Post requests from a webpage can switch GPIO pins on the pi– that will switch the relay, which in turn will power on or off the bubble maker. 

Along the way we'll have to configure a dynamic DNS server, add some security protections to the Pi, and experiment a bit with Daemons. The hardware and software for this project are pretty simple, but the networking is actually a little challenging.

### Hardware

These are the parts you'll need to get started:

- Raspberry Pi Zero° 
- Relay Module
- A bubble maker°°

°or almost any other Raspberry Pi 

°°ideally one that's not battery operated. I used [this](https://www.amazon.com/gp/product/B07FD4TD45) one.

### System Setup

To start, you'll need to make sure your RPi is running the latest version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) and connected to your network with SSH enabled. There are a bunch of ways to do this, but if you want to avoid plugging your pi into a screen and keyboard, follow my favorite steps below, otherwise **go ahead with whatever your preferred way of doing that is and skip to Hardware Setup!**

To start, you'll want to download [the latest version](https://downloads.raspberrypi.org/raspbian_lite_latest) of Raspbian Lite. Flash the image to the Pi's SD card, I like [Etcher](https://www.balena.io/etcher/) for doing this.

Mount your microSD card, and in a Terminal, navigate to the directory. Most likely, you can just type

```
$ cd /Volumes/boot
```

Create the file wpa_supplicant.conf (this will replace the RPi wifi config on boot)

```
$ nano wpa_supplicant.conf
```

Paste the below text into the file and adjust to your wireless network, and if not in the US, replace "us" with your country code:

```
country=us
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
 scan_ssid=1
 ssid="YOUR NETWORK NAME"
 psk="YOUR NETWORK PASSWORD"
}
```
Save the file, then close the file. Now create a file named ssh— this enables ssh on boot.

```
$ sudo touch ssh
```

Now unmount the SD and toss it back in your Pi— on boot, your Pi will connect to the specified network with SSH enabled! 

And before we go any further any Pi project should tell you, change your password from *Raspberry* to something more secure as soon as possible! SSH into your Pi, type `sudo raspi-config`, then select Change User Password ☺

### Hardware Setup

To start, plug that bubble maker in and enjoy some bubbles! Next, turn the on/off switch to off, unplug the unit, and while unplugged, turn on/off switch back to on— we want bubbles to blow whenever power is provided to the machine. Again with the power off (power unplugged) we'll want to connect the rest of the components in the following way:

![Diagram of system, relay plugged into pi and bubble maker power supply](https://github.com/taylortabb/IOT-Bubble-Maker/raw/master/docs/diagram.png)

The relay signal pin is connected to Pi pin 7, and the power for the bubble maker is attached to the relay, in the "NO" or "Normally Open" direction. Now power everything up! The bubble maker should not be blowing at this point.

### Bubble-Server

Getting the server going is actually the easiest part of all of this!

SSH into your Pi, and update/download all the required packages

`sudo apt-get install apache2 git python-requests RPi.GPIO`

Then navigate to /home/pi and make a new folder called bubbles

`mkdir bubbles`

enter the repo and clone this github repository 

`cd bubbles`

`git clone https://github.com/taylortabb/IOT-Bubble-Maker.git`

Enter the directory

`cd IOT-Bubble-Maker`

And open bubble-server.py to get an idea what's going on `nano bubble-server.py` and follow the notes in the code. 

`sudo nano bubble-server.py`

That's it! you're ready to run the server with `python bubble-server.py`

### The Webpage

The Python server accepts Post requests including the duration to turn on the bubble maker. It's very easy to set up your on page to send this request, but if you'd like to use the template, follow these steps, otherwise skip to **Making it Remotely Accessible.**

On your computer, download this github repo and open index.html (in the main repo folder, not the docs folder) in a text editor. Scroll down to the bottom and be sure to enter your Pi's IP in the form of 192.168.1.18:8080 (8080 is the port the python server is on, so be sure to include that) where you see `REPLACE THIS WITH YOUR SERVER ADDRESS`.

```
request = $.ajax({
  url: "REPLACE THIS WITH YOUR SERVER ADDRESS",
  type: "post",
  data: serializedData
});
```

You can also change the duration the bubble maker remains on by changing  "5" to another integer in `<input type="hidden" name="duration" value="5">`

Save and close the file.

### Making it Remotely Accessible

At this point, if you open index.html in a web browser on the same network as your Pi, pressing the button should make bubbles flow! To make it accessible from anywhere, you'll need to set up port forwarding and a dynamic DNS service. Note: setting up port forwarding in an inherent security risk, and every router and ISP works differently. Should you wish you make the bubble blower accessible from the internet, it's totally at your on risk.

#### Port Forwarding

Port forwarding works differently on every router, but you'll most likely need to log into your router's admin panel and follow specific instructions associated with that device— your goal is to forward TCP/UDP traffic on port 8080 to your Pi's local IP address. 

#### Dynamic DNS

You'll then need to configure a Dynamic DNS service to ensure the POST request always is sent to the correct IP. I like No-IP because there is a free option, AND once you've made and account and set up forwarding, there's a [simple add on for RPi](https://www.noip.com/support/knowledgebase/install-ip-duc-onto-raspberry-pi/) to keep your IP updated!

As your Pi is now accessible from the deepest depths of the web, you'll want to at the very minimum try to bock malicious connections, perhaps using [Fail2Ban](https://pimylifeup.com/raspberry-pi-fail2ban/). While you're not likely causing a security issue, there is risk in making your pi remotely accessible, and remember you should proceed at your own choice.

Finally, you'll just need to go back to index.html and replace the `"REPLACE THIS WITH YOUR SERVER ADDRESS",` with your No-IP address, i.e. bubbles.noipaddress.com:8080.

### Getting it to run on boot

Now we'll make sure all this runs each time you turn on the pi. This will mean we use Cron! A very cool job scheduler that works with RPi. SSH into your Pi and enter the following

`crontab -e`

scroll all the way to the bottom and paste the following to ensure the bubble server and dynamic dns add on run after every reboot.

`@reboot python /home/pi/bubbles/bubble-server.py`

`@reboot sudo /usr/local/bin/noip2`

save and close the file. Type `sudo reboot` , and once your Pi reboots, the python script and noip add-on should be running!

### Finishing up

At this point, try pressing the button on index.html! If all seems good, your IOT Bubble Maker is ready to use! To host the webpage for remote use of the bubble maker, [GitHub pages](https://pages.github.com/) is a super great simple option. And better yet, if you have a .edu email address, you can get a free domain name from [namecheap](https://nc.me/), so you can share a custom link to use your bubble maker with all your friends!

And finally, I'd love to know if you've made a bubble maker— a whimsical long term goal is to create a world wide network of public bubble makers— If you would like your bubble maker listed and accessible from a hopefully-soon-to-exist [website](http://go.tabb.me/Global-Bubble-Dashboard/) of global bubble makers, shoot me a message [here](https://www.tabb.me/pittsbubble-feedback)

Have questions? You can connect with me [here](https://www.tabb.me/pittsbubble-feedback)

## Authors

- **Taylor Tabb** - [tabb.me](https://www.tabb.me/)

## License

This project is licensed under the MIT License.
