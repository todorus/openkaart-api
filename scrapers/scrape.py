from urllib import urlopen
import json
from math import ceil
import time
import datetime

def days_hours_minutes(timeDelta):
    return timeDelta.days, timeDelta.seconds//3600, (timeDelta.seconds//60)%60

def scrape(serverBaseUrl, typeName, fileName, page, limit, total, sortBy):
    startIndex = page * limit
    if(sortBy is None):
        url = '{}?SERVICE=WFS&request=getFeature&typeName={}&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326&count={}&startIndex={}'.format(serverBaseUrl, typeName, limit, startIndex)
    else:
        url = '{}?SERVICE=WFS&request=getFeature&typeName={}&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326&count={}&startIndex={}&sortBy={}'.format(serverBaseUrl, typeName, limit, startIndex, sortBy)

    startTime = time.time()
    print 'fetching: %s' % url
    response = urlopen(url)

    if(total == 0):
        data = json.load(response)
        total = data["totalFeatures"]

    page = (startIndex / limit)
    indexedFilename = "%s.%d" % (fileName, page)

    print 'writing: %s' % indexedFilename
    out = open(indexedFilename, 'wb')
    out.write(bytes(response.read()))
    out.close()

    passedTime = time.time() - startTime

    return page, total, passedTime


def start_scrape(serverBaseUrl, typeName, fileName, sortBy):
    page = 0
    limit = 1000
    totalPages = 1
    total = 0
    attempt = 1
    maxAttempts = 3

    while page < totalPages:
        try:
            page, total, passedTime = scrape(serverBaseUrl, typeName, fileName, page, limit, total, sortBy)

            if page == 0:
                totalPages = ceil(total / limit)

            if page < totalPages:
                indexesLeft = totalPages - page
                timeDelta = datetime.timedelta(seconds=indexesLeft * passedTime)
                timeString = ", estimated time remaining: %s" % timeDelta

                page += 1
                attempt = 1
                print "moving to %s (%d/%d) %s" % (typeName, page, totalPages, timeString)

        except IOError, e:
            print "attempt %d resulted in an IOError" % attempt
            attempt += 1
            if attempt <= maxAttempts:
                print "retrying"
            else:
                print "more than %d failed attempts, aborting" % maxAttempts
                break


cbsRegionsWFS = 'https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows'
start_scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_provincie_2016_gegeneraliseerd', '../data/provinces.geo.json', None)
start_scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd', '../data/municipalities.geo.json', None)
start_scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_wijk_2016_gegeneraliseerd', '../data/district.geo.json', None)
start_scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_buurt_2016_gegeneraliseerd', '../data/neighborhoods.geo.json', None)
start_scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_ggdregio_2016_gegeneraliseerd', '../data/ggd.geo.json', None)
start_scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_jeugdzorgregio_2016_gegeneraliseerd', '../data/youthcare.geo.json', None)

bagAddressWFS = 'https://geodata.nationaalgeoregister.nl/inspireadressen/wfs'
start_scrape(bagAddressWFS, 'inspireadressen:inspireadressen', '../data/adressen.geo.json', "gid")
