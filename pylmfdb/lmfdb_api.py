from api_routines import *
try:
  from six.moves.urllib.request import urlopen
except:
  raise ImportError('Unable to find six compatability layer. Aborting')
try:
  import json
except:
  raise ImportError('Unable to import json parser')

base_url = 'http://localhost:37777'

def _get_searchers():
    full_url = base_url + "/api2/description/searchers"
    try:
        page = urlopen(full_url)
        result = json.loads(page.read())
    except:
        return None

    if (result['type'] == api_type_searchers):
        return result['data']
    else:
        return None

def _get_search_fields(searcher):
    full_url = base_url + "/api2/description/"+searcher
    try:
        page = urlopen(full_url)
        result = json.loads(page.read())
    except:
        return None

    if (result['type'] == api_type_descriptions):
        return result['data']
    else:
        return None

def _get_data_fields(searcher):
    full_url = base_url + "/api2/inventory/"+searcher
    try:
        page = urlopen(full_url)
        result = json.loads(page.read())
    except:
        return None

    if (result['type'] == api_type_descriptions):
        return result['data']
    else:
        return None

def _get_field_names(search_fields, cnames):
    ret = {}
    for el in cnames:
        for el2 in search_fields:
            if search_fields[el2].get('cname',None) == el:
                ret[el] = el2
                break
    return ret
 
def _search(searcher, field_names = None, start = None):
    full_url = base_url + "/api2/data/"+searcher
    query = []
    if field_names:
        for el in field_names:
            query.append(el+"="+field_names[el])

    if start:
        query.append("_view_start="+str(start))

    if (len(query) > 0):
        full_url += "?" + "&".join(query)

    print(full_url)
    try:
        page = urlopen(full_url)
        result = json.loads(page.read())
    except:
        return None

    if (result['type'] == api_type_records):
        return result['data']
    else:
        return None
