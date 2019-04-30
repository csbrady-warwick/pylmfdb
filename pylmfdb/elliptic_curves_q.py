from lmfdb_api import lmfdb_api_searcher
from sage.schemes.elliptic_curves.constructor import EllipticCurve
class lmfdb_elliptic_curves_q:

    def __init__(self, url = None):
        self._searcher_name = 'elliptic_curves_q' #Hard coded searcher name
        self._searcher = lmfdb_api_searcher(url)
        searchers = self._searcher._get_searchers()
        if not self._searcher_name in searchers.keys(): raise KeyError('Missing API key')
        search_fields = self._searcher._get_search_fields(self._searcher_name)
        self._cnamed_fields = {}
        self._other_fields = []
        self._failed_fields = []
        for el in search_fields:
            try:
                cname = search_fields[el].get('cname', None)
                if (cname):
                    self._cnamed_fields[cname] = el
                else:
                    self._other_fields.append(el)
            except: self._failed_fields.append(el)

    def get_cnames(self):
        return self._cnamed_fields.keys()

    def search(self, **kwargs):
        search_dict = {}
        for el in kwargs:
            if (not el in self._cnamed_fields.keys()):
                if (not el in self._other_fields):
                    raise KeyError('Unknown searcher')
                else:
                    print('"' + el + '" is a non canonical search name.')
                    search_dict[el] = kwargs[el]
            else:
                search_dict[self._cnamed_fields[el]] = kwargs[el]
        start_pos = 0
        vals = {'view_next':0}
        result = []
        while vals['view_next'] >=0:
            vals = self._searcher._search(self._searcher_name, search_dict, start = start_pos)
            for el in vals['records']:
                result.append(EllipticCurve(el['ainvs']))
            start_pos = vals['view_next']
        return result
