#!/usr/bin/python

import sys
import re

pid = int(sys.argv[1])
f = open("/proc/%d/maps" % pid)

for line in f.readlines():
        m = re.search('^([0-9a-f]+)-([0-9a-f]+).*\[heap\]', line)

        if m:
                mem_start = int(m.group(1), 16)
                mem_end = int(m.group(2), 16)

                mem = open("/proc/%d/mem" % pid, "r")
                mem.seek(mem_start, 0)
                data = mem.read(mem_end - mem_start)
                print data

                mem.close()

f.close()
