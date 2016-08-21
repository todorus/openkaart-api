from scraper import Scraper

cbsRegionsWFS = 'https://geodata.nationaalgeoregister.nl/cbsgebiedsindelingen/ows'
Scraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_provincie_2016_gegeneraliseerd', '../data/provinces.geo.json', None).start()
Scraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_gemeente_2016_gegeneraliseerd', '../data/municipalities.geo.json', None).start()
Scraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_wijk_2016_gegeneraliseerd', '../data/district.geo.json', None).start()
Scraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_buurt_2016_gegeneraliseerd', '../data/neighborhoods.geo.json', None).start()
Scraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_ggdregio_2016_gegeneraliseerd', '../data/ggd.geo.json', None).start()
Scraper(cbsRegionsWFS, 'cbsgebiedsindelingen:cbs_jeugdzorgregio_2016_gegeneraliseerd', '../data/youthcare.geo.json', None).start()

bagAddressWFS = 'https://geodata.nationaalgeoregister.nl/inspireadressen/wfs'
Scraper(bagAddressWFS, 'inspireadressen:inspireadressen', '../data/adressen.geo.json', "gid").start()

# raise NotImplementedError("Subclasses should implement this!")
