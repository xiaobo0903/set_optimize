# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  pubTools.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: 本程序是mysql的优化项检测，输入mysql的my.cnf的地址，然后检测，内容设置                        
Others: None
**********************************************************************************************          
'''
try:
    # Python3
    import configparser as ConfigParser
    import io as StringIO
except ImportError:
    # Python2
    import ConfigParser
    import StringIO
import os
import sys
from cut_comm import cut_comm
#读取linux系统中的配置文件 sysctl.conf
sysconf = ""
optconf = "./data/my.ini"
sdict = {}
odict = {}
smem = 4096

#读取my.init文件内容并放入到sdic中
def load_my():

    mypath = None
    while True:
        if sys.version_info < (3, 0):
            mypath = raw_input("\n读输入mysql数据库的配置文件地址(如:/etc/mysql/my.cnf),按'q'可退出: ")
        else:
            mypath = input("\n读输入mysql数据库的配置文件地址(如:/etc/mysql/my.cnf),按'q'可退出: ")
        if mypath == 'q':
            exit()

        #print(mypath)
        if os.path.isfile(mypath):
            break
        print("输入的文件不存在!, 请重新输入")
        mypath = None

    nstr = ""
    with open(mypath, 'r') as fo:
        for line in fo:
            nline = cut_comm(line)
            nstr  = nstr+nline+"\n"

    ini_fp = StringIO.StringIO(nstr)
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.readfp(ini_fp)

    for item in config.items("mysqld"):
        key = ""
        val = ""
        #因为允许输入未赋值的设置，所以需要对于key进行处理
        try:
            num = item[0].index("#")
            key = item[0][0:num]
            key = key.strip()
        except Exception:
            key = item[0]
            key = key.strip()
        #因为允许输入未赋值的设置，所以需要对于val进行处理
        try:
            num = item[1].index("#")
            val = item[1][0:num]
            val = val.strip()
        except Exception:
            val = item[1]           
        if val == None:
            val = "isTrue"
        sdict[key] = val
    #print(sdict)
#因为mysql 的设置与内容有相关性，所以需要读取系统的内容
def get_sys_mem():

    p = os.popen("free")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            mem = line.split()[1:4]
            break
    global smem
    smem1 = round(int(mem[0])/1000)
    smem = (int((smem1+512) / 1024)) * 1024 

#读取优化项的配置内容
def load_optimize_conf():

    #在此使用这个方法，是为了py2和py3的兼容性
    config = ConfigParser.ConfigParser()
    config.read(optconf)
    for select in config.sections():
        #print(select)
        itemd = {}
        for item in config.items(select):
            itemd[item[0]] = item[1]
        itemd["sys"] = ""
        odict[select] = itemd
    #print("读取优化标准配置完成")
    #print(odict)

#设置当前的优化项配置内容
def set_cur_conf():
    #读取odict的内容，把系统当前的配置写入到odict中
    for (k,v) in  odict.items(): 
        if sdict.get(k):
            v["sys"] = sdict[k]
            odict[k] = v

def diff_sys_conf():

    load_my()
    load_optimize_conf()
    set_cur_conf()
    print("\n当前系统的内存容量是:[%sM], 针对其优化的配置信息比对结果是:\n"%(smem))

    print("{0:53}{1:33}{2:35}{3:15}{4:20}\n".format("名称" ,"当前值" ,'推荐值','检测结果','说明'))

    for (k,v) in  odict.items(): 
        for vm in v:
            if vm == "name":
                n = v["name"]
            if vm == "sys":
                s = v["sys"]
            if vm == "mval":
            #0，1，2，3，4， 5， 6， 7）（0，1， 2， 4， 8，16，32， 64）
            #如果是mval值，则需要对于系统进行按内容配置，如{16M, 32M, 64M, 256M, 512M, 1024M, 2048M, 4096M}，则第0：缺省,1:为1G起,2:2G, 3:4G
                ii = (int(int((smem/1024)+1)/2))*2
                if ii == 0:
                    ii = 1
                import math
                lg = int(math.log(ii,2))
                if lg > 7:
                    lg = 7
                o = v["mval"].split(",")[lg]
            if vm == "val":
                o = v["val"]  
            if vm == "bval":
                o = v["bval"]              
        #如果系统没的设置，则把缺省值设置给当前值
        o = o.strip() 
        if s == "" :
            s = "isFalse"
        flag = "No"
        if o == s:
            flag = "Pass"

        print("%-50s %-30s %-30s %-10s %-s"%(k, s, o, flag, n))
    
    print("\n按任意键继续......")
    try:
        raw_input()
    except:
        input()
        
if __name__ == "__main__":
    get_sys_mem()
    diff_sys_conf()