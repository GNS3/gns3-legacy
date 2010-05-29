Dynagen README
Version 0.11.1.091203


For documentation, refer to the tutorial in the docs directory, and the sample network files in the sample_labs directory. To see usage examples for all options, refer to the "all_config_options.txt" file in the sample_labs directory. Also be sure to visit the Dynamips web site at http://www.ipflow.utc.fr/index.php/Cisco_7200_Simulator.

This version of Dynagen requires at least version 0.2.8-RC1 of Dynamips. The Windows installer package requires at least Windows XP SP2. For earlier versions of Windows, replace the Dynamips binary with the Windows 2000 version as described in the Dynagen FAQ section of the tutorial.

Known Issues
============
* "save" and "idlepc save" commands may reformat the indentation of your network file and add an explicit "model" definition in the router section
* Gig interfaces on the NPE-G2 cannot currently be used.

Changelog
=========
Version 0.11.1.091203
* "delay" option added to dynagen.ini. Allows you to globally set the default delay between device startups. 
* Added a progress bar which is displayed during the delay between device startups.
* Sync with GNS3, which includes:
  - Some ghosting changes made by Pavel
  - Unicode support
  - Quick JIT blocks sharing support
  - Allows use of "monitor" filter provided by dynamips
  - Pavel's automatic unused slot removal

Version 0.11.0
* Merge of the features of confDynagen (dynamic reconfiguration, pemu support, and many other features). Big thanks to Pavel Skovajsa for performing the merge work and other significant contributions.
* Addition of a pemu server for Cisco PIX emulation. Thanks to Thomas Pani for writing the wrapper, and to mmm123 for writing pemu. NOTE: A Pemu instance will always consume 100% of a CPU core. There is no "idlepc". Use a tool like BES (Windows) or cpulimit (Linux) if you wish to reduce CPU usage.
* Could not specify a model of 1751 or 1760 in a router definition
* WIC interfaces on 1751s and 1760s could not be used
* On Windows platforms, Network Device list changes to the temp dir before executing Dynamips (helps Vista users).
* Added a delay option to start /all. This introduces a pause between starting devices.
* Filter command was broken in 0.10.x
* FS#217 - fixed the connect method for switches. Only effected 3rd party developers using the library, Dynagen does not use these methods.
* FS#211 - Dynagen crash when specifying invalid port
* 7200 instances now default to using an NPE-400 rather than an NPE-200. This is because the C7200-IO-2FE is not compatible with the NPE-200 and this was causing confusion. You can override this new behavior with "npe = NPE-200".
* Referencing f0/0 or f0/1 with 7200s now automatically inserts a C7200-IO-2FE in slot 0 rather than a C7200-IO-FE. You can override this behavior by specifying "slot0=PA-C7200-IO-FE".
* Support for ATM to Ethernet bridge introduced in Dynamips 0.2.8-RC2. Provision using ATMBR.
* idlemax issue fixed (see http://7200emu.hacki.at/viewtopic.php?p=13676)
* Resolves crash when invalid port specified on adapter (http://7200emu.hacki.at/viewtopic.php?p=15685)
* Dynagen now warns if a router does not have an image set
* The prefix "PA-" for the 7200 IO adapters is optional (i.e. "PA-C7200-IO-2FE" or "C7200-IO-2FE").
* Multisever config with two instances on the same system no longer requires use of the UDP configuration option workaround.
* The adapter "PA-4T+" should now be specified as "PA-4T+". "PA-4T" is still supported so as not to break compatibility with existing labs.
* Added a "start-pemu.sh" script to launch pemuwrapper, writing temp files to a temp directory. To be used on Linux systems.
* Throws a warning for the infamous "using localhost with multiserver" misconfiguration.
* Change of base udp port for pemuwrapper to 40000 so that we do not conflict with vpc
* "idlepc show" now shows the current idlepc value if one has already been applied
* idlepc commands now warn that pemu instances are not supported
* Added "ghostsize" command to dynamic configuration mode
* Ignores GNS3-DATA section. Caution: Issuing a "copy run start" from inside of Dynagen will obliterate this section.

Version 0.10.1
* Accidentally only gave the NM-16ESW 15 interfaces.

Version 0.10.0
* Support for the 1700 platform new to Dynamips 0.8.0-RC1. See the tutorial for supported platforms and modules.
* Support for WIC-1T, WIC-2T, and WIC-1ENET. See the tutorial for supported router platforms and usage.
* Support for NM-CIDS and NM-NAM. Note these are just "stubs" (at least as of this version of Dynamips). You can connect to them using "IDS-Sensorx/0 = ..." or "Analysis-Modulex/0 = ..." but they don't actually do anything. See the tutorial for platform support.
* FS#154 - added "confreg" command to set the configuration register of router(s) from Dynagen. e.g. "confreg r1 0x2142" followed by "reload r1". Note changes to the config register will not be displayed in a "show ver" until the router is reloaded.
* FS#182 - Second port of PA-C7200-IO-2FE was not usable
* FS#177 - crash on malformed interface entry in net file
* Dynagen now automatically picks a PA-2FE-TX rather than a PA-FE-TX when referencing a FastEthernet on ports 1-6 on a 7200. You can override this to mimic the old behavior with "slotx = PA-FE-TX".
* the vbs file that launches SecureCRT sessions was missing from the Windows installer package
* Changed the state shown with the "list" command for virtual switches from "n/a" to "always on" to avoid confusion.
* Added an up-to-date list of hardware emulated by Dynamips to the tutorial. Thanks to ggee for performing the initial documentation in this post: http://7200emu.hacki.at/viewtopic.php?t=1831

Version 0.9.3
* No longer prints a warning for unused switchports
* Added "MAC" option to set base MAC address of a router. See all_config_options.txt for usage.
* Eliminated unnecessary Leopard-2FE insertion on 3660s resulting in "a NM already exists in slot 0" warnings from Dynamips.
* Fix bug that caused crash when trying to capture packets on an unconnected interface
* Dynamips temp files are now written to the user's temp dir rather than \Program Files\Dynamips. Might make it work better under Vista.
* Dynagen allows POS to frame-relay switch connections. But there seems to be a bug in dynamips 0.2.7 that prevents it from functioning.
* Console entries in dynagen.ini for use with iTerm on OS X and SecureCRT on Windows. The SecureCRT one is a little glitchy but generally works.
* Entering "no ?" caused a crash
* Including a new Network Device list script for Windows that includes interface descriptions in the output contributed by Volker Semken.

Version 0.9.2
* Fixed required version string
* Removed false warning message when autostart is used at the router level
* Added some info and fixed some misspellings in all_config_options.txt
* Added the console command. It is identical to the telnet command. It occurred to me that "telnet" is a misleading command since a connection to the console is actually being made. But you can use which ever one you prefer, and you can abbreviate "console" as "con" if you wish.

Version 0.9.1
* added "oldidle" option for use in network files. Setting this to true allows you to use pre-0.2.7-RC2 idlepc values. This disables direct jumps between JIT blocks (new to 0.2.7 RC2). Use this a the top level of your network file, or in the defaults or specific router definition.
* sparsemem was misspelled in all_config_options.txt
* Built-in motherboard Ethernet/fastethernet interfaces now are automatically created on 2600 platforms.
* Improved checking for attempts to insert network modules into unsupported slots, and the error now indicates the offending router name.
* I totally neglected to include the 2611XM. Sorry 2611XM!
* 2621, 2621XM, and 2651XM mistakenly only got one integrated FE instead of two.
* Could not use gigabit adapters properly on 7200s
* This version performs much more rigorous checking for the validity of adapters against routers, and now outputs warnings for config items that it cannot parse and ignores. This should help with troubleshooting network files.
* Added a check for minimum required version of dynamips
* Added a check for trying to run idlepcget when an idlepc value has already been applied
* Fixed misc idlepc get/save bugs. BTS 143, BTS 111 and BTS 116
* "save" only saved configs on the first server of a multiserver config when both instances of dynamips were running on the same system
* fixed NPE-G2 with ghostios bug
* Other misc general error handling and message improvements

Version 0.9.0
* Added packet capture, via the "capture" command. Capture files are written to the host on which the dynamips server is running in PCAP format (i.e. can be opened with tcpdump, Wireshark, etc.)
* Added support for all the new 2600 models Chris added in 0.2.7.
* Added support for sparsemem. Enable with "sparsemem = true" at either the top level of the network file or in the device defaults or device section
* New adapters for 7200s: PA-2FE-TX, PA-GE, C7200-IO-2FE, C7200-IO-GE-E. Specify the new IO cards with "slot0" options, and the new adapters with "slotx" options, where x is 1-6.
* New NPEs for 7200s: npe-g1, npe-g2

Version 0.8.3
* Added a "--notelnet" command line option to make integration with gDynagen easier. See http://gdynagen.sourceforge.net

Version 0.8.2
* Ghost instances are now deleted once the mmap file has been created. This means there is no longer a ghost instance consuming process VM space.
* Ghost size is automatically calculated. Use of the "ghostsize" option should no longer be necessary. Thanks to this and the previous bugfix, I don't think there are any situations (other than using compressed images) that should cause ghostios to break otherwise functioning labs.
* When using multiple dynamips servers running on the same host, ghost files are shared among the dynamips processes if possible.
* Added "idlemax", "idlesleep', and "showdrift" idlepc commands for advanced manipulation and diagnostics of idlepc. Added "idlemax" and "idlesleep" network file options to go along with the CLI commands. The network file options aren't supported with in dynamips yet (as of 0.2.6-RC4), so don't try to use them.
* Rewrote send() to fix BTS #94.
* Added check for non-running routers in telnet command. BTS #102

Version 0.8.1
* So, as great as the Ghost RAM feature is, it does have the potential to break existing labs (for example, if the lab uses compressed images.) So for safety and to preserve backwards compatibility ghostios now defaults to False. You can turn it on with "ghostios = true" in either the router definition, the device defaults section, or at the top level of your network file. As usual, see all_config_options.txt for more info.
* Fixed bug that caused crash when using ghostios and image paths that do not include any directory separator characters.
* Trying to manually start a nonexistent router caused dynagen to crash.
* Ghost instances are only created if two or more routers on the same dynamips host use the same IOS image. This optimization eliminates unnecessary host virtual memory consumption, so as not to run into process vm size limits unnecessarily.
* Added an option to manually tweak the virtual ram allocated to Ghost images. Set this with "ghostsize = ..." in either the router definition, the device defaults section, or at the top level of your network file. The default is whatever that class of router would normally use.

Version 0.8.0
* 2691, 3725, and 3745 support. Usage is as you would expect, but see all_config_options.txt for documentation.
* Support for the IOS ghosting feature added in 0.2.6-RC3. IOS ghosting takes advantage of the mmap() "MAP_PRIVATE" flag to allocate a shared memory mapped file for IOS images. So instead of each virtual router storing an identical copy of IOS in its virtual RAM, the host will allocate one shared region of memory that they will all share. If you are running 10 routers all with the same IOS image, and that image is 60 MB in size you will save 9*60 = 540 MB of real RAM when running your lab with this feature. If you are using mmap (which is on by default) then IOS ghosting will automatically be implemented and you don't need to make any changes to your labs to take advantage of it. You can turn it off on a per router (or per device default section) with "ghostios = False" if you so desire. If you are using more than one IOS image in your lab then the feature still works, but the sharing will only occur among routers that are using the same image. The ghost file created is based on the name of your IOS image, so be sure that all your images have different names in a given lab (all the more reason to use the image naming convention recommended in the tutorial.)
* Corrected some minor typos in all_config_options.txt (thanks Dmitry M)
* Added error checks for malformed or non-existent devices specified in push/save/import/export commands. BTS #94
* ctrl-c then return now exits the CLI instead of crashing. BTS #89
* With RC3 push / extract are much improved so import/export/push/save should all work much better. I removed the workaround code that ensured routers were started before push / extract operations since that is no longer necessary with 0.2.6-RC3.
* The Windows installer no longer overwrites dynagen.ini if it exists (so as not to obliterate customizations). In all cases it creates a file dynagen.ini.new that might contain additional options. You should manually compare your dynagen.ini and this file to see if any of the new options are useful to you.

Version 0.7.0
* Added idlepc commands, for generating, testing, and saving idlepc values from Dynagen. See the tutorial for example usage.
* Also includes a system for maintaining your idlepc values in a "database" indexed by the image name. Again, see the tutorial for an example of how to use this feature.
* Added import / export CLI commands that store / retrieve IOS configs in a directory. Can be used as an alternative to save / push for packaging up labs, for creating "snapshots" for later retrieval, importing configurations from "the real world", etc. Note this feature is experimental and is still being refined. Garbled import / exports have been observed. (Thanks to "solo" for assistance with patch).
* Network files and CLI commands (should) now also support two letter interface type designations (e.g. Fa0/1 or. F0/1)
* Added "send" CLI command for sending raw hypervisor commands. Here is some rope, try not to hang yourself with it...
* Dynagen checks for console selection conflicts. BTS #92
* Added a "debug" top level option to turn on debugging from network files. Usage is "debug = " and a number from 0 - 9. Right now 0 means disabled, 1 means the same thing as using the -d command line switch, and 2 - 3 provide increasing levels of debugging verbosity
* Added a udp option to dynagen.ini to set the base udp NIO port. Can still be overridden in the network file.
* Fixed bug using "-n" option that caused dynamips to crash
* Trying to use iomem option resulted in "invalid iomem type, must be an integer". Fixed.
* Fixed bug parsing bad interfaces on filter command
* Fixed a bug in the "save" command that sometimes wrote the configuration in the wrong network file section
* Fixed bug that caused save command to crash dynagen when the port was specified in the dynamips server section BTS #73
* Fixed bug that caused some hypervisor commands that returned errors to cause a hang
* Due to some Dynamips / Dynagen "branding" confusion, the Start menu folder is now named "Dynagen". You may want to manually delete the old "Dynamips" program group. The programs are still installed in C:\Program Files\Dynamips for now.
* Windows uninstaller now correctly deletes all files except the Images directory (for safety)
* The dynamips.exe included with the Windows installer package is now built against Winpcap 4.0 beta 2. It doesn't seem to be necessary to upgrade from previous betas to use, but you might wish to anyway.

Version 0.6.0
* Added support for NM-16ESW. Specify with "slotx = NM-16ESW"
* Added "save" / "push" CLI commands for storing IOS configurations in network files. Pretty experimental, and currently only works with 7200s.
* Added support for dynamips filters with the "filter" CLI command. See the online help for usage.
* "ver" CLI command now also shows dynamips server version(s)
* Fixed command line switch bug that falsely reported crashes. BTS #66
* Fixed a bug that prevented manually specifying NM-4T and NM-4E on 3620s and 3640s
* Dynagen should now function on Windows 2000 after replacing dynamips.exe and cygwin1.dll with the ones compiled against Windows 2000 (downloaded from the dynamips site)

Version 0.5.2
* Fixed a bug that broke model selection on non US OSs that represented strings as Unicode.
* Only the first 4 interfaces of a PA-8E were usable.
* Pause if the Dynagen crashes so the user can see the Python traceback for support purposes. No more "I click on a net file, Dynagen flashes and goes away."
* Gracefully handle a malformed section rather than crash
* Crashed poorly if it couldn't find the network file. BTS #62
* Eliminated the depreciated "ROM" option and associated library support. BTS #61
* Gracefully handle attempts to establish connections to nonexistant devices
* Defining a switchport but not using it now just issues a warning and continues
* Console "ver" command also shows the version(s) of the dynamips server(s)
* Added iomem config option to set the iomem size on 3600s

Version 0.5.1:
* Fixed many occurrences of a stupid "s/false/False" typo
* Corrected the bug that prevented the manual specification of "NM-4T"

Version 0.5.0:
* 3620, 3640, and 3660 router support for use with dynamips 0.2.5-RC4 and later. See all_config_options.txt and the tutorial for usage.
* Simpler syntax for specifying dynamips server control port makes using multiple dynamips processes on the same server easier. See the FAQ in the tutorial for an example.
* Added a setup.py for unix installations and dynagen now looks in "unix friendly" places (i.e. /etc and /usr/local/etc) as well as the same directory as dynagen for dynagen.ini and CONFSPEC (thanks for Erik Wenzel for providing patches!)
* Dynamips 0.2.5-RC4 and later uses a new hypervisor syntax for many commands, so that version of Dynamips or later requires Dynagen 0.4.4 or later, and vice versa.
* Dynamips for Windows/Cygwin now requires Winpcap 4.0 (currently in beta)
* Dynamips 0.2.5 now uses the router name in the nvram, bootflash, logfiles etc. This means that when existing Dynagen labs are changed, nvram files will continue to match the correct router. However it also means that labs made with previous versions that use instance ID will be incompatible. To convert old lab data to the new format, you can manually rename nvram, disk, bootflash, etc files from c7200_ix_blah (where x is the instance id) to c7200_routername_blah (where routername is the name of the router as defined in the dynagen lab).

Version 0.4.3:
* Added "disk0" and "disk1" options to set the ATA sizes (set to 0 for none) (BTS #49)
* Added a "udp" option to change the default starting UDP port for UDP NIOs
* Added "show mac <switchname>" and "clear mac <switchname>" CLI commands to support the new dynamips hypervisor commands that show / clear Ethernet switch mac address tables
* Supports spaces in filespec (e.g. with "workingdir", "image", etc.). Because of this change, dynagen 0.4.3 now requires dynamips 0.2.5-RC2 or later which added this feature.
* mmap now defaults to true, to match the default behavior of dynamips. This causes dynamips to use disk files for router virtual memory rather than RAM. To return to the previous behavior, set "mmap = false" in your [[7200]] sections.  (BTS #41)
* Fixed several connect bugs relating to connections between devices distributed across multiple dynamips instances on the same or different servers
* Fixed a bug in exec_area that caused it to botch the idlepc value instead (BTS #46)
* Fixed a bug in ETHSW config that prevented the use of any manual NIO other than NIO_gen_eth

Version 0.4.2:
* Removed "clock" option from labs and the tutorial, because as of dynamips 0.2.5 RC1 the clock skew is automatically calculated (yay!)

Version 0.4.1:
* Added "idlepc" and "exec_area" options. idlepc was introduced in 0.2.5-pre25, see the dynamips web site or the dynamips readme for usage

Version 0.4.0:
* Implicit distributed Dynamips server support. (BTS #12) See multiserver sample lab.
* Added Ethernet switch support (introduced in dynamips 0.2.5-pre22). See ethernet_switch sample lab.
* Added a telnet command to launch connections to router consoles from the CLI (BTS #12). Added dynagen.ini file to support this feature. The "telnet" option in the INI specifies the telnet client to launch and needs to be customized for your OS (see examples for Windows, Linux, and OS X)
* Fixed the frame-relay lab (missing [[7200]] section. Doh!)
* Fixed NIO_vde issue (BTS #25)

Open Caveats
============
See the Bug Tracking System at http://www.ipflow.utc.fr/bts/ for a list of open issues.


Greg Anuzelli (dynagen@gmail.com)
