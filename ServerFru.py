#!/usr/bin/env python
import os
import sys
from ctypes import *
from binascii import *

class Dbg(object):
	DEBUG=False

class Fru(object):
	codetype=0xC0

def Usage():
    usage = """ Usage: frutool -h|-stxt|-sbin|-w [file]|-r <length filename>
    -h: This help
    -w [file]: File data(fruconfig.ini or user defined) write to FRU
    -e <length>: Write "length" bytes of FRU ROM with 0xff,this will erase the FRU data
    -sbin: Read FRU data and show in hex format
    -stxt: Read FRU data and show in text format
    -offset: Read FRU data and show in text format with the item offset
    -r <size> <filename>: Read FRU data and write the data to file
    [Example]:
        frutool -r 0x800 fru.bin
        The "length" must less than 0x800
        Note:To re-burn a single item,please use following command,
        If the "string" has blank,it must be embodied with double quotation.
        if the "string" is not exist,it will show the single item only
        frutool <cmd> [string] 
        The "cmd" should be one of the following:
        /CPN     Chassis Part Number
        /CSN     Chassis Serial Number
        /BM      Board Manufacture
        /BMT     Board Manufacture date/time
        /BPNA    Board Product Name
        /BSN     Board Serial Number
        /BPNU    Board Part Number
        /BFFI    Board Fru File ID
        /PM      Product Manufacturer
        /PN      Product Name
        /PPN     Product Part/Mode Number
        /PV      Product Version
        /PSN     Product Serial Number
        /PAT     Product Asset Tag
        /PFFI    Product Fru File ID

        [Example]:to re-burn chassis part number
        frutool /CPN "123456789"

        [Example]:to show chassis part number only
        frutool /CPN

        [Example]:to re-burn board manufacture date/time
        frutool /BMT "2012-12-12 14:19:19"
    """
    print(usage)

def dump_fru_to_file(fru_buf, size=512, filename='./fru.bin'):
    start = 0
    if size > 2048:
        buf_size = 2048
    else:
        buf_size = size
    if os.path.exists(filename) == True:
        print("File %s is exist, do you want to cover it" % filename )
        Asr=input("yes/no: ")
        if Asr == 'no' or Asr == 'n':
            print("Please use a new file name !")
            sys.exit(4)
    fd=open(filename, mode='wb')
    #buf=create_string_buffer(buf_size)
    #hdl.readfru(buf, start, buf_size)
    fd.write(fru_buf.raw)
    fd.close()
    
def read_fru_test(fru_buf):
    start = 0
    size=512
    if size > 2048:
        buf_size = 2048
    else:
        buf_size = size
    #buf=create_string_buffer(buf_size)
    #hdl.readfru2(pointer(buf), start, buf_size)
    size=len(fru_buf.raw)
    print("buf.value = %s" % fru_buf.value.__str__()[20:-1])
    loop = 0
    i = 0
    j = 0
    for i in range(size//16):
        print('%08x:' % loop, end=' ')
        j = 0
        for j in range(16):
            print('%02x' %  fru_buf.raw[j+loop], end=' ')
            j += 1
        j = 0
        for j in range(16):
            if int(fru_buf.raw[j+loop]) < 32 or int(fru_buf.raw[j+loop]) > 126:
                print('.', end='')
            else:
                print('%c' % fru_buf.raw[j+loop],end='')
            j += 1
        loop += 16
        i +=1
        print('')
    remain=size % 16
    print('%08x:' % loop, end=' ')
    for i in range(remain):
        print('%02x' % fru_buf.raw[loop+i], end=' ')
    for i in range(16 - remain):
        print('  ', end=' ')
    for i in range(remain):
        if int(fru_buf.raw[i+loop]) < 32 or int(fru_buf.raw[i+loop]) > 126:
            print('.', end='')
        else:
            print('%c' % fru_buf.raw[i+loop],end='')
    print('')

   

def show_fru_in_hex(fru_buf, size=512):
    #TODO
    start = 0
    if size > 2048:
        buf_size = 2048
    else:
        buf_size = size
    #buf=create_string_buffer(buf_size)
    #hdl.readfru(buf, start, buf_size)
    size=len(fru_buf.raw) 
    loop = 0
    i = 0
    j = 0
    for i in range(size//16):
        print('%08x:' % loop, end=' ')
        j = 0
        for j in range(16):
            print('%02x' %  fru_buf.raw[j+loop], end=' ')
            j += 1
        j = 0
        for j in range(16):
            if int(fru_buf.raw[j+loop]) < 32 or int(fru_buf.raw[j+loop]) > 126:
                print('.', end='')
            else:
                print('%c' % fru_buf.raw[j+loop],end='')
            j += 1
        loop += 16
        i +=1
        print('')
    remain=size % 16
    print('%08x:' % loop, end=' ')
    for i in range(remain):
        print('%02x' % fru_buf.raw[loop+i], end=' ')
    for i in range(16 - remain):
        print('  ', end=' ')
    for i in range(remain):
        if int(fru_buf.raw[i+loop]) < 32 or int(fru_buf.raw[i+loop]) > 126:
            print('.', end='')
        else:
            print('%c' % fru_buf.raw[i+loop],end='')
    print('')

############################################################ 
# R/W Chassis Info
#
############################################################
def rw_chassis_info(fru_buf, c_name, c_string="", mode='r'):
    
    cha_offset = fru_buf.raw[2]*8
    area_length = fru_buf.raw[cha_offset + 1] * 8
    cpn_len = fru_buf.raw[cha_offset + 3] - Fru.codetype 
    cpn_offset = cha_offset + 3 + 1

    csn_len = fru_buf.raw[cpn_offset + cpn_len ] - Fru.codetype
    csn_offset = cpn_offset + cpn_len + 1

    #print("Chassis Type:             %2X" % cha_type)
    #Read Chassis Info 
    if c_name== '/CPN' and  mode == 'r':
        print("Chassis Part Number:        ", end='')
        for i in range(0, cpn_len):
            print('%c' %fru_buf.raw[cpn_offset + i], end='')
        print('')
    elif c_name == '/CSN' and mode == 'r':
        print("Chassis Serial Number:      ", end='')
        for i in range(0, csn_len):
            print('%c' % fru_buf.raw[csn_offset + i], end='')
        print('')
    #
    checksum_offset = cha_offset + area_length - 1
    checksum = 0
    print("DEBUG: Chassis Checksum is: %x(offset:%x) " % (fru_buf.raw[checksum_offset], checksum_offset))
    print("DEBUG: Area length: %d, Programming ( %s )" % (area_length, c_string))
    #Program Chassis Info
    if c_name == '/CPN' and mode == 'w':
        p_fru_buf=addressof(fru_buf)
        fru_string=string_at(p_fru_buf, sizeof(fru_buf))
        print("DEBUG: fru_string ( %s )" % fru_string)
        if cpn_len <= len(c_string):
            print("The length of %s is out of range! " % c_string)
            sys.exit(1)
        cpn_fru=create_string_buffer(c_string.encode('utf-8'))
        space = create_string_buffer(b'', cpn_len-len(c_string)-1) # cpn_fru include an end byte: '\x00'
        left_start=cpn_offset + cpn_len 
        new_fru = fru_buf.raw[0:cpn_offset] + cpn_fru.raw + space.raw +  fru_buf.raw[left_start:]
        print("DEBUG: fru_string ( %s )" % new_fru)
       
 	#TODO: Need to calculate CheckSum.
        checksum_offset = cha_offset + area_length - 1
        checksum = 0
        print("Chassis Checksum is: %x(offset:%x) " % (fru_buf.raw[checksum_offset], checksum_offset))
        for i in range(0, area_length):
            checksum += fru_buf.raw[cha_offset + i]
        checksum = 256 - checksum
        print("Calulate checksum is (%d)" % checksum)    
        return new_fru

    if c_name == '/CSN' and mode == 'w':
        csn_fru=create_string_buffer(c_string.encode('utf-8')) 
        if csn_len <= len(c_string):
            print("The length of %s is out of range! " % c_string)
            sys.exit(2)
        space = create_string_buffer(b'', csn_len-len(c_string)-1) # cpn_fru include an end byte: '\x00'
        left_start=csn_offset + csn_len 
        new_fru = fru_buf.raw[0:csn_offset] + csn_fru.raw + space.raw +  fru_buf.raw[left_start:]
        print("DEBUG: fru_string ( %s )" % new_fru)
	#TODO: Need to calculate CheckSum. 
        return new_fru
       

def rw_board_info(fru_buf, c_name, c_string, mode='r'):
    board_items=['/BM', '/BMT', '/BPNA', '/BSN', '/BPNU', '/BFFI' ]
    board_offset = fru_buf.raw[3]*8
    date_offset = board_offset + 3 #
    bpm_offset  = date_offset + 3 + 1
    bpm_len = fru_buf.raw[bpm_offset - 1] - Fru.codetype
    
    
    if c_name == '/BMT' and mode == 'r':
        print("Manufacturing Date/Time  :  ")
        #TODO: 	   
 
    if c_name == '/BM' and mode == 'r':
        print("Board Manufacturer String:  ", end='')
        for i in range(0, bpm_len):
            print('%c' % fru_buf.raw[bpm_offset + i], end='')
        print('')
    
    bpn_len = fru_buf.raw[bpm_offset+bpm_len] - Fru.codetype
    bpn_offset = bpm_offset + bpm_len + 1
    if c_name == '/BPNA' and mode == 'r':
        print("Board Product Name String:  ", end='')
        for i in range(0, bpn_len):
            print('%c' % fru_buf.raw[bpn_offset + i], end='')
        print('')
    
    bsn_len = fru_buf.raw[bpn_offset + bpn_len ] - Fru.codetype
    bsn_offset = bpn_offset + bpn_len + 1
    if c_name == '/BSN' and mode == 'r':
        print("Board Serial Number String: ", end = '')
        for i in range(0, bsn_len):
            print('%c' %fru_buf.raw[bsn_offset + i ], end = '')
        print('')
    
    bpnu_len = fru_buf.raw[bsn_offset + bsn_len] - Fru.codetype
    bpnu_offset = bsn_offset + bsn_len + 1
    if c_name == '/BPNU' and mode == 'r':
        print("Board Part Number String:   ", end = '')
        for i in range(0, bpnu_len):
            print('%c' % fru_buf.raw[bpnu_offset + i], end = '')
        print('')
    
    bffi_len = fru_buf.raw[bpnu_offset + bpnu_len] - Fru.codetype
    bffi_offset = bpnu_offset + bsn_len + 1
    if c_name == '/BFFI' and mode == 'r':
        print("FRU File ID String:         ", end = '')
        for i in range(0, bffi_len):
            print('%c' % fru_buf.raw[bffi_offset + i], end = '')
        print('')
    #print("Custom Mfg. Info:           ", end = '')

    #TODO: Program Board Info
    if mode == 'w':
        print("TODO: Programming the Chassis information !")

def rw_product_info(fru_buf, c_name, c_string, mode='r'):
    product_items=['/PM', '/PN', '/PPN', '/PV', '/PSN', '/PAT', '/PFFI']

    product_offset = fru_buf.raw[4]*8
    pm_len = fru_buf.raw[product_offset+3] - Fru.codetype
    pm_offset = product_offset + 3 + 1
    if c_name == '/PM' and mode == 'r':
        print("Manufacturer Name:          ", end = '')
        for i in range(0, pm_len):
            print('%c' % fru_buf.raw[pm_offset + i], end = '')
        print('')
    
    pn_len = fru_buf.raw[pm_offset + pm_len] - Fru.codetype
    pn_offset = pm_offset + pm_len + 1
    if c_name == '/PN' and mode == 'r':
        print("Product Name:               ", end = '')
        for i in range(0, pn_len):
            print('%c' % fru_buf.raw[pn_offset + i], end = '')
        print('')

    ppn_len = fru_buf.raw[pn_offset + pn_len] - Fru.codetype
    ppn_offset = pn_offset + pn_len + 1
    if c_name == '/PPN' and mode == 'r':
        print("Product Part/Mode Name:     ", end = '')
        for i in range(0, ppn_len):
            print('%c' % fru_buf.raw[ppn_offset + i], end = '')
        print('')
    
    pv_len = fru_buf.raw[ppn_offset + ppn_len] - Fru.codetype
    pv_offset = ppn_offset + ppn_len + 1
    if c_name == '/PV' and mode == 'r':
        print("Product Version String:     ", end = '')
        for i in range(0, pv_len):
            print('%c' % fru_buf.raw[pv_offset + i], end = '')
        print('')

    psn_len = fru_buf.raw[pv_offset + pv_len] - Fru.codetype
    psn_offset = pv_offset + pv_len + 1
    if c_name == '/PSN' and mode == 'r':
        print("Product Serail Number:      ", end = '')
        for i in range(0, psn_len):
            print('%c' % fru_buf.raw[psn_offset + i], end = '')
        print('')

    pat_len = fru_buf.raw[psn_offset + psn_len] - Fru.codetype
    pat_offset = psn_offset + psn_len + 1
    if c_name == '/PAT' and mode == 'r':
        print("Product Asset Tag:          ", end = '')
        for i in range(0, pat_len):
            print('%c' % fru_buf.raw[pat_offset + i], end = '')
        print('')

    pffi_len = fru_buf.raw[pat_offset + pat_len] - Fru.codetype
    pffi_offset = pat_offset + pat_len + 1
    if c_name == '/PFFI' and mode == 'r':
        print("Product FRU Fiel ID:        ", end = '')
        for i in range(0, pffi_len):
            print('%c' % fru_buf.raw[pffi_offset + i], end = '')
        print('')
   
    #TODO: Program Board Info
    if mode == 'w':
        print("TODO: Programming the Chassis information !")


def show_fru_in_text(fru_buf):
    #TODO
    codetype= 0xC0
    #Show Chassis FRU Info
    cha_offset = fru_buf.raw[2]
    cha_type = fru_buf.raw[cha_offset*8 + 2]
    print("Chassis Code Type/Length: %2X " % fru_buf.raw[cha_offset*8 + 3])
    #11000000 is Interpretation depends on Language Codes
    if fru_buf.raw[cha_offset*8 + 3] & 0xC0 != Fru.codetype:
        print("Not Support this Language Code");
        sys.exit(-1)
    cpn_len = fru_buf.raw[cha_offset*8 + 3] - Fru.codetype 
    cpn_offset = cha_offset* 8 + 4
    #cpn = create_string_buffer(cpn_len)
    print("Chassis Type:             %2X" % cha_type)
    print("Chassis Part Number:      ", end='')
    for i in range(0, cpn_len):
        print('%c' %fru_buf.raw[cpn_offset + i], end='')
    print('')
    csn_len = fru_buf.raw[cpn_offset + cpn_len] - Fru.codetype
    csn_offset = cpn_offset + cpn_len + 1
    print("Chassis Serial Number:      ", end='')
    for i in range(0, csn_len):
        print('%c' % fru_buf.raw[csn_offset + i], end='')
    print('')
     
    #Show Board FRU Info
    board_offset = fru_buf.raw[3]*8
    date_offset = board_offset + 3 #
    bpm_offset  = date_offset + 3 + 1
    bpm_len = fru_buf.raw[bpm_offset - 1] - Fru.codetype
    print("Board Manufacturer String:  ", end='')
    for i in range(0, bpm_len):
        print('%c' % fru_buf.raw[bpm_offset + i], end='')
    print('')
    bpn_len = fru_buf.raw[bpm_offset+bpm_len] - Fru.codetype
    bpn_offset = bpm_offset + bpm_len + 1
    print("Board Product Name String:  ", end='')
    for i in range(0, bpn_len):
        print('%c' % fru_buf.raw[bpn_offset + i], end='')
    print('')
    bsn_len = fru_buf.raw[bpn_offset + bpn_len ] - Fru.codetype
    bsn_offset = bpn_offset + bpn_len + 1
    print("Board Serial Number String: ", end = '')
    for i in range(0, bsn_len):
        print('%c' %fru_buf.raw[bsn_offset + i ], end = '')
    print('')
    bpnu_len = fru_buf.raw[bsn_offset + bsn_len] - Fru.codetype
    bpnu_offset = bsn_offset + bsn_len + 1
    print("Board Part Number String:   ", end = '')
    for i in range(0, bpnu_len):
        print('%c' % fru_buf.raw[bpnu_offset + i], end = '')
    print('')
    bffi_len = fru_buf.raw[bpnu_offset + bpnu_len] - Fru.codetype
    bffi_offset = bpnu_offset + bsn_len + 1
    print("FRU File ID String:         ", end = '')
    for i in range(0, bffi_len):
        print('%c' % fru_buf.raw[bffi_offset + i], end = '')
    print('')
    #print("Custom Mfg. Info:           ", end = '')

    #Show Production FRU Info
    product_offset = fru_buf.raw[4]*8
    pm_len = fru_buf.raw[product_offset + 3] - Fru.codetype
    pm_offset = product_offset + 1
    print("Manufacturer Name:          ", end = '')
    print("Product Name:               ", end = '')
    print("Product Part/Mode Name:     ", end = '')
    print("Product Version String:     ", end = '')
    print("Product Serail Number:      ", end = '')
    print("Product Asset Tag:          ", end = '')
    print("Product FRU Fiel ID:        ", end = '')
    print('')

def rw_csn(arg):
    #TODO:
    pass
    
    

def main(argv):
    if len(argv) == 1 or argv[1]=="-h":
        Usage()
        sys.exit(1)
    print(argv)

    #Load KCS API
    hdl = cdll.LoadLibrary('./clib/libkcs.so')
    fru_size=hdl.get_fru_data_length()
    print("fru_size = %d" % fru_size)
    if fru_size <=0:
        print("Get the size of FRU fail !")
        sys.exit(-1)
    fru=create_string_buffer(fru_size)
    hdl.readfru(fru, 0, fru_size)
    #Verify the FRU header checksum:
    ret=hdl.verify_modify_check_sum(fru,0,7,"Common Header",None,0)
    if ret < 0:
        print("Verify FRU header check sum fail!")
        sys.exit(ret)
    if Dbg.DEBUG == True:
        print('Common Header Version: %2x' % fru.raw[0])
        print('Internal Use offset:   %2x' % fru.raw[1])
        print('Chassis Info offset:   %2x' % fru.raw[2])
        print('Board Info offset:     %2x' % fru.raw[3])
        print('Product Info offset:   %2x' % fru.raw[4])
        print('MultiRecord area offset:%2x' % fru.raw[5])
        print('PAD:                   %2x' % fru.raw[6])
        print('Checksum:              %2x' % fru.raw[7])

    chassis_items=['/CPN', '/CSN']
    board_items=['/BM', '/BMT', '/BPNA', '/BSN', '/BPNU', '/BFFI' ]
    product_items=['/PM', '/PN', '/PPN', '/PV', '/PSN', '/PAT', '/PFFI']
    if argv[1] in board_items:
        if len(argv) == 3:
            rw_board_info(fru, argv[1], argv[2], 'w')
        else:
            rw_board_info(fru, argv[1], '', 'r')
    elif argv[1] in chassis_items:
        if len(argv) == 3:
            new_fru=rw_chassis_info(fru, argv[1], argv[2], 'w')
            print("DEBUG: new_frufru ( %s )" % new_fru)
            hdl.flashfru(new_fru, 0, fru_size)
        else:
            rw_chassis_info(fru, argv[1], '', 'r')
    elif argv[1] in product_items:
        if len(argv) == 3:
            rw_product_info(fru, argv[1], argv[2], 'w')
        else:
            rw_product_info(fru, argv[1], '', 'r')

    elif argv[1] == '-r' and len(argv) == 4:
        dump_fru_to_file(fru, int(argv[2]), argv[3])
    elif argv[1] == "-sbin" and len(argv) == 3:
        show_fru_in_hex(fru, int(argv[2]))
    elif argv[1] == "-sbin" and len(argv) ==2:
        show_fru_in_hex(fru)
    elif argv[1] == "-stxt":
        for items in chassis_items:
            rw_chassis_info(fru, items, '', 'r')
        for items in board_items:
            rw_board_info(fru, items, '', 'r')
        for items in product_items:
            rw_product_info(fru, items, '', 'r')
        #show_fru_in_text(fru)
    elif argv[1] == "-test":
        read_fru_test(hdl)
    else:
        Usage()
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)

