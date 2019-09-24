#!/bin/bash

cp dbh.py dbh
cp dbp.py dbp
chmod +x dbh
chmod +x dbp
chmod +x set_path.py
python set_path.py # set path

echo 
echo -e "\e[32m ALL DONE! Now try use the following commands anywhere\e[0m"
echo "$ dbh"
echo "$ dbp"