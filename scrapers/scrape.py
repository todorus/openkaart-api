from urllib import urlopen
import json
from math import floor
import time
import datetime

def days_hours_minutes(timeDelta):
    return timeDelta.days, timeDelta.seconds//3600, (timeDelta.seconds//60)%60

# https://geodata.nationaalgeoregister.nl/inspireadressen/wfs?version=2.0.0&request=getFeature&typeName=inspireadressen:inspireadressen&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326&count=10&startIndex=0&sortBy=gid
def scrape(serverBaseUrl, typeName, fileName, startIndex, total, sortBy):
    limit = 1000

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

    index = (startIndex / limit)
    indexedFilename = "%s.%d" % (fileName, index)

    print 'writing: %s' % indexedFilename
    out = open(indexedFilename, 'wb')
    out.write(bytes(response.read()))
    out.close()

    lastIndex = startIndex + limit


    if lastIndex < total:
        passedTime = time.time() - startTime
        totalIndex = floor(total / limit)
        indexesLeft = totalIndex - index
        timeDelta = datetime.timedelta(seconds=indexesLeft * passedTime)
        timeString = ", estimated time remaining: %s" % timeDelta

        print "moving to %s (%d/%d) %s" % (typeName, index+1, totalIndex, timeString)
        scrape(serverBaseUrl, typeName, fileName, startIndex+limit, total, sortBy)


cbsRegionsWFS = 'https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows'
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_provincie_2016_gegeneraliseerd', '../data/provinces.geo.json', 0, 0, None)
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd', '../data/municipalities.geo.json', 0, 0, None)
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_wijk_2016_gegeneraliseerd', '../data/district.geo.json', 0, 0, None)
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_buurt_2016_gegeneraliseerd', '../data/neighborhoods.geo.json', 0, 0, None)
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_ggdregio_2016_gegeneraliseerd', '../data/ggd.geo.json', 0, 0, None)
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_jeugdzorgregio_2016_gegeneraliseerd', '../data/youthcare.geo.json', 0, 0, None)

bagAddressWFS = 'https://geodata.nationaalgeoregister.nl/inspireadressen/wfs'
scrape(bagAddressWFS, 'inspireadressen:inspireadressen', '../data/adressen.geo.json', 0, 0, "gid")
