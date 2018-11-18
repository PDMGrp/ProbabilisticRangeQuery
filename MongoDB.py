#!/usr/bin/python

# Copyright (c) 2017 ObjectLabs Corporation
# Distributed under the MIT license - http://opensource.org/licenses/MIT

__author__ = 'mLab'

# Written with pymongo-3.4
# Documentation: http://docs.mongodb.org/ecosystem/drivers/python/
# A python script connecting to a MongoDB given a MongoDB Connection URI.

import sys
import pymongo
import datetime


### Create seed data



### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

# uri = 'mongodb://user:pass@host:port/db'
uri = 'mongodb://pdmGroup4:pdmGroup4@ds129762.mlab.com:29762/pdm_sensor_data'


###############################################################################
# main
###############################################################################

def main(sw_size, start_time, counter):
    client = pymongo.MongoClient(uri)

    db = client.get_database()

    # First we'll add a few songs. Nothing is required to create the songs
    # collection; it is created automatically when we insert.

    # songs = db['songs']
    pdm_dataset = db['datasetpdm']
    # Note that the insert method can take either an array or a single dict.

    
    #end_time = input("Please enter your end time of query (YYYY-M-D-H-M): ")
    
    #stime_list = start_time.split('-')
    #etime_list = end_time.split('-')
    # Then we need to give Boyz II Men credit for their contribution to
    # the hit "One Sweet Day".
    #d = datetime.datetime(int(stime_list[0]), int(stime_list[1]), int(stime_list[2]), int(stime_list[3]))
    d = start_time + datetime.timedelta(hours = counter)

    '''
    end_time = start_time + 
    end_h = int(stime_list[3]) + sw_size
    if end_h > 24:
        end_h = end_h % 24
    end_m = int(stime_list[1]) + 1
    '''

    d2 = d + datetime.timedelta(hours = sw_size)

    #d2 = datetime(int(etime_list[0]), int(etime_list[1]), int(etime_list[2]), int(etime_list[3]),int(etime_list[4]))

    print(d, d2)
    query = {"$and":[{'dateTime':{'$gt':d}},{'dateTime':{'$lt':d2}}]}

    # Finally we run a query which returns all the hits that spent 10 or
    # more weeks at number 1.
    cursor = pdm_dataset.find(query)

    #for doc in cursor:
    #    print((doc['dateTime']))
    #    print((doc['temperature']))

    ### Since this is an example, we'll clean up after ourselves.
    min_temp = cursor[0]['temperature']
    max_temp = 0
    min_humidity = cursor[0]['humidity']
    max_humidity = 0
    db = []
    for doc in cursor:
        # print((doc['dateTime']))
        if doc['humidity'] >= 0 and doc['humidity'] <= 100:
            db.append([doc['dateTime'],doc['sensorId'],doc['temperature'],doc['humidity']])
            if doc['temperature'] < min_temp:
                min_temp = doc['temperature']
            if doc['temperature'] > max_temp:
                max_temp = doc['temperature']
            if doc['humidity'] < min_humidity:
                min_humidity = doc['humidity']
            if doc['humidity'] > max_humidity:
                max_humidity = doc['humidity']

        #db.append(doc['dateTime','sensorId','temperature','humidity'])
    
    #print(db)
    ### Only close the connection when your app is terminating

    print("Minimum Temperature within the range: ",min_temp)
    print("Maximum Temperature within the range: ",max_temp)
    print("Minimum Humidity within the range: ",min_humidity)
    print("Maximum Humidity within the range: ",max_humidity)

    client.close()
    return db


if __name__ == '__main__':
    main()
