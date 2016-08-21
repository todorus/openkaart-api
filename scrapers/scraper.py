from urllib import urlopen
import json
from math import ceil
import time
import datetime


def days_hours_minutes(timeDelta):
    return timeDelta.days, timeDelta.seconds//3600, (timeDelta.seconds//60)%60


class Scraper(object):

    def __init__(self):
        self.limit = 1000
        self.maxAttempt = 3

    def start(self):
        page = 0
        attempt = 1

        while self.hasNext(page):
            try:
                startTime = time.time()
                self.scrape(page, self.limit)
                passedTime = time.time() - startTime
                timeDelta = datetime.timedelta(passedTime)
                print "duration: %s" % timeDelta

                page += 1
                attempt = 1
                print "moving to %s %d" % (self.typeName, page)

            except IOError, e:
                print "attempt %d resulted in an IOError" % attempt
                attempt += 1
                if attempt <= self.maxAttempts:
                    print "retrying"
                else:
                    print "more than %d failed attempts, aborting" % self.maxAttempts
                    break

    def scrape(self, page, limit):

        content = self.fetch(page, limit)
        self.write(content, page)

        return

    def hasNext(page):
        raise NotImplementedError("Subclasses should implement this!")

    def fetch(self, page, limit):
        raise NotImplementedError("Subclasses should implement this!")

    def write(self, json_string, page):
        raise NotImplementedError("Subclasses should implement this!")


class WFSScraper(Scraper):
    def __init__(self, basePath, typeName, fileName, sortBy):
        super(WFSScraper, self).__init__()
        self.basePath = basePath
        self.typeName = typeName
        self.fileName = fileName
        self.sortBy = sortBy
        self.total = 0

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
        self.total = data["totalFeatures"]

    def hasNext(self, page):
        if self.total == 0:
            return True
        else:
            return page < ceil(self.total / self.limit)
