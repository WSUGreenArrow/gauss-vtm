Video Transmission Software
===========================
This is the software that runs on the Raspberry Pi-based VTM.

The software is written for use with our specific hardware, but could be
adapted with some simple changes. It is largely a combination of a
Python script to drive the streaming and configuration files for some
networking components. The configuration files are under the `conf`
directory of this repository.

Prerequisites
-------------
This software uses a custom build of hostapd, the software responsible
for setting up the wireless adapter as an access point.

We are using an ALFA AWUS036ACH Wi-Fi adapter with an RTL8812AU chip.
Despite a standard build of hostapd working fine in the past, we can
now only get the product to function by using a version of hostapd
modified for Realtek devices.

This copy of hostapd can be built from the sources in the repository
[hostapd][hostapd], and the binary package for Raspbian is available in
the releases for that repository.

In addition to the copy of hostapd, the wireless card also requires a
custom version of the driver that can compile on Linux 3.10 and up.
The version we used has been forked into [rtl8812au][rtl8812au].



[rtl8812au]: https://github.com/WSUGreenArrow/rtl8812au
[hostapd]:   https://github.com/WSUGreenArrow/hostapd
