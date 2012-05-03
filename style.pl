#!/usr/bin/env perl
#
# Copyright (C) 2012 - GNS3 development team
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED ``AS IS'' AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

# Fixes coding style
# http://redmine.gns3.net/projects/gns3-devel/wiki/CodingStyle
# This tool is not part of the GNS3 distribution

# find . \! -path "*build*" \! -path "*Ui*" -name "*.py" -exec ./style.pl {} \;

use strict;
use warnings;

my $style_utf8 = '# -*- coding: utf-8 -*-' . "\n";
my $style_tabs = '# vim: expandtab ts=4 sw=4 sts=4:' . "\n";
my $style_modeline = '# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:' . "\n";

my @toremove = ($style_utf8, $style_tabs);
my @header = ($style_modeline);

if (scalar(@ARGV) < 1)
{
        print STDERR "usage: $0 <file.py> [...]\n";
        exit 1;
}

sub strip_data
{
        my $data = shift;
        foreach (@toremove)
        {
                if ("$_" eq "$data")
                {
                        return "";
                }
        }
        return $data;
}

foreach (@ARGV)
{
        my $filename = $_ . ".style";
        rename $_, $filename or die "rename $_, $filename: $!.\n";
        open IFILE, $filename or die "open $filename: $!.\n";
        open OFILE, ">", $_ or die "open $_: $!.\n";
        my @data = <IFILE>;
        close IFILE;

        my @clean_data = map { s/\r\n/\n/g; $_; } @data;
        @clean_data = map { strip_data($_) } @clean_data;
        my $idx = 0;
        if (scalar(@clean_data) > 1 && $data[0] =~ m/^\#\!/)
        {
                $idx = 1;
        }
        foreach (@clean_data)
        {
                $_ =~ s/\s+\n$/\n/;
                my $line = $_;
                my $i = 0;
                foreach (@header)
                {
                        if ("$_" eq "$line")
                        {
                                splice @header, $i, 1;
                        }
                        else
                        {
                                $i = $i + 1;
                        }
                }
        }
        foreach (@header)
        {
                splice @clean_data, $idx, 0, $_;
        }
        foreach (@clean_data)
        {
                print OFILE $_;
        }
        unlink $filename;
        close OFILE;
}
