from __future__ import print_function
try:
  from six.moves.urllib.request import urlopen
except:
  raise ImportError('Unable to find six compatability layer. Aborting')
try:
  import json
except:
  raise ImportError('Unable to import json parser')

#Patch raw_input in Python3
try: raw_input = input
except NameError: pass

api_type_searchers = 'API_SEARCHERS'
api_type_descriptions = 'API_DESCRIPTIONS'
api_type_inventory = 'API_INVENTORY'
api_type_records = 'API_RECORDS'
api_type_error = 'API_ERROR'

def get_and_decode(url):
    try:
        page = urlopen(url)
        dat = str(page.read().decode('utf-8'))
        return json.loads(dat)
    except Exception as e:
        print(e)
        return None

class lmfdb_api_searcher:
    def __init__(self, base_url = None):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'http://localhost:37777'

    def _get_searchers(self):
        full_url = self.base_url + "/api2/description/searchers"

        result = get_and_decode(full_url)
        if not result: return None

        if (result['type'] == api_type_searchers):
            return result['data']
        else:
            return None

    def _get_search_fields(self, searcher):
        full_url = self.base_url + "/api2/description/"+searcher

        result = get_and_decode(full_url)
        if not result: return None

        if (result['type'] == api_type_descriptions):
            return result['data']
        else:
            return None

    def _get_data_fields(self, searcher):
        full_url = self.base_url + "/api2/inventory/"+searcher

        result = get_and_decode(full_url)
        if not result: return None

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

        result = get_and_decode(full_url)
        if not result: return None

        if (result['type'] == api_type_records):
            return result['data']
        else:
            return None

    def interactive_search(self):
        val = self._get_searchers()
        if not val:
            print('Unable to get the list of searchers. Check that you can connect to ', self.base_url)
            return
        while(True):
            print('LMFDB has returned the following searchers to select from:')
            print('0) : Cancel search')
            for indx, el in enumerate(val):
                print(str(indx+1) + ") : " + str(val[el]['human_name']))
            print('Select the searcher to use by number')
            data=raw_input('Type d{number} to get the description :')
            if data.startswith('d'):
                try:
                    index = int(data[1:])
                    if index >= 1 or index <= len(val):
                        print('')
                        print('Description for ' + list(val.values())[index-1]['human_name'])
                        try:
                            print(val[el]['desc'])
                        except: pass
                        print('')
                        raw_input('Press a key to continue')
                    else:
                       print('Invalid description')
                except Exception as e: print(e)
            else:
                try:
                    index = int(data)
                    if (index >= 0 and index <= len(val)):
                        break 
                except: pass

        if (index == 0):
            print("Cancelling search")
            return None
        searcher = list(val.keys())[index-1]
        print('Using searcher : '+list(val.values())[index-1]['human_name'])
        fields = self._get_search_fields(searcher)
        if (not fields):
            print('Unable to get fields for searcher. This is a backend problem')
            return None
        else:
            while(True):
                print('LMFDB has returned the following fields that can be searched in:')
                print('0) : Cancel search')
                for indx, el in enumerate(fields):
                    print(str(indx+1) + ") : " + str(el))
                print('Select the field to search in by number')
                data=raw_input('Type d{number} to get the description :')
                if data.startswith('d'):
                    try:
                        index = int(data[1:])
                        if index >= 1 or index <= len(fields):
                            print('')
                            print('Description for ' + list(fields.keys())[index-1])
                            try:
                                print(list(fields.values())['description'])
                            except: pass
                            print('')
                            raw_input('Press a key to continue')
                        else:
                            print('Invalid description')
                    except: pass
                else:
                    try:
                        index = int(data)
                        if (index >= 0 and index <= len(fields)):
                            break
                    except: pass

            if (index == 0):
                print("Cancelling search")
                return None

        sval = raw_input('Please enter the value to search for :')
        return self._search(searcher, {list(fields.keys())[index-1] : sval})
