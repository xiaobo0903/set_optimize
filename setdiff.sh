#!/bin/bash

clear
echo "1) linux系统配置参数优化对比"
echo "2) mysql数据库配置参数优化对比"
while :
do
    read -p "请选择，输入\"q\"退出:" yn
    if [ $yn = "q" ]; then
        exit 1
    elif [ $yn = '1' ]; then
        python ./sys_optimize.py

    elif [ $yn = '2' ]; then
        python ./mysql_optimize.py
    else
       echo ""
    fi
done
