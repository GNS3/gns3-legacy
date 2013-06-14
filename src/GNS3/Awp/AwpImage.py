# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

import struct
import os

def awp_image_parse(rel_file, output_path, img_path_dict):
    """
    Implementation of a parser that extracts kernel image and initrd
    from the given .rel file.
    Return a dictionary containing the path to the extracted files.
    """

    rel_name = os.path.splitext(os.path.basename(rel_file))[0]
    
    # parse release header
    file = open(rel_file, "rb")
    file.seek(24)
    kernelo = struct.unpack('>i', file.read(4))[0]
    file.seek(28)
    kernels = struct.unpack('>i', file.read(4))[0]
    file.seek(48)
    initrdo = struct.unpack('>i', file.read(4))[0]
    file.seek(52)
    initrds = struct.unpack('>i', file.read(4))[0]

    # create kernel image
    kernel = output_path + os.sep + rel_name + '-bzImage'
    file.seek(kernelo)
    kernel_img = file.read(kernels)
    output = open(kernel, 'wb')
    output.write(kernel_img)
    output.close()

    # create initrd
    initrd = output_path + os.sep + rel_name + '-initrd'
    file.seek(initrdo)
    initrd_img = file.read(initrds)
    output = open(initrd, 'wb')
    output.write(initrd_img)
    output.close()

    img_path_dict['kernel'] = kernel
    img_path_dict['initrd'] = initrd

    file.close()
