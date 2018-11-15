#!/usr/bin/python

# Copyright (c) 2017 ObjectLabs Corporation
# Distributed under the MIT license - http://opensource.org/licenses/MIT

__author__ = 'mLab'

# Written with pymongo-3.4
# Documentation: http://docs.mongodb.org/ecosystem/drivers/python/
# A python script connecting to a MongoDB given a MongoDB Connection URI.

import sys
import pymongo
from datetime import datetime, date, time


### Create seed data



### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

# uri = 'mongodb://user:pass@host:port/db'
uri = 'mongodb://pdmGroup4:pdmGroup4@ds129762.mlab.com:29762/pdm_sensor_data'


###############################################################################
# main
###############################################################################

def main():
    client = pymongo.MongoClient(uri)

    db = client.get_database()

    # First we'll add a few songs. Nothing is required to create the songs
    # collection; it is created automatically when we insert.

    # songs = db['songs']
    pdm_dataset = db['datasetpdm']
    # Note that the insert method can take either an array or a single dict.

    start_time = input("Please enter your start time of query (YYYY-M-D-H-M): ")
    end_time = input("Please enter your end time of query (YYYY-M-D-H-M): ")
    
    stime_list = start_time.split('-')
    etime_list = end_time.split('-')
    # Then we need to give Boyz II Men credit for their contribution to
    # the hit "One Sweet Day".
    d = datetime(int(stime_list[0]), int(stime_list[1]), int(stime_list[2]), int(stime_list[3]),int(stime_list[4]))
    d2 = datetime(int(etime_list[0]), int(etime_list[1]), int(etime_list[2]), int(etime_list[3]),int(etime_list[4]))

    print(d, d2)
    query = {"$and":[{'temperature': 38.8039},{'dateTime':{'$gt':d}},{'dateTime':{'$lt':d2}}]}

    # Finally we run a query which returns all the hits that spent 10 or
    # more weeks at number 1.
    cursor = pdm_dataset.find(query)

    #for doc in cursor:
    #    print((doc['dateTime']))
    #    print((doc['temperature']))

    ### Since this is an example, we'll clean up after ourselves.
    db = []
    for doc in cursor:
        # print((doc['dateTime']))
        db.append(doc['dateTime'],doc['sensorId'],doc['temperature'],doc['humidity'])
        #db.append(doc['dateTime','sensorId','temperature','humidity'])
    
    print(db)
    ### Only close the connection when your app is terminating

    client.close()
    return db


if __name__ == '__main__':
    main()
