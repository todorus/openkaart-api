from __future__ import print_function

import json
import logging


log = logging.getLogger()
log.setLevel(logging.INFO)


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    return event
