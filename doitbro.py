'do it bro'

import argparse
import traceback
import time

import pymongo

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dburl', default='mongodb://localhost:27017', help='mongodb url without db part [%(default)s]')
    args = parser.parse_args()
    client = pymongo.MongoClient(args.dburl)
    db = client.local
    collection = db['oplog.rs']
    cursor = collection.find(tailable=True)
    while True:
        try:
            if cursor.alive:
                x = cursor.next()
                print(x)
            else: 
                print(cursor)
        except KeyboardInterrupt:
            break
        except StopIteration:
            time.sleep(1)
        except:
            traceback.print_exc()

