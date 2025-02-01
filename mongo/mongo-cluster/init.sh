#!/bin/bash

sleep 10

mongo --host mongodb_router --port 27017 --eval "sh.addShard('rs1/mongodb_shared_server:27017')"
mongo --host mongodb_config --port 27017 --eval "rs.initiate({_id: 'csvr', configsvr: true, members: [{ _id: 0, host : 'mongodb_config:27017' }]})"

sleep 10
