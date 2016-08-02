import math

# if 'limit' in event and event["limit"] > 0:
#     limit = event["limit"]
# if 'page' in event and event["page"] > 0:
#     page = event["page"]

def paginate(count, **kwargs):
    page = 0
    limit = 10

    if 'limit' in kwargs and kwargs["limit"] > 0:
        limit = kwargs["limit"]
    if 'page' in kwargs and kwargs["page"] > 0:
        page = kwargs["page"]

    if count > 0:
        total = math.ceil(count / limit)
    else:
        total = 1

    return {"current": page, "total": total}
