#!/bin/bash
pip install python-telegram-bot

#telegram-cli
git clone --recursive https://github.com/vysheng/tg.git && cd tg
./configure
make
#zypper in lua-devel libconfig-devel readline-devel libevent-devel libjansson-devel python-devel libopenssl-devel

cp bin/telegram-cli ../


#redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install
rm -rf redis-stable*

pip install redis

nohup redis-server 2>&1 1>/dev/null &
