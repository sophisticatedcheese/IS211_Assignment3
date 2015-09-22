__author__ = 'Terence Jeremiah. September 2015'

import datetime
import logging
import sys
import urllib2
import pprint
import random
import argparse
import csv
import re
import operator

def main():

    def grabber(info):
        response = urllib2.urlopen(info)
        return response

    def process(link):

        cata=csv.reader(link)

        dates= '%Y-%m-%d %H:%M:%S'
        hits= imgHits=0
        firefox = chrome = iee = safari = 0

        time={}
        for t in range(0,24):
            time[t]=0

        for col in cata:
            result= {'path':col[0], 'data':col[1], 'browser':col[2], 'status':col[3],'size':col[4]}

            date = datetime.datetime.strptime(result['date'], dates)
            time[date.hour]=time[date.hour]+1
            hits=hits+1

            if re.search(r"\.(?:jpg|jpeg|gif|png)$", result['path'], re.I | re.M):
                imgHits=imgHits+1

            if re.search("chrome/\d+", result['browser'], re.I ):
                chrome=chrome+1

            if re.search('safari', result['browser'], re.I) and not re.search("chrome/\d+", result['browser'], re.I):
                safari=safari+1

            if re.search('firefox', result['browser'], re.I):
                firefox=firefox+1

            if re.search("msie", result['browser'], re.I):
                iee=iee+1

        tempTime=time
        for t in range(0,24):
            id = (max(tempTime.iteritems(), key = operator.itemgetter(1))[0])
            print "Hour %02d has %s hits today" % (id, tempTime[id])
            tempTime.pop(id)

        imageRequest = (imgHits/hits)*100
        browsers = {'Safari': safari, 'Chrome':chrome, 'Firefox': firefox, 'IEE': iee}
        print "Image account request for {0:0.1f} of requests".format(imageRequest)
        print "The popular Browser is %s" % (max(browsers.iteritems(), key=operator.itemgetter(1))[0])

    url_parser=argparse.ArgumentParser()
    url_parser.add_argument("--url", help= 'enter URL", type = str')
    args=url_parser.parse_args()

    if args.url:
        try:
            csvData=grabber(args.url)
            grabHits=process(csvData)
        except:
            print "Error on URL"
    else:
        print "Enter URL or CSV file"

if __name__ == "__main__":
    main()












