from urllib import urlopen


def scrape(serverBaseUrl, typeName, fileName):
    url = '{}?SERVICE=WFS&request=getFeature&typeName={}&outputFormat=json&srsName=urn:x-ogc:def:crs:EPSG:4326'.format(serverBaseUrl, typeName)

    print 'fetching: {}'.format(url)
    response = urlopen(url)

    print 'writing: {}'.format(fileName)
    out = open(fileName, 'wb')
    out.write(bytes(response.read()))
    out.close()


cbsRegionsWFS = 'https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows'
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_provincie_2016_gegeneraliseerd', 'provinces.geo.json')
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd', 'municipalities.geo.json')
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_wijk_2016_gegeneraliseerd', 'district.geo.json')
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_buurt_2016_gegeneraliseerd', 'neighborhoods.geo.json')
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_ggdregio_2016_gegeneraliseerd', 'ggd.geo.json')
scrape(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_jeugdzorgregio_2016_gegeneraliseerd', 'youthcare.geo.json')

bagAddressWFS = 'https://geodata.nationaalgeoregister.nl/inspireadressen/wfs'
scrape(bagAddressWFS, 'inspireadressen:inspireadressen', 'adressen.geo.json')
