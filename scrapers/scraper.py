from urllib import urlopen
import json
from math import ceil
import time
import datetime
import os.path
import psycopg2


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
                print "moving to %d" % (page,)

            except IOError, e:
                print "attempt %d resulted in an IOError" % attempt
                attempt += 1
                if attempt <= self.maxAttempts:
                    print "retrying"
                else:
                    print "more than %d failed attempts, aborting" % self.maxAttempts
                    break
        self.close()

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

    def close(self):
        pass


class WFSScraper(Scraper):
    def __init__(self, basePath, typeName, fileName, sortBy):
        super(WFSScraper, self).__init__()
        self.basePath = basePath
        self.typeName = typeName
        self.fileName = fileName
        self.sortBy = sortBy
        self.total = -1

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

    def hasNext(self, currentPage):
        if self.total == -1:
            return True
        else:
            return currentPage < ceil(self.total / self.limit)


class FileScraper(Scraper):
    def __init__(self, basePath):
        super(FileScraper, self).__init__()
        self.basePath = basePath

    def start(self):
        self.conn = psycopg2.connect("dbname=openkaart_development user=todorus")
        self.cur = self.conn.cursor()
        super(FileScraper, self).start()

    def fetch(self, page, limit):
        fileName = "%s.%d" % (self.basePath , page)

        print 'loading: %s' % fileName
        content = open(fileName)
        return content

    def hasNext(self, currentPage):
        fileName = "%s.%d" % (self.basePath, currentPage)
        return os.path.isfile(fileName)

    def write(self, json_string, page):
        raise NotImplementedError("Subclasses should implement this!")

    def close(self):
        self.cur.close()
        self.conn.close()
