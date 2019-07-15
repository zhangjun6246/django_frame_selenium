# -*- coding: utf-8 -*- 

"""
 * @Description:   ui自动化平台公共模块
 * @author:        lujun
 * @version:       V1.0
 * @Date:          2018/04/19
"""

import configparser
import os
import paramiko

def read_conf(option, item):
    """
        读取配置文件公共模块

        example：
        readConf('SSH','hostname')
        return: Str
    """
    currentDir = os.getcwd()
    confDir = currentDir.replace("apis\\views","ui.conf")
    cp = configparser.SafeConfigParser()
    cp.read(confDir)
    confValue = cp.get(option,item)
    return confValue

def ssh_connect(hostname, username, password, port, cmd):
    """ SSH 链接 """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        #ssh.connect(hostname=hostname,port=port,username=username,password=password,timeout=10)
        ssh.connect(hostname,port,username,password,timeout=10)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        print (stdout.read())
        ssh.close()
    except expression as identifier:
        ssh.close()
        print ('SHH链接失败!' )


if __name__ == "__main__":
    read_conf('SSH','username')
    ssh_connect('10.40.6.24','root','oo4zv~S99R+@4ml0ww?#','36000','ifconfig')