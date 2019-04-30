try:
  from six.moves.urllib.request import urlopen
except:
  raise ImportError('Unable to find six compatability layer. Aborting')
try:
  import json
except:
  raise ImportError('Unable to import json parser')

api_type_searchers = 'API_SEARCHERS'
api_type_descriptions = 'API_DESCRIPTIONS'
api_type_inventory = 'API_INVENTORY'
api_type_records = 'API_RECORDS'
api_type_error = 'API_ERROR'

class lmfdb_api_searcher:
    def __init__(self, base_url = None):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'http://localhost:37777'

    def _get_searchers(self):
        full_url = self.base_url + "/api2/description/searchers"
        try:
            page = urlopen(full_url)
            result = json.loads(page.read())
        except:
            return None

        if (result['type'] == api_type_searchers):
            return result['data']
        else:
            return None

    def _get_search_fields(self, searcher):
        full_url = self.base_url + "/api2/description/"+searcher
        try:
            page = urlopen(full_url)
            result = json.loads(page.read())
        except:
            return None

        if (result['type'] == api_type_descriptions):
            return result['data']
        else:
            return None

    def _get_data_fields(self, searcher):
        full_url = self.base_url + "/api2/inventory/"+searcher
        try:
            page = urlopen(full_url)
            result = json.loads(page.read())
        except:
            return None

        if (result['type'] == api_type_descriptions):
            return result['data']
        else:
            return None

    def _get_field_names(self, search_fields, cnames):
        ret = {}
        for el in cnames:
            for el2 in search_fields:
                if search_fields[el2].get('cname',None) == el:
                    ret[el] = el2
                    break
        return ret
 
    def _search(self, searcher, field_names = None, start = None):
        full_url = self.base_url + "/api2/data/"+searcher
        query = []
        if field_names:
            for el in field_names:
                query.append(el+"="+field_names[el])

        if start:
            query.append("_view_start="+str(start))

        if (len(query) > 0):
            full_url += "?" + "&".join(query)

        try:
            page = urlopen(full_url)
            result = json.loads(page.read())
        except:
            return None

        if (result['type'] == api_type_records):
            return result['data']
        else:
            return None

    def interactive_search(self):
        val = self._get_searchers()
        if not val:
            print('Unable to get the list of searchers. Check that you can connect to ', self.base_url)
            return
        print('LMFDB has returned the following searchers:')
        for indx, el in enumerate(val):
            print(str(indx) + ") : " + str(el))

      
