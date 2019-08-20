from __future__ import print_function
from builtins import object
import types
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

def get_and_decode(url):
    try:
        page = urlopen(url)
        dat = str(page.read().decode('utf-8'))
        return json.loads(dat)
    except Exception as e:
        return None

class meta_base(object):
    def __getitem__(self, value):
        return vars(self)[value]

    def __str__(self):
        return str(vars(self))

def build_object(name, keys, docs, obj_prototype):
    attrs = {'__doc__':docs}
    proto = type(name, (obj_prototype,), attrs)
    val = proto()
    try:
        for el in keys:
            setattr(val, el, keys[el])
    except:
        pass
    return val

class lmfdb_search(object):
    def __init__(self, api_searcher, query, docs, obj_prototype = meta_base):
        self.api_searcher = api_searcher
        self.query = query
        self.docs = docs
        self.start = 0
        self.obj_prototype = obj_prototype
        self._load()

    def _load(self):
        self.result = self.api_searcher._search_inner(self.query['searcher'], self.query['field_names'], self.start)
        self.start = self.result['view_next']
        self._retindex = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            val = build_object('LMFDB_search_result', self.result['records'][self._retindex], self.docs, self.obj_prototype)
        except IndexError:
            if (self.result['view_next'] < 0): raise StopIteration
            self._load()
            val = build_object('LMFDB_search_result', self.result['records'][self._retindex], self.docs, self.obj_prototype)
        self._retindex = self._retindex + 1
        return val

    def __len__(self):
        return len(self.result['records'])

    def __getitem__(self, index):
        if (self.result):
            return build_object('LMFDB_search_result', self.result['records'][index], self.docs, self.obj_prototype)
        else:
            raise IndexError

class lmfdb_api_searcher:
    def __init__(self, base_url = None):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'http://localhost:37777'

        self.search = None
        self.start = 0

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

        if (result['type'] == api_type_inventory):
            return result['data']
        else:
            return None

    def _get_doc_strings(self, searcher):
        data = self._get_data_fields(searcher)
        str=""
        for el in data:
            try:
                str+=el + ' - ' + data[el]['description'] + '\n'
            except:
                str+= el + ' - '  + 'No data in inventory, please update\n'
        return str

    def _get_field_names(self, search_fields, cnames):
        ret = {}
        for el in cnames:
            for el2 in search_fields:
                if search_fields[el2].get('cname',None) == el:
                    ret[el] = el2
                    break
        return ret

    def _search(self, searcher, field_names = None, start = None, obj_prototype = meta_base):
        query = {'searcher':searcher,'field_names':field_names}
        return lmfdb_search(self, query, self._get_doc_strings(searcher), obj_prototype)
 
    def _search_inner(self, searcher, field_names = None, start = None):
        full_url = self.base_url + "/api2/data/"+searcher
        query = []
        if field_names:
            for el in field_names:
                query.append(el+"="+str(field_names[el]))

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
