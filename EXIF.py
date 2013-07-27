#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Library to extract Exif information from digital camera image files.
# https://github.com/ianare/exif-py
#
#
# VERSION 1.3.0
#
# Copyright (c) 2002-2007 Gene Cash
# Copyright (c) 2007-2013 Ianaré Sévi and contributors
#
# See LICENSE.txt file for licensing information
# See 'CHANGES.txt' file for all contributors and changes
#

import sys
import getopt
import logging
from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
from exifread import process_file

def usage(exit_status):
    """Show command line usage."""
    msg = 'Usage: EXIF.py [OPTIONS] file1 [file2 ...]\n'
    msg += 'Extract EXIF information from digital camera image files.\n\nOptions:\n'
    msg += '-q --quick   Do not process MakerNotes.\n'
    msg += '-t TAG --stop-tag TAG   Stop processing when this tag is retrieved.\n'
    msg += '-s --strict   Run in strict mode (stop on errors).\n'
    msg += '-d --debug   Run in debug mode (display extra info).\n'
    print(msg)
    sys.exit(exit_status)

def main():
    # parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hqsdct:v", ["help", "quick", "strict", "debug", "stop-tag="])
    except getopt.GetoptError:
        usage(2)
    if args == []:
        usage(2)
    detailed = True
    stop_tag = DEFAULT_STOP_TAG
    debug = False
    strict = False
    color = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage(0)
        if o in ("-q", "--quick"):
            detailed = False
        if o in ("-t", "--stop-tag"):
            stop_tag = a
        if o in ("-s", "--strict"):
            strict = True
        if o in ("-d", "--debug"):
            debug = True

    ## Configure the logger
    if debug:
        level = logging.DEBUG
        log_format = '%(levelname)s - %(message)s'
    else:
        level = logging.INFO
        log_format = '%(message)s'

    logger = logging.getLogger('exifread')
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(log_format))
    logger.setLevel(level)
    ch.setLevel(level)
    logger.addHandler(ch)

    # output info for each file
    for filename in args:
        try:
            file = open(str(filename), 'rb')
        except:
            logger.error("'%s' is unreadable", filename)
            continue
        logger.info(filename)
        # get the tags
        data = process_file(file, stop_tag=stop_tag, details=detailed, strict=strict, debug=debug)
        if not data:
            logger.warning('No EXIF information found')
            continue

        x = data.keys()
        x.sort()
        for i in x:
            if i in ('JPEGThumbnail', 'TIFFThumbnail'):
                continue
            try:
                logger.info('%s (%s): %s', i, FIELD_TYPES[data[i].field_type][2], data[i].printable)
            except:
                logger.error("%s : %s", i, str(data[i]))
        if 'JPEGThumbnail' in data:
            logger.info('File has JPEG thumbnail')


if __name__ == '__main__':
    main()
