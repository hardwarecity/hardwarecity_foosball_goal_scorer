PROJECT: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sensors <--> Arduino <--> Raspberry Pi <--> Firebase <--> Web App

RASPBERRY PI:
Listen (with interrupts) PORT 20 (Team A) and PORT 21 (Team B).
When a trigger happens, the internal variables (goal counters) is updated, and a message is sent by firebase by HTTP.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


INSTALL ON RASPBIAN: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y python-dev python3-dev
sudo apt-get install -y python-pip python3-pip
sudo pip install bottle

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

GPIO ON OSMC: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sudo apt-get update
sudo apt-get install build-essential
export ARCH=arm
export CROSS_COMPILE=/usr/bin/

By: https://discourse.osmc.tv/t/gpio-control-need-some-help/3246/4



To install the latest development version from the project source code library:

$ sudo apt-get install -y python-dev python3-dev
$ sudo apt-get install -y mercurial
$ sudo apt-get install -y python-pip python3-pip
$ sudo apt-get remove -y python-rpi.gpio python3-rpi.gpio
$ sudo pip install hg+http://hg.code.sf.net/p/raspberry-gpio-python/code#egg=RPi.GPIO
$ sudo pip-3.2 install hg+http://hg.code.sf.net/p/raspberry-gpio-python/code#egg=RPi.GPIO

To revert back to the default version in Raspbian:

$ sudo pip uninstall RPi.GPIO
$ sudo pip-3.2 uninstall RPi.GPIO
$ sudo apt-get install python-rpi.gpio python3-rpi.gpio

by: http://raspberrypi.stackexchange.com/questions/27407/importerror-no-module-named-gpio
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++