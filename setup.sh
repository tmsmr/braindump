#!/usr/bin/env bash

STARTDIR=`pwd`
mkdir /tmp/braindump && cd /tmp/braindump
wget https://github.com/opthomas-prime/braindump/archive/master.zip
unzip master.zip
sudo install -Tv -m 777 braindump-master/braindump.py /usr/local/bin/braindump.py
sudo ln -vs /usr/local/bin/braindump.py /usr/local/bin/brian
sudo pip3 install whoosh
cd $STARTDIR
rm -r /tmp/braindump
