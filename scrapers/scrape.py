from owslib.wfs import WebFeatureService


def scrape(typename, filename):
    wfs11 = WebFeatureService(url='https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows', version='1.1.0')
    response = wfs11.getfeature(typename=typename, outputFormat='json', srsname='urn:x-ogc:def:crs:EPSG:4326')
    out = open(filename, 'wb')
    out.write(bytes(response.read()))
    out.close()

scrape('cbsgebiedsindelingen:cbs_provincie_2016_gegeneraliseerd', 'provinces.geo.json')
scrape('cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd', 'municipalities.geo.json')
scrape('cbsgebiedsindelingen:cbs_wijk_2016_gegeneraliseerd', 'district.geo.json')
scrape('cbsgebiedsindelingen:cbs_buurt_2016_gegeneraliseerd', 'neighborhoods.geo.json')

scrape('cbsgebiedsindelingen:cbs_ggdregio_2016_gegeneraliseerd', 'ggd-regions.geo.json')
scrape('cbsgebiedsindelingen:cbs_jeugdzorgregio_2016_gegeneraliseerd', 'ggd-regions.geo.json')
