# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
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
# By Jeremy GROSSMANN for the GNS3 project (www.gns3.net).
#

import sys, os
import tempfile, shutil
import subprocess as sub

pkzip_magic = '50 4b 03 04 14'
gzip_magic = '1f 8b 08 00 1d'

def find_offset(f, magic):

    pos = 0
    width=16

    if width > 4:
        spaceCol = width//2
    else:
        spaceCol = -1

    hexwidth = 3 * width
    if spaceCol != -1:
        hexwidth += 1

    while 1:
        buf = f.read(width)

        length = len(buf)
        if length == 0:
            return

        hex = ""
        for i in range(length):
            c = buf[i]
            if i == spaceCol:
                hex = hex + " "
            hex = hex + ("%02x" % ord(c)) + " "
        line = "%06x %-*s" % (pos, hexwidth, hex)
        if magic in line:
            offset = line.split(' ')[0]
            return (offset)
        pos = pos + length
    return (None)

def executeCommand(cmd):

    try:
        p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT, shell=True)
        outputlines = p.stdout.readlines()
        p.wait()
    except (OSError, IOError), e:
        print cmd + ': ' + e.strerror()
        return False
    for line in outputlines:
        print line.strip()
    return True

def unpackASA7(path, output):
    ''' Unpack ASA v7 and early binary images
    '''

    try:
        f = open(path, "rb")
    except IOError:
        print >>sys.stderr, "Couldn't open %s" % path
        return

    image_size = os.path.getsize(path)
    offset = find_offset(f, pkzip_magic)
    if offset:
        zip_offset = image_size - int(offset, 16)
        tempdir = tempfile.gettempdir()
        zipfile_path = tempdir + os.sep + os.path.basename(path) + '.zip'
        try:
            zipfile_fd = open(zipfile_path, "wb")
        except IOError:
            print >>sys.stderr, "Couldn't create %s" % zipfile_path
            return
        seek_offset = image_size - zip_offset
        f.seek(seek_offset)
        zipfile_fd.write(f.read())
        zipfile_fd.close()
        if executeCommand("unzip -jo %s -d %s" % (zipfile_path, tempdir)) == False:
            return
        shutil.move(tempdir + os.sep + 'pix', output)
        print "ASA7 binary image successfully unpacked in %s" % output
    else:
        print >>sys.stderr, "Couldn't find any ZIP header in %s" % path
    f.close()

def unpackASA8(path, output):
    ''' Unpack ASA v8 binary images
    '''

    try:
        f = open(path, "rb")
    except IOError:
        print >>sys.stderr, "Couldn't open %s" % path
        return

    image_size = os.path.getsize(path)
    offset = find_offset(f, gzip_magic)
    if offset:
        gzip_offset = image_size - int(offset, 16)
        tempdir = tempfile.gettempdir()
        cwd = os.getcwdu()
        gzipfile_path = tempdir + os.sep + os.path.basename(path) + '.gz'
        try:
            gzipfile_fd = open(gzipfile_path, "wb")
        except IOError:
            print >>sys.stderr, "Couldn't create %s" % gzipfile_path
            return
        seek_offset = image_size - gzip_offset
        f.seek(seek_offset)
        gzipfile_fd.write(f.read())
        gzipfile_fd.close()
        tmpdir = tempfile.mkdtemp()
        if sys.platform.startswith('win'):
            for file in ['cpio.exe', 'libiconv2.dll', 'libintl3.dll']:
                shutil.copy(file, tmpdir)
        os.chdir(tempdir)
        if executeCommand("gzip -fd %s" % gzipfile_path) == False:
            return
        os.chdir(tmpdir)
        if executeCommand("cpio -i --no-absolute-filenames --make-directories < %s" % gzipfile_path[:-3]) == False:
            return
        os.chdir(cwd)
        shutil.move(tmpdir + os.sep + 'vmlinuz', output + '.vmlinuz')
        if executeCommand("gzip %s" % gzipfile_path[:-3]) == False:
            return
        shutil.move(gzipfile_path, output + ".initrd")
        print "ASA8 initrd successfully unpacked in %s.initrd" % output
        print "ASA8 kernel successfully unpacked in %s.vmlinuz" % output
    else:
        print >>sys.stderr, "Couldn't find any ZIP header in %s" % path
    f.close()

def unpackIOS(path, output):
    ''' Unpack IOS binary images
    '''

    try:
        cmd = "unzip -p %s > %s" % (path, output)
        p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT, shell=True)
        outputlines = p.stdout.readlines()
        p.wait()
    except (OSError, IOError), e:
        print cmd + ': ' + e.strerror()
        return
    for line in outputlines:
        print line.strip()
    print "IOS binary image successfully unpacked in %s" % output

def usage():

    print '%s [--output file] [--format <IOS|ASA7|ASA8> ] <binary image>' % os.path.basename(sys.argv[0])

if __name__ == '__main__':

    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:f:", ["help", "output=", "format="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    output = None
    format = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-f", "--format"):
            format = a
        else:
            assert False, "unhandled option"

    if args and args[0]:
        path = args[0]
        if output == None:
            output = os.path.basename(path) + '.unpacked'
        if format == None:
            format = 'ASA7'
            print 'Warning: No format set, defaulted to ASA7'
        if format == 'ASA7':
            unpackASA7(path, output)
        elif format == 'ASA8':
            unpackASA8(path, output)
        elif format == 'IOS':
            unpackIOS(path, output)
        else:
            print >>sys.stderr, "Invalid format %s" % format
            usage()
            sys.exit(2)
    else:
        usage()
        sys.exit(2)


