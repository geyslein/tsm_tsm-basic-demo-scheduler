#!/usr/bin/env python

import time
import sys
import warnings
import logging

logging.basicConfig(level="DEBUG")

n = 10
args = sys.argv[1:]
if args:
    n = int(args[0])

if n > 60:
    warnings.warn("job will need > 1min")

print(f"sleep {n} seconds")
for i in range(n):
    msg = f"sec: {i}"
    logging.warning(msg)
    print(msg)
    time.sleep(1)
