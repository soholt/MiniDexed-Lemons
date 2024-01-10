#!/usr/bin/env python
import gzip, time, numbers, json
from os import listdir

import sys
#from os.path import dirname
sys.path.append('./tools')
from parsers import get_inis, parse_ini


config = open("./lemons.json", "r")
conf = json.load(config)
config.close()

indent = 2    
data = json.dumps(conf, indent=indent, separators=(',', ':'))
jsn = open('./www/lemons.json', "w")
jsn.write(data)
jsn.close()

indent = None
data = json.dumps(conf, indent=indent, separators=(',', ':'))
gz = open('./PicoW/lemons.json.gz', mode='wb')
gzdat = gzip.compress(data.encode(), compresslevel=9, mtime=time.time())
gz.write(gzdat)
gz.close()

print('Lemons config saved in ./www/lemons.json and ./PicoW/lemons.json.gz')
print('Re-upload updated config to Pico W ./PicoW/lemons.json.gz')