#!/usr/bin/env python
import gzip, time, numbers, json
from os import listdir
from parsers import get_inis, parse_ini


config = open("../lemons.json", "r")
conf = json.load(config)['local']
config.close()

# For pretty json indent = 2
# for compact json indent = None
indent = 2 #None

if __name__ == "__main__":

    #minidexed =  parse_ini(paths['performance'])
    print("------------ convert performance.ini to json ---------------")

    performance = parse_ini(conf['rootPath'] + conf['performance']) # parse_ini(paths['performance'])

    indent = 2    
    data = json.dumps(performance, indent=indent, separators=(',', ':'))
    jsn = open('../www/performance.json', "w")
    jsn.write(data)
    jsn.close()

    indent = None
    data = json.dumps(performance, indent=indent, separators=(',', ':'))
    gz = open('../PicoW/performance.json.gz', mode='wb')
    gzdat = gzip.compress(data.encode(), compresslevel=9, mtime=time.time())
    gz.write(gzdat)
    gz.close()
    print('Performance saved in ../www/performance.json and ../Picow/performance.json.gz')


    print("------------ convert performance/*.ini to json ---------------")

    indent = None
    payload = {}
    perfs = conf['rootPath'] + conf['performances'] #paths['performances']
    #print(perfs)
    inis = get_inis(perfs)
    #print(inis)

    #ini = open("performance.json", "r")
    #jsn = ini.readlines()
    #data['000001_performace.ini'] = json.loads(jsn)
    #ini.close()
    
    for i in inis:
        #{ _id: { 'id':id, 'file':i, 'name':name, 'size':0, 'data':{} }
        _dat = inis[i]
        ini = perfs + '/' + _dat['file']
        _dat['data'] = parse_ini(ini)
        payload[i] = _dat
        #print('i',i, inis[i], ini)
        #pass#
        #print(i)
        #print(i['ini'], i['jsn'])
        #dat = parse_ini(i['ini'], i['jsn'])
        #dat = parse_ini(i['ini'])
        #file = i['ini'].split('/')
        #data[file[-1]] = dat

    indent = 2    
    data = json.dumps(payload, indent=indent, separators=(',', ':'))
    jsn = open('../www/performances.json', "w")
    jsn.write(data)
    jsn.close()

    indent = None
    data = json.dumps(payload, indent=indent, separators=(',', ':'))
    gz = open('../PicoW/performances.json.gz', mode='wb')
    gzdat = gzip.compress(data.encode(), compresslevel=9, mtime=time.time())
    gz.write(gzdat)
    gz.close()

    print('Performances saved in ../www/performances.json and ../Picow/performances.json.gz')
