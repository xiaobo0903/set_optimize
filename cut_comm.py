# -*- coding: UTF-8 -*-
#删除行中的以“#号为解释内容；
def cut_comm(str):
    try:
        num = str.index("#")
        nstr = str[0:num]
        return nstr  
    except:
        return str

