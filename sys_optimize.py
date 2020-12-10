# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  pubTools.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: linux系统的优化项分析， 主要是分析/etc/sysctl.conf；                        
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
#读取linux系统中的配置文件 sysctl.conf
sysconf = "/etc/sysctl.conf"
optconf = "./data/linux_sysctl.ini"
sdict = {}
odict = {}

#读取linux系经中sysctl.conf文件中的信息；并放入到sdic中
def load_sysctl():

    #在此使用这个方法，是为了py2和py3的兼容性
    ini_str = '[system]\n' + open(sysconf, 'r').read()
    ini_fp = StringIO.StringIO(ini_str)
    config = ConfigParser.ConfigParser()
    config.readfp(ini_fp)
    for item in config.items("system"):
        sdict[item[0]] = item[1]
    #print(sdict)

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

    load_sysctl()
    load_optimize_conf()
    set_cur_conf()
    print("\n系统的配置信息比对结果:\n")

    print("{0:53}{1:33}{2:35}{3:15}{4:20}\n".format("名称" ,"当前值" ,'推荐值','检测结果','说明'))

    for (k,v) in  odict.items(): 
        n = v["name"]
        s = v["sys"]
        o = v["val"]
        d = v["def"]
        #如果系统没的设置，则把缺省值设置给当前值
        if s == "" :
            s = d
        flag = "No"
        if o == s:
            flag = "Pass"

        print("%-50s %-30s %-30s %-10s %-s"%(k, s, o, flag, n))
    
    print("按任意键继续......")
    raw_input()
    mk_standard_opt()
#生成标准的优化项内容；
def mk_standard_opt():
    #打印标准的优化项配置，可清空系统的/etc/sysctl.conf内容，把生成的内容直接拷入；
    print("\n下面是生成的标准linux系统的优化项配置内容，你可以用下面的内容替换/etc/sysctl.conf的内容；") 
    print("###################################  由自动配置程序生成的优化内容  #######################################\n")     
    for (k,v) in  odict.items(): 
            n = v["name"]
            s = v["sys"]
            o = v["val"]
            d = v["def"]
            print("%s=%s"%(k, o))

    print("\n###################################  生成的优化内容  #######################################") 
    print("\n操作方法:\n")  
    print("1、备份/etc/sysctl.conf文件")  
    print("2、清空/etc/sysctl.conf文件内容")  
    print("3、拷贝生成的内容到/etc/sysctl.conf文件") 
    print("4、重启服务器(如果想临时生效，可使用sysctl -p命令)")          
if __name__ == "__main__":
    diff_sys_conf()