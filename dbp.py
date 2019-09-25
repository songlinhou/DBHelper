#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 19:12:01 2019

@author: Ray
"""

import json
import os
import sys
import subprocess


file_name = '.name'
is_name_newly_created = False
user_data = {'name':None}
width = 70
global_table = None

temp_files = []

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


def generateCTLContent(datname,tablename,columns,outputfile=None,sep=','):
  columns_str = ','.join(columns)
  ctl_content ='''load data
  infile {datname}
  into table {tablename}
  fields terminated by '{sep}' 
  ({columns})\n'''.format(sep=sep,datname=datname,tablename=tablename,columns=columns_str)
  if outputfile:
    with open(outputfile,'w') as f:
      f.write(ctl_content)
  return ctl_content
  

def checkColumnConsistency(datname,columns,sep=','):
  with open(datname) as f:
    lines = f.readlines()
  for line in lines:
    line_trim = line.strip()
    row_values = line_trim.split(sep)
    if len(row_values) != len(columns):
      return False
  return True


def build_dctl_file(tablename,columns=None,datname=None,sqlfile=None,output_file=None,sep=','):
  if datname:
    if not os.path.isfile(datname):
      print "data file not found"
      return
  
  if not tablename:
    print "tablename not provided"
    return
  else:
    tablename = tablename.strip()
    if not tablename:
      print "tablename cannot be blank"
      return

  if sqlfile:
    if not os.path.isfile(sqlfile):
      print 'sql file not found'
  #data = {'DAT':{},'SQL':{},'TABLE':tablename,'COL':{}}
  data = {'TABLE':tablename}
  
  with open(datname) as f:
    data['DAT'] = {}
    data['DAT']['name'] = os.path.basename(datname)
    data['DAT']['content'] = f.read()
    
  with open(sqlfile) as f:
    data['SQL'] = {}
    data['SQL']['name'] = os.path.basename(sqlfile)
    data['SQL']['content'] = f.read()
  
  if columns:
    data['COL'] = columns
  data_str = json.dumps(data)
  if output_file:
    with open(output_file,'w') as f:
      json.dump(data,f)
  else:
    print data_str
  return data_str
  

def new_db_bundle():
  tablename = None
  columns = None
  
  while not tablename:
    tablename = raw_input("[NECESSARY] Input the Name of One Target Table:")
    tablename = tablename.strip()
  while True:
    column_str = raw_input("[NECESSARY] Input the Attributes of Table {} Seperated by comma(,):".format(tablename))
    columns = column_str.split(',')
    if columns == ['']:
      continue
    else:
      print columns
      break
  while True:
    sqlfile = raw_input("[OPTIONAL] Input the .sql for Table {}:".format(tablename))
    sqlfile = sqlfile.strip()
    sqlfile = sqlfile.replace('\'','')
    sqlfile = sqlfile.replace('\\','')
    if not sqlfile:
      break
    else:
      if not os.path.isfile(sqlfile):
        print "Wrong path for .sql file"
      else:
        break
  while True:
    datfile = raw_input("[OPTIONAL] Input the .dat for Table {}:".format(tablename))
    datfile = datfile.strip()
    datfile = datfile.replace('\'','')
    datfile = datfile.replace('\\','')
    if not datfile:
      break
    else:
      if not os.path.isfile(datfile):
        print "Wrong path for .dat file"
      else:
        break
  
  filename = tablename
  if sqlfile:
    filename += "-sql"
  if datfile:
    filename += '-dat'
  filename += ".dbbundle"
    
  build_dctl_file(tablename,columns,datfile,sqlfile,filename) 
  return filename

#print generateCTLContent('work.dat','Work',['eid','name'])

def load_as_sql(filepath=None):
  #echo exit | sqlplus ${username}@CS/${username^^} @createTables
  check_name()
  while not filepath:
    filepath = raw_input("Input the .sql file name:")
    filepath = filepath.strip()
    filepath = filepath.replace('\'','')
    filepath = filepath.replace('\\','')
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

def process_bundle(filename):
  global temp_files
  global global_table
  try:
    with open(filename) as f:
      data = json.load(f)
  except:
    print "{}[x]Bad formatted bundle file!{}".format(bcolors.FAIL,bcolors.ENDC)
    exit(-1)
  id = 1
  table = data['TABLE']
  table = table.strip()
  global_table = table
  column = data['COL']
  if 'SQL' in data.keys():
    print '[{}]generate .sql file'.format(id)
    sqlname = data['SQL']['name']
    sqlcontent = data['SQL']['content']
    with open(sqlname,'w') as f:
      f.write(sqlcontent)
    id += 1
    temp_files.append(sqlname)
    
    print '[{}]execute .sql file'.format(id)
    load_as_sql(sqlname)
    
  if 'DAT' in data.keys():
    print '[{}]generate .dat file'.format(id)
    datname = data['DAT']['name']
    datcontent = data['DAT']['content']
    with open(datname,'w') as f:
      f.write(datcontent)
    id +=1
    temp_files.append(datname)
    
    print '[{}]create ctl file'.format(id)
    ctl_file = '{}-ctl.ctl'.format(table)
    generateCTLContent(datname,table,column,ctl_file)
    id += 1
    temp_files.append(ctl_file)
    
    print '[{}]execute ctl file'.format(id)
    load_as_data(ctl_file)
    id += 1
  remove_temp_files()

def upload_to_server(filepath):
  check_name()
  username = user_data['name']
  username = username.strip()
  if "SSH_CONNECTION" in os.environ:
    print "{}You are using the remote host. Please use this function in your localhost only.{}".format(bcolors.FAIL,bcolors.ENDC)
    return
  print "Ready to upload to server"
  if not os.path.exists(filepath):
    print "{}[x]{} doesn't exist{}".format(bcolors.FAIL,bundlefilename,bcolors.ENDC)
    return
  if os.path.isfile(filepath):
    subprocess.call("scp '{}' {}@ccc.wpi.edu:.".format(filepath,username.lower()),shell=True)
  elif os.path.isdir(filepath):
    subprocess.call("scp -r '{}' {}@ccc.wpi.edu:.".format(filepath,username.lower()),shell=True)
  else:
    print "{}File {} not supported.{}".format(bcolors.FAIL,filepath,bcolors.ENDC)

def downlaod_from_server(filepath):
  check_name()
  username = user_data['name']
  username = username.strip()
  if "SSH_CONNECTION" in os.environ:
    print "{}You are using the remote host. Please use this function in your localhost only.{}".format(bcolors.FAIL,bcolors.ENDC)
    return
  print "Ready to download from server"
  subprocess.call("scp -r '{}@ccc.wpi.edu:{}' .".format(username.lower(),filepath),shell=True)

  
def remove_temp_files():
  global temp_files
  for f in temp_files:
    os.remove(f)
  log_file = '{}-ctl.log'.format(global_table)
  if os.path.exists(log_file):
    os.remove(log_file)


def reset_name():
  global user_data
  os.remove(file_name)
  user_data = {'name':None}
  check_name()

def get_full_filename(argv):
  full_name = ""
  parts = sys.argv[2:]
  print "parts=",parts
  for part in parts:
    full_name = full_name + part
  full_name = full_name.replace("\\","")
  return full_name

def show_help():
  print "{}DB Bundler{}".format(bcolors.BOLD,bcolors.ENDC)
  print "Usage:"
  print "{}./dbp new{}\t\tCreate a new bundle file".format(bcolors.OKBLUE,bcolors.ENDC)
  print "{}./dbp run Table.dbbundle{}\t\tUse an existing bundle file called Table.dbbundle".format(bcolors.OKBLUE,bcolors.ENDC) 
  print "{}./dbp upload info.txt{}\t\tUpload a file called info.txt to server".format(bcolors.OKBLUE,bcolors.ENDC)   
  
if __name__ == '__main__':
  if len(sys.argv) == 1:
    show_help()
  else:
    action = sys.argv[1]
    if action == 'new':
      bundlename = new_db_bundle()
      upload_to_server(bundlename)
      exit(0)
    elif action == 'run':
      if len(sys.argv) >= 3:
        bundlefilename = get_full_filename(sys.argv)
        #bundlefilename = sys.argv[2]
        #bundlefilename = bundlefilename.replace("'","")
        #bundlefilename = bundlefilename.replace("\\","")
        if not os.path.isfile(bundlefilename):
          print "{}[x]It is not a valid file{}".format(bcolors.FAIL,bcolors.ENDC)
          exit(-1)
        else:
          process_bundle(bundlefilename)
      else:
        show_help()
    elif action == 'upload':
      if len(sys.argv) >= 3:
        bundlefilename = sys.argv[2]
        #print bundlefilename
        bundlefilename = bundlefilename.replace("'","")
        bundlefilename = bundlefilename.replace("\\","")
        print bundlefilename
        print 
        if not os.path.exists(bundlefilename):
          print "{}[x]{} doesn't exist{}".format(bcolors.FAIL,bundlefilename,bcolors.ENDC)
          exit(-1)
        else:
          upload_to_server(bundlefilename)
    elif action == 'download':
      if len(sys.argv) >= 3:
        bundlefilename = sys.argv[2]
        bundlefilename = bundlefilename.strip()
        #print bundlefilename
        if not bundlefilename:
          print "{}Name mustn't be empty.{}".format(bcolors.FAIL,bcolors.ENDC)
          exit(-1)
        print "{}Preparing to download {} from the server.{}".format(bcolors.OKBLUE,bundlefilename,bcolors.ENDC)
        print 
        upload_to_server(bundlefilename)   
    else:
      show_help()
  
    
    
  
  