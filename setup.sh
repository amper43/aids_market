#!/bin/bash
pip install python-telegram-bot

#redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install
rm -rf redis-stable*

pip install redis

nohup redis-server 2>&1 1>/dev/null &
