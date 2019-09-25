#!/bin/bash

#cp dbh.py dbh
#cp dbp.py dbp
chmod +x dbh
chmod +x dbp
chmod +x set_path.py
python set_path.py # set path

if command -v python &>/dev/null; then
    echo "python is installed"
else
    sudo apt-get -y install python
fi

if command -v vim &>/dev/null; then
    echo "vim is installed"
else
    sudo apt-get -y install vim
fi 

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -f "~/.bash_profile" ]; then
	source ~/.bash_profile	
else
	echo "#dbh hook\nexport PATH=$PATH:${DIR}" >> ~/.bash_profile
	source ~/.bash_profile
fi

source ~/.bash_profile

echo 
echo -e "\e[32m ALL DONE! Now try use the following commands anywhere\e[0m"
echo "$ dbh"
echo "$ dbp"
