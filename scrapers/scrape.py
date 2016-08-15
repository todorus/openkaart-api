from owslib.wfs import WebFeatureService


def scrape(typename, filename):
    wfs11 = WebFeatureService(url='https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows', version='1.1.0')
    response = wfs11.getfeature(typename=typename, outputFormat='json')
    out = open(filename, 'wb')
    out.write(bytes(response.read()))
    out.close()

scrape('cbsgebiedsindelingen:cbs_provincie_2016_gegeneraliseerd', 'provinces.json')
scrape('cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd', 'municipalities.json')
scrape('cbsgebiedsindelingen:cbs_wijk_2016_gegeneraliseerd', 'district.json')
scrape('cbsgebiedsindelingen:cbs_buurt_2016_gegeneraliseerd', 'neighborhoods.json')

scrape('cbsgebiedsindelingen:cbs_ggdregio_2016_gegeneraliseerd', 'ggd-regions.json')
scrape('cbsgebiedsindelingen:cbs_jeugdzorgregio_2016_gegeneraliseerd', 'ggd-regions.json')
