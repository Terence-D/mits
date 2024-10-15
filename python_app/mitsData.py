import redis
import json
import os
import mitsCommon

redisServer = os.environ.get('REDIS_SERVER_NAME', 'redis')
redisPort = os.environ.get('REDIS_PORT', '6379')
redisDb = 0

r = redis.StrictRedis(host=redisServer, port=redisPort, charset="utf-8", decode_responses=True, db=redisDb)

def scan(prefix):
    return r.scan_iter(prefix + "*")

def set(key, value):
    return r.set (key, value)

def get(key):
    return r.get(key)

def add(media, fullRefresh):
    jsonString = json.dumps(media.__dict__, default=lambda o: o.__dict__, indent=4)
    if (r.exists(media.getUniqueId()) == False or fullRefresh):
        r.set (media.getUniqueId(), jsonString)
        return True
    return False

def remove(foundKeys):
    for key in scan(mitsCommon.moviePrefix):
        if key not in foundKeys:
            r.delete(key)
    for key in scan(mitsCommon.seriesPrefix):
        if key not in foundKeys:
            r.delete(key)

