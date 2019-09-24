#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 01:39:58 2019

@author: Ray
"""



from os.path import expanduser


if __name__ == '__main__':
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