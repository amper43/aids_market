#!/bin/bash
pip install python-telegram-bot

#redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

pip install redis
