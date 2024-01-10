#!/usr/bin/env python
import gzip, time, numbers, json
from os import listdir
from parsers import parse_minidexed

user = {}

config = open("../lemons.json", "r")
conf = json.load(config)['local']
config.close()
#print('conf', conf)


# For pretty json indent = 2
# for compact json indent = None
indent = 2 #None

if __name__ == "__main__":

    #minidexed =  parse_ini(paths['performance'])
    print("------------ convert minidexed.ini to json ---------------")
    # Open original
    ini_file = open(conf['rootPath'] + conf['minidexed'], "r")
    txt = ini_file.readlines()
    ini_file.close()
    txt[3] = '\nUSBGadget=0\n' # insert USBGadget param
    
    #print(txt)
    
    conf_orig = parse_minidexed(txt)
    conf = conf_orig

    user_ini = []
    # Apply user config to ini
    for i in txt:

        #user_ini.append(i)
        
        if(i[0:1] == '#' or i == '\n'): #, i[0:2] == '\n'
            user_ini.append(i)
            #print('--pass',i)
        else:
            '''
            print('++ ',i)
        
            for i in user:
                #print('user: ', i, user[i])
                #{ "val":"48000", "type":"select", "vals":{} }

                # TXT
                orig = i + '=' + conf[i]['val']
                usr = i + '=' + user[i]
                i = i.replace(orig, usr)
                print('-orig,usr,i',orig,usr,i)
'''
            user_ini.append(i)
        
    # Create a copy with user config applied
    #ini_file = open('../minidexed.ini', "w")
    #_txt = ini_file.writelines(user_ini)
    #ini_file.close()

                #words = txt
                #words = [word.replace(orig,usr) for word in words]

            #part = i.split('=')
            #dat['ini'][part[0]] = part[1]
            #dat['ops'][part[0]] = {'type':'select', 'vals':{}}
            
            #dat[part[0]] = { 'val': part[1], 'type': 'select', 'vals': {} }

    # Apply user config to json
    for i in user:
        # JSON
        conf[i]['val'] = user[i] #{ 'val': defaults[i], 'type': 'select', 'vals': {} }

        #print('orig:',orig, 'usr:',usr)
    #print('words:',words)
    #user[i]

    indent = 2    
    data = json.dumps(conf, indent=indent, separators=(',', ':'))
    jsn = open('../www/minidexed.json', "w")
    jsn.write(data)
    jsn.close()

    indent = None
    data = json.dumps(conf, indent=indent, separators=(',', ':'))
    gz = open('../PicoW/minidexed.json.gz', mode='wb')
    gzdat = gzip.compress(data.encode(), compresslevel=9, mtime=time.time())
    gz.write(gzdat)
    gz.close()

    print('minidexed.ini saved in ../www/minidexed.json and ../Picow/minidexed.json.gz')
