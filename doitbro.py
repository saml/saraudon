'''do it bro

replSet=rs0
oplogSize=128

'''

import argparse
import traceback
import time
import logging

import pymongo

logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d | %(message)s', level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dburl', default='mongodb://localhost:27017', help='mongodb url without db part [%(default)s]')
    args = parser.parse_args()
    client = pymongo.MongoClient(args.dburl)
    logging.info('connected to %s', args.dburl)
    db = client.local
    collection = db['oplog.rs']
    ts = collection.find().sort('$natural', -1)[0]['ts']
    while True:
        try:
            query = {'ts': {'$gt': ts}}
            logging.debug(query)
            cursor = collection.find(query, tailable=True)
            for op in cursor:
                ts = op['ts']
                logging.info(op)
            time.sleep(1)
        except pymongo.errors.AutoReconnect:
            logging.exception('cannot reconnect')
            time.sleep(1)
