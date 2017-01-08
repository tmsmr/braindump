#!/usr/bin/env bash

wget -v https://github.com/opthomas-prime/braindump/archive/master.zip -O /tmp/braindump-master.zip
unzip -v /tmp/braindump-master.zip -d /tmp
sudo install -Tv -m 777 /tmp/braindump-master/braindump.py /usr/local/bin/braindump.py
sudo ln -vs /usr/local/bin/braindump.py /usr/local/bin/brian
sudo pip3 install whoosh
