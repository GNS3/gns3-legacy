# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2012 GNS3 Development Team (http://www.gns3.net/team).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# http://www.gns3.net/contact
#

# Functions to uncompress IOS images

import os, mmap, zipfile, shutil, tempfile


def isIOScompressed(ios_image):
    """ Check either a IOS image is compress or not
        Returns True if compressed
    """

    fd = open(ios_image, 'r+b')
    mapped_file = mmap.mmap(fd.fileno(), 0)

    # look for ZIP 'end of central directory' signature
    pos = mapped_file.rfind('\x50\x4b\x05\x06')

    # look for another ZIP 'end of central directory' signature
    # if we find one it means the IOS image itself contains zipped files
    multiple_zipped_files = mapped_file.find('\x50\x4b\x05\x06', 0, pos)

    # let's find the 'CISCO SYSTEMS' string between our last signature and the end of our file
    # so we can know the IOS image is compressed even if there are other ZIP signatures in our file
    cisco_string = mapped_file.find('\x43\x49\x53\x43\x4F\x20\x53\x59\x53\x54\x45\x4D\x53', pos + 4)

    mapped_file.close()
    fd.close()

    # finding the signature and not recognized as a regular zip file means IOS is compressed
    #if (pos > 0 and not zipfile.is_zipfile(ios_image)) and not (multiple_zipped_files > 0 and not cisco_string > 0):
    # issue: zipfile.is_zipfile now returns True in Python 2.7.3, let's try without it ...
    if pos > 0 and not (multiple_zipped_files > 0 and not cisco_string > 0):
        return True
    return False


def uncompressIOS(ios_image, dest_file):

    # we don't touch the original image
    tmp_fd = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfile(ios_image, tmp_fd.name)
    data = tmp_fd.read()

    # look for ZIP 'end of central directory' signature
    pos = data.rfind('\x50\x4b\x05\x06')
    if pos > 0:
        # size of 'ZIP end of central directory record'
        tmp_fd.seek(pos + 22)
        # this make a clean zipped file
        tmp_fd.truncate()

    # uncompress the IOS image
    is_zipfile = zipfile.is_zipfile(tmp_fd.name)
    if is_zipfile:
        zip_file = zipfile.ZipFile(tmp_fd.name, 'r')
        for member in zip_file.namelist():
            source = zip_file.open(member)
            target = file(dest_file, "wb")
            shutil.copyfileobj(source, target)
            source.close()
            target.close()
        zip_file.close()
    try:
        tmp_fd.close()
        os.remove(tmp_fd.name)
    except:
        pass

if __name__ == '__main__':

    # for testing
    image = '/Users/grossmj/Public/GNS3 Test Kit/c2600-i-mz.122-5d.bin'
    extracted_image = '/tmp/c2600.image'
    print isIOScompressed(image)
    uncompressIOS(image, extracted_image)
    print isIOScompressed(extracted_image)
