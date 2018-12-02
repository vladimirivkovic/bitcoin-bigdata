#!/usr/bin/python

import json
import sys

txs = json.load(sys.stdin)

for tx in txs:
    outs = tx[u'out']
    for out in outs:
        print("%s\t%d" % (out[u'addr'], out[u'value']))
