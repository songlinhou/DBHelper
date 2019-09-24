#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:14:55 2019

@author: Ray
"""

import os
import json
import sys
import subprocess



file_name = '.name'
is_name_newly_created = False
user_data = {'name':None}
width = 70


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_name():
  global user_data
  global is_name_newly_created
  #user_data = {'name':None}
  try:
    if os.path.exists(file_name):
      with open(file_name) as f:
        data_str = f.read()
        user_data = json.loads(data_str)
  except Exception:
    user_data = {'name':None}
  #print "user_data=",user_data
  while not user_data['name']:
    username_input = raw_input('input your username:')
    user_data['name'] = username_input.strip()
    is_name_newly_created = True
  
  if is_name_newly_created:
    with open(file_name,'w') as f:
      data_str = json.dumps(user_data)
      f.write(data_str)

def reset_name():
  global user_data
  os.remove(file_name)
  user_data = {'name':None}
  check_name()

def setup_path():
  from os.path import expanduser
  home = expanduser("~")
  path = os.path.join(home,".bash_profile")
  script_path = os.path.abspath(__file__)
  script_dir = os.path.dirname(script_path)
  #print "script",script_dir
  if os.path.exists(path):
    lines = None
    with open(path) as f:
      lines = f.readlines()
    for line in lines:
      if line.startswith('#dbh hook'):
        return
  with open(path,'a+') as f:
    f.write('#dbh hook\nexport PATH=$PATH:{}'.format(script_dir))
  

def show_title():
  global width
  line1 = "#" * width
  line2 = "## {}DB Helper{}".format(bcolors.BOLD,bcolors.ENDC)
  line2_ = (width - len(line2) - 2 + 8) * ' ' + "##"
  line2 = line2 + line2_
  version = "Version: 1.0"
  line3 = "##" + (width - 2 - 3 - len(version)) * ' ' + version + " ##"
  author = "Author: {}Ray{}".format(bcolors.OKBLUE,bcolors.ENDC)
  line4 = "##" + (width - 2 - 3 - len(author) + 9) * ' ' + author + " ##"
  
  print "\n"
  print line1
  print line2
  print line3
  print line4
  print line1
 
def exit_app():
  print "{}Good Bye.{}".format(bcolors.OKGREEN,bcolors.ENDC)
  exit(0)
  
def main_menu_options():
  options = []
  options.append( "{}[1]{} Enter SQL Console".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[2]{} Generate .sql Script".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[3]{} Generate .ctl File".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[4]{} Load .sql Script".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[5]{} Load .ctl Data Controller".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[6]{} View File".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[7]{} Create/Edit File".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[8]{} Reset Name".format(bcolors.OKBLUE,bcolors.ENDC))
  options.append( "{}[9]{} Exit".format(bcolors.OKBLUE,bcolors.ENDC))
  
  for option in options:
    print option
  return len(options)
  
  
def index():
  show_title()
  print "\nCurrent Path"
  print "Menu\\"
  opt_len = main_menu_options()
  print "-" * width
  choice = None
  while True:
    try:
      choice = int(raw_input('{}Input your choice (1-{}):{}'.format(bcolors.BOLD,opt_len,bcolors.ENDC)))
      if 1 <= choice <= opt_len:
        break;
    except:
      choice = None
  
  if choice == 1:
    init_db()
  elif choice == 2:
    create_sql()
  elif choice == 3:
    create_ctl_file()
  elif choice == 4:
    load_as_sql()
  elif choice == 5:
    load_as_data()
  elif choice == 6:
    view_file()
  elif choice == 7:
    create_or_edit_file()
  elif choice == 8:
    reset_name()
  elif choice == 9:
    exit_app()
      
def init_db():
  check_name()
  cmd = 'source /cs/bin/oracle-setup > /dev/null;'
  sqlplus= 'sqlplus {username}/{USERNAME}@CS;'.format(username=user_data['name'],USERNAME=str(user_data['name']).upper());
  #print sqlplus
  cmd += sqlplus
  subprocess.call(cmd,shell=True)

def help_info():
  print "{}dbh db{}\tGo to SQL Console".format(bcolors.OKBLUE,bcolors.ENDC)
  print "{}dbh edit{}\tGenerate .sql File".format(bcolors.OKBLUE,bcolors.ENDC)
  print "{}dbh load data.sql{}\tLoad SQL Script or Datafile".format(bcolors.OKBLUE,bcolors.ENDC)
  print "{}dbh view{}\tView a file".format(bcolors.OKBLUE,bcolors.ENDC)
  print "{}dbh help{}\tView this Help Guide".format(bcolors.OKBLUE,bcolors.ENDC)
  
def load_file(filepath=None):
  check_name()
  while not filepath:
    filepath = raw_input("{}Input the file name:{}".format(bcolors.BOLD,bcolors.ENDC))
    filepath = filepath.strip()
  if not os.path.exists(filepath):
    print "{}[x] File not exists{}".format(bcolors.FAIL,bcolors.ENDC)
    return
  path,filename = os.path.split(filepath)
  _,ext = os.path.splitext(filename)
  if ext.lower() == '.sql':
    load_as_sql(filepath)
  elif ext.lower() == '.ctl':
    load_as_data(filepath)


def create_sql():
  print "{}visit the following link{}".format(bcolors.BOLD,bcolors.ENDC)
  print "{}https://www.freeformatter.com/sql-formatter.html{}".format(bcolors.UNDERLINE,bcolors.ENDC)
  while True:
    ans = raw_input('{}Do you need to open the editor now(Y/N)? {}'.format(bcolors.OKGREEN,bcolors.ENDC))
    if ans.strip().lower() == 'y':
      view_file()
      break
    elif ans.strip().lower() == 'n':
      break
  

def create_ctl_file(datname=None,tablename=None,columns=None,check_exist=True,output_file=None,sep=','):
  check_name()
  while not tablename:
    tablename = raw_input("{}Input the table name:{}".format(bcolors.BOLD,bcolors.ENDC))
    tablename = tablename.strip()
  if not check_exist:
    while not datname:
      datname = raw_input("{}Input the .dat file name:{}".format(bcolors.BOLD,bcolors.ENDC))
      datname = datname.strip()
  else:
    first_try = True
    # check the disk
    while True:
      if first_try:
        datname = raw_input("{}Input the existing .dat file name:{}".format(bcolors.BOLD,bcolors.ENDC))
      else:
        datname = raw_input("{}Must input an existing .dat file name:{}".format(bcolors.OKBLUE,bcolors.ENDC))
      basename,ext = os.path.splitext(datname)
      exist_list = [False,False]
      if os.path.isfile(datname):
        exist_list[0] = True
      if not ext:
        datname2 = basename + '.dat'
        if os.path.isfile(datname2):
          exist_list[1] = True
      if exist_list[0]:
        break
      elif exist_list[1]:
        datname = datname2
        break
      first_try = False
    
  if not columns:
    while True:
      try:
        column_num = int(raw_input("{}How many columns are there for table {}?{}".format(bcolors.BOLD,tablename,bcolors.ENDC)))
        if column_num > 0:
          break
      except:
        column_num = None
    columns = []
    for i in range(column_num):
      while True:
        col = raw_input("{}column {} name:{}".format(bcolors.BOLD,i+1,bcolors.ENDC))
        col = col.strip()
        if col:
          columns.append(col)
          break;
  content = generateCTLContent(datname,tablename,columns)
  print content
  while not output_file:
    output_file = raw_input("{}Save as file:{}".format(bcolors.BOLD,bcolors.ENDC))
    output_file = output_file.strip()
  with open(output_file,'w') as f:
    f.write(content)
  return content
    
def generateCTLContent(datname,tablename,columns,sep=','):
  columns_str = ','.join(columns)
  ctl_content ='''load data
  infile {datname}
  into table {tablename}
  fields terminated by '{sep}' 
  ({columns})'''.format(sep=sep,datname=datname,tablename=tablename,columns=columns_str)
  return ctl_content

def load_as_sql(filepath=None):
  #echo exit | sqlplus ${username}@CS/${username^^} @createTables
  check_name()
  while not filepath:
    filepath = raw_input("Input the .sql file name:")
    filepath = filepath.strip()
  if not os.path.exists(filepath):
    print "{}[x] File not exists{}".format(bcolors.FAIL,bcolors.ENDC)
    return
  path,filename = os.path.split(filepath)
  basename,ext = os.path.splitext(filename)
  target_format = os.path.join(path,basename)
  print "TARGET= " + target_format
  cmd = 'source /cs/bin/oracle-setup > /dev/null;'
  cmd += "echo exit | sqlplus {username}@CS/{USERNAME} @{target}".format(username=user_data['name'],USERNAME=str(user_data['name']).upper(),target=target_format)
  print cmd
  subprocess.call(cmd,shell=True)
  
def load_as_data(filepath=None):
  #sqlldr ${username}@CS/${username^^} control=loadHW3-emp.ctl
  check_name()
  while not filepath:
    filepath = raw_input("{}Input the .ctl file name:{}".format(bcolors.BOLD,bcolors.ENDC))
    filepath = filepath.strip()
  if not os.path.exists(filepath):
    print "{}[x] File not exists{}".format(bcolors.FAIL,bcolors.ENDC)
    return
  cmd = 'source /cs/bin/oracle-setup > /dev/null;'
  cmd += "sqlldr {username}@CS/{USERNAME} control={ctlfile}".format(username=user_data['name'],USERNAME=str(user_data['name']).upper(),ctlfile=filepath);
  print cmd
  subprocess.call(cmd,shell=True)
  
def create_or_edit_file(filepath=None):
  toolname = ""
  while not filepath:
    filepath = raw_input("{}Input the file name:{}".format(bcolors.BOLD,bcolors.ENDC))
    filepath = filepath.strip()
  while True:
    print "Create/Edit {} Using".format(filepath)
    print "{}[1] Nano (For learners){}".format(bcolors.BOLD,bcolors.ENDC)
    print "{}[2] VIM (For advanced users){}".format(bcolors.BOLD,bcolors.ENDC)
    choice = raw_input("Choice=")
    if choice == 1:
      toolname = 'nano'
      break
    elif choice == 2:
      toolname = 'vim'
      break
  cmd = "{} {}".format(toolname,filepath)
  subprocess.call(cmd,shell=True)

def view_file(filepath=None):
  while not filepath:
    filepath = raw_input("{}Input the file name:{}".format(bcolors.BOLD,bcolors.ENDC))
    filepath = filepath.strip()
  if not os.path.exists(filepath):
    print "{}[x] File not exists{}".format(bcolors.FAIL,bcolors.ENDC)
    return
  cmd = "less " + filepath
  subprocess.call(cmd,shell=True)


setup_path()

if len(sys.argv) > 1:
  command = sys.argv[1]
  if command.lower() == 'help':
    help_info()
  elif command.lower() == 'db':
    check_name()
    init_db()
  elif command.lower() == 'load':
    check_name()
    if len(sys.argv) >= 3:
      path = sys.argv[2]
      load_file(path)
    else:
      print "{}[x] Please provide the location of the file.{}".format(bcolors.FAIL,bcolors.ENDC)
  elif command.lower() == 'view':
    check_name()
    if len(sys.argv) >= 3:
      path = sys.argv[2]
      view_file(path)
    else:
      print "{}[x] Please provide the location of the file.{}".format(bcolors.FAIL,bcolors.ENDC)
  else:
    help_info()
    
else:
  index()

    



  
    