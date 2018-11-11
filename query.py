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

def main(args):
    client = pymongo.MongoClient(uri)

    db = client.get_default_database()

    # First we'll add a few songs. Nothing is required to create the songs
    # collection; it is created automatically when we insert.

    # songs = db['songs']
    pdm_dataset = db['datasetpdm']
    # Note that the insert method can take either an array or a single dict.


    # Then we need to give Boyz II Men credit for their contribution to
    # the hit "One Sweet Day".
    d = datetime(2004, 3, 3, 3)

    query = {'temperature': 38.8039,'dateTime':{'$gt':d}}


    # Finally we run a query which returns all the hits that spent 10 or
    # more weeks at number 1.
    print(d)
    cursor = pdm_dataset.find(query)

    for doc in cursor:
        print((doc['dateTime']))
        print((doc['temperature']))

    ### Since this is an example, we'll clean up after ourselves.


    ### Only close the connection when your app is terminating

    client.close()


if __name__ == '__main__':
    main(sys.argv[1:])
