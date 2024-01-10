#!/usr/bin/env python
import gzip, json, os, time
#from sd_card_path import paths
from parsers import get_voices, extract_dx7_voices
# json indent spaces 2 or None
indent = None #2 # None


config = open("../lemons.json", "r")
conf = json.load(config)['local']
config.close()

vox_path = conf['rootPath'] + conf['voxs']
#print('vox_path', vox_path)

'''
    Some dirty names: (and utf chars?)
    Should it be normalised?

    "XyloHrdWd\\",
    "TorimLong\\",
    "Grinder 4\\",
    "Koto\\\\\\\\\\1",
    "SoftGuitr\\",
    "NylonPck3\\",
    "NylonBel3\\",
    "Sitar KC \\",
    "Chroma   \\",
    "Clavi 1  \\",
    "SqrThang2\\",
    "KillrD's5\\",
    "KilerD's2\\",
    "Bello 3\u007f \\",
    "Belashun \\",
    "RodeBell \\",
    "ChinezBls\\",
'''

if __name__ == '__main__':
    print("---------------- Extract Voices to json -------------------")

    voices = {}
    #_path = os.path.realpath(paths['voxs'])
    #files = os.listdir(_path)

    voxs = get_voices(vox_path)
    #print('files',files)

    c = 1 # start banks from 1, not 0
    for i in voxs:
        # voxs[_id] = { 'id':id, 'file':i, 'name':name, 'size':0, 'data':{} }
        #print(voxs[i])
        voxs[i]['data'] = extract_dx7_voices(vox_path + '/' + voxs[i]['file'])
        
        if i == 0: # @TODO tmp hack for banks
            print('-- @TODO report bug, tmp hack: dropping bank 0 so bank 1 becomes 0 and sending 0xb1 20 00 selects correct bank')
        else:
            voices[i-1] = voxs[i] #voices[i] = voxs[i]
        # Count from 0
        #voices[i] = voxs[i] #voices[i] = voxs[i]

        # Count from 1
        #voices[c] = voxs[i] #voices[i] = voxs[i]

        # _dat['data'] = parse_ini(ini)
        #    voices[file] = extract_dx7_voices(_path + '/' + file)
        c = c + 1


    indent=2
    data = json.dumps(voices, indent=indent, separators=(',', ':'))
    #jsn = open('../config/voxs.json', 'w')
    #jsn.write(data)
    #jsn.close()
    jsn = open('../www/voxs.json', 'w')
    jsn.write(data)
    jsn.close()

    indent=None
    data = json.dumps(voices, indent=indent, separators=(',', ':'))
    gz = open('../PicoW/voxs.json.gz', mode='wb')
    gzdat = gzip.compress(data.encode(), compresslevel=9, mtime=time.time())
    gz.write(gzdat)
    gz.close()

    #print('ungz:', gzip.decompress(gzdat).decode())
    
    print('Voices saved in ../www/voxs.json and ../PicoW/voxs.json.gz')

    # test
    #vox = extractVoices('000000_rom3a.syx')
    #print(json.dumps(vox, indent=indent, separators=(',', ':')))
