from os import listdir

def get_inis(inis_path):
    inis = {}
    files = listdir(inis_path)
    for i in files:
        id = i[0:6]
        ext = i[-4:]
        name = i[7:-4]
        if ext == '.ini':
            _id = int(id)
            inis[_id] = { 'id':id, 'file':i, 'name':name, 'size':0, 'data':{} }
    return inis


def get_voices(voxs_path):
    voxs = {}
    files = listdir(voxs_path)
    for i in files:
        id = i[0:6]
        ext = i[-4:]
        name = i[7:-4]
        if ext == '.syx':
            _id = int(id)
            voxs[_id] = { 'id':id, 'file':i, 'name':name, 'size':0, 'data':{} }

    return voxs

'''
    performance/s .ini parser
'''
def parse_ini(ini_file):
    #def toJson(ini_file, json_file):
    
    ini = open(ini_file, "r")
    txt = ini.readlines()
    ini.close()

    dat = { '0':{}, '1':{}, '2':{}, '3':{}, '4':{}, '5':{}, '6':{},  '7':{}, '8':{} }

    for i in txt:
        i = i.strip().replace('\n', '')
        
        #if i[:1] == '#' or i[:1] == '' or i[:2] == '\n': # skip comments and empty lines
        if i[0:1] == '#' or i == '': # skip comments and empty lines // i[0:2] == '\n'
            pass
        else:
            #print('i',i)
            part = i.split('=')
            key = part[0][-1:]
            name = part[0]
            _name = part[0][:-1]
            value = part[1].strip() #print(key.isnumeric(), key, name, value, part)
            if key.isnumeric(): #check if numeric, then tg
                dat[key][_name] = value
            else: # else fx
                dat['0'][name] = value

    # Write individual files
    #jsn = open(json_file, "w")
    #jsn.write(json.dumps(dat, indent=indent, separators=(',', ':')))
    #jsn.close()

    return dat



'''
    minidexed .ini parser
'''
def parse_minidexed(txt):

    #dat = { 'ini':{}, 'ops':{} }
    dat = {}


    for i in txt:
        i = i.replace('\n', '')
        c = 0
        if i == '' or i == '\n': # skip comments and empty lines
            pass
        elif(i[0:1] == '#'):
            #dat['comment_' + str(c)] = i
            c = c + 1
        else:
            part = i.split('=')
            #dat['ini'][part[0]] = part[1]
            #dat['ops'][part[0]] = {'type':'select', 'vals':{}}
            #print(part)
            
            dat[part[0]] = { 'val': part[1], 'type': 'select', 'vals': {} }

    # Apply corrections:
    dat['USBGadget']['vals'] = ['0','1']
    dat['USBGadget']['type'] = 'switch'
            
    dat['SoundDevice']['vals'] = ['hdmi','i2s', 'pwm']
    
    dat['SampleRate']['vals'] = ['44100','48000']
    
    dat['DACI2CAddress']['vals'] = ['0','1']
    dat['DACI2CAddress']['type'] = 'switch'

    dat['ChannelsSwapped']['vals'] = ['0','1']
    dat['ChannelsSwapped']['type'] = 'switch'
    
    dat['EngineType']['vals'] = { '1':'Modern', '2':'Mark I', '3':'OPL'}

    dat['MIDIBaudRate']['vals'] = ['31250','115200', '256000']

    dat['IgnoreAllNotesOff']['vals'] = ['0','1']
    dat['IgnoreAllNotesOff']['type'] = 'switch'
    
    dat['MIDIAutoVoiceDumpOnPC']['vals'] = ['0','1']
    dat['MIDIAutoVoiceDumpOnPC']['type'] = 'switch'

    dat['HeaderlessSysExVoices']['vals'] = ['0','1']
    dat['HeaderlessSysExVoices']['type'] = 'switch'

    dat['MIDIRXProgramChange']['vals'] = ['0','1']
    dat['MIDIRXProgramChange']['type'] = 'switch'

    dat['ExpandPCAcrossBanks']['vals'] = ['0','1']
    dat['ExpandPCAcrossBanks']['type'] = 'switch'

    dat['PerformanceSelectChannel']['vals'] = ['0','1']
    dat['PerformanceSelectChannel']['type'] = 'switch'





    # todo more




    dat['LCDI2CAddress']['vals'] = ['0','0x27']






    return dat

#import sys
#from importlib import reload
#reload(sys)
#sys.setdefaultencoding('utf-8')

def extract_dx7_voices(file):
    voices = {} #voices = []
    syx = open(file, 'rb')
    header = 6
    offset = 118
    block = 128
    v = 1 # start voices from 1
    for i in range(0,32):
        syx.seek(header + offset + (i * block))
        dat = bytearray(syx.read(10))

        # count from 0
        #voices[i] = dat.decode('ascii') #.replace('\\',' ') voices[i] = voices.append(dat.decode('ascii')) #.replace('\\',' ')
        #voices[i] = dat
        if dat[8] == 0x9f:
            dat[8] = 0
        try:
            voices[i] = dat.decode('ascii')
            #voices[i] = dat.decode('utf-8')
            #voices[i] = { 'ascii': dat.decode('ascii'), 'utf-8': dat.decode('utf-8') } 
        except Exception as e:
            print("--Error:", file, e, dat)

        # count from 1
        #voices[v] = dat.decode('ascii')
        
        v = v + 1
    syx.close()
    return voices
