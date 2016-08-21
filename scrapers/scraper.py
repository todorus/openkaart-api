from urllib import urlopen
import json
from math import ceil
import time
import datetime


def days_hours_minutes(timeDelta):
    return timeDelta.days, timeDelta.seconds//3600, (timeDelta.seconds//60)%60


class Scraper():

    def __init__(self, basePath, typeName, fileName, sortBy):
        self.basePath = basePath
        self.typeName = typeName
        self.fileName = fileName
        self.sortBy = sortBy
        return

    def start(self):
        page = 0
        limit = 1000
        totalPages = 1
        total = 0
        attempt = 1
        maxAttempts = 3

        while page < totalPages:
            try:
                total, passedTime = self.scrape(page, limit, total)

                if page == 0:
                    totalPages = ceil(total / limit)

                if page < totalPages:
                    indexesLeft = totalPages - page
                    timeDelta = datetime.timedelta(seconds=indexesLeft * passedTime)
                    timeString = ", estimated time remaining: %s" % timeDelta

                    page += 1
                    attempt = 1
                    print "moving to %s (%d/%d) %s" % (self.typeName, page, totalPages, timeString)

            except IOError, e:
                print "attempt %d resulted in an IOError" % attempt
                attempt += 1
                if attempt <= maxAttempts:
                    print "retrying"
                else:
                    print "more than %d failed attempts, aborting" % maxAttempts
                    break

    def scrape(self, page, limit, total):

        startTime = time.time()

        content = self.fetch(page, limit)
        total = self.write(content, page)

        passedTime = time.time() - startTime

        return total, passedTime

    def fetch(self, page, limit):
        startIndex = page * limit
        if(self.sortBy is None):
            url = '{}?SERVICE=WFS&request=getFeature&typeName={}&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326&count={}&startIndex={}'.format(self.basePath, self.typeName, limit, startIndex)
        else:
            url = '{}?SERVICE=WFS&request=getFeature&typeName={}&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326&count={}&startIndex={}&sortBy={}'.format(self.basePath, self.typeName, limit, startIndex, self.sortBy)

        print 'fetching: %s' % url
        response = urlopen(url)
        content = response.read()
        return content


    def write(self, json_string, page):
        indexedFilename = "%s.%d" % (self.fileName, page)

        print 'writing: %s' % indexedFilename
        out = open(indexedFilename, 'wb')
        out.write(bytes(json_string))
        out.close()

        data = json.loads(json_string)
        total = data["totalFeatures"]
        return total
