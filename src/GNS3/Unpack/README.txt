================================
Cisco binary image unpacker v0.1
================================

Cisco binary image unpacker is a software that allows you to unpack IOS and ASA images.

Usage: unpack [--output file] [--format <IOS|ASA7|ASA8> ] <binary image>

Important notice: ASA v7 images can be used in GNS3 and Pemu. At the moment ASA v8 images run only with Qemu.

=============================================
How to unpack ASA version 7 and early images?
=============================================

Images tested: asa722-k8.bin asa724-k8.bin

[Linux]

$ python unpack.py --format ASA7 asa724-k8.bin 
Archive:  /tmp/asa724-k8.bin.zip
inflating: /tmp/pix
ASA7 binary image successfully unpacked in asa724-k8.bin.unpacked

[Windows]

C:\Unpack>unpack.exe --format ASA7 asa724-k8.bin
Archive:  c:/docume~1/admini~1/locals~1/temp/asa724-k8.bin.zip
inflating: c:/docume~1/admini~1/locals~1/temp/pix
ASA7 binary image successfully unpacked in asa724-k8.bin.unpacked

Then you just need to use asa724-k8.bin.unpacked in GNS3 or Pemu as a PIX image.

===================================
How to unpack ASA version 8 images?
===================================

Image tested: asa802-k8.bin

[Linux]

$ python unpack.py --format ASA8 asa802-k8.bin
gzip: /tmp/asa802-k8.bin.gz: decompression OK, trailing garbage ignored
cpio: Removing leading `/' from member names
cpio: dev/console: Cannot mknod: Operation not permitted
cpio: dev/ram0: Cannot mknod: Operation not permitted
cpio: dev/mem: Cannot mknod: Operation not permitted
cpio: dev/kmem: Cannot mknod: Operation not permitted
cpio: dev/null: Cannot mknod: Operation not permitted
cpio: dev/port: Cannot mknod: Operation not permitted
cpio: dev/hda: Cannot mknod: Operation not permitted
cpio: dev/hda1: Cannot mknod: Operation not permitted
cpio: dev/hda2: Cannot mknod: Operation not permitted
cpio: dev/hda3: Cannot mknod: Operation not permitted
cpio: dev/hdb: Cannot mknod: Operation not permitted
cpio: dev/hdb1: Cannot mknod: Operation not permitted
cpio: dev/hdb2: Cannot mknod: Operation not permitted
cpio: dev/hdb3: Cannot mknod: Operation not permitted
cpio: dev/ttyS0: Cannot mknod: Operation not permitted
cpio: dev/ttyS1: Cannot mknod: Operation not permitted
cpio: dev/net/tun: Cannot mknod: Operation not permitted
61039 blocks
ASA8 initrd successfully unpacked in asa802-k8.bin.unpacked.initrd
ASA8 kernel successfully unpacked in asa802-k8.bin.unpacked.vmlinuz

[Windows]

C:\Unpack>unpack.exe --format ASA8 asa802-k8.bin

gzip: c:\docume~1\admini~1\locals~1\temp\asa802-k8.bin.gz: decompression OK, trailing garbage ignored
cpio: Removing leading `/' from member names
cpio: vmlinuz: Function not implemented
...
61039 blocks
ASA8 initrd successfully unpacked in asa802-k8.bin.unpacked.initrd
ASA8 kernel successfully unpacked in asa802-k8.bin.unpacked.vmlinuz

Create a FLASH file with the follwing command: "qemu-img create FLASH 256M"

Then you can use Qemu to launch ASA:

$qemu -hda FLASH -hdachs 980,16,32 -kernel asa802-k8.bin.unpacked.vmlinuz -initrd asa802-k8.bin.unpacked -m 256 --no-kqemu 
-append "auto nousb ide1=noprobe bigphysarea=16384 console=ttyS0,9600n8 hda=980,16,32" -serial telnet::15000,server,nowait

Finally start telnet to connect on port 15000:

$telnet localhost 15000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.

ciscoasa> show version

Cisco Adaptive Security Appliance Software Version 8.0(2) 

Compiled on Fri 15-Jun-07 19:29 by builders
System image file is "Unknown, monitor mode tftp booted image"
Config file at boot was "startup-config"

ciscoasa up 17 secs

Hardware:   , 128 MB RAM, CPU Pentium II 2394 MHz
Internal ATA Compact Flash, 256MB
BIOS Flash Firmware Hub @ 0xffe00000, 1024KB

 0: Ext: Ethernet0/0         : irq 255
 1: Ext: Ethernet0/1         : irq 255
 2: Ext: Ethernet0/2         : irq 255
 3: Ext: Ethernet0/3         : irq 255
 4: Ext: Ethernet0/4         : irq 255
 5: Ext: Ethernet0/5         : irq 255
VLANs                        : 200
Failover                     : Active/Active
3DES-AES                     : Enabled
Security Contexts            : 20
GTP/GPRS                     : Enabled
VPN Peers                    : 5000
WebVPN Peers                 : 2500
ADV END SEC                  : Enabled
              
Serial Number: 123456789AB
Running Activation Key: 0x00000000 0x00000000 0x00000000 0x00000000 0x00000000 
Configuration register is 0x0
Configuration has not been modified since last system restart.
ciscoasa>

=========================
How to unpack IOS images?
=========================

[Linux]

$ python unpack.py --format IOS 
c2600-is-mz.122-46.bin 
warning [c2600-is-mz.122-46.bin]:  17732 extra bytes at beginning or within zipfile
(attempting to process anyway)
IOS binary image successfully unpacked in c2600-is-mz.122-46.bin.unpacked

[Windows]

C:\Unpack>unpack.exe --format IOS c2600-is-mz.122-46.bin
warning [c2600-is-mz.122-46.bin]:  17732 extra bytes at beginning or within zipfile
(attempting to process anyway)
IOS binary image successfully unpacked in c2600-is-mz.122-46.bin.unpacked

Then you can use the image in GNS3 and dynamips.
