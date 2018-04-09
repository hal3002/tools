#!/usr/bin/env python

import base64
import re
import sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-n", "--min", dest="minimum_length", help="Minimum base64 string length (Default: 4)", default=4, type=int)
(options, args) = parser.parse_args()

for m in re.findall("(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?", sys.stdin.read(), re.IGNORECASE):
    if len(m) > options.minimum_length:
        try:
            print base64.b64decode(m)
        except TypeError:
            pass
