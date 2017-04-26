# use the six compatibility layer
import sys
try:
  from six.moves.urllib.request import urlopen
except:
  raise ImportError('Unable to find six compatability layer. Aborting')
try:
  from sage.all import NumberField, PolynomialRing, QQ, ZZ
  insage = True
except:
  insage = False
import json
import api_routines

url_base = 'http://beta.lmfdb.org'
url_api = 'http://beta.lmfdb.org/api/numberfields/fields/?_format=json&'

class lmfdb_number_field:

  coefficients = None
  degree = None
  discriminant = None
  galois_group = None
  label = None
  regulator = None

  def get_polynomial_ring(self, **kwargs):
    return PolynomialRing(QQ, **kwargs)(self.coefficients)
  def get_number_field(self, **kwargs):
    return NumberField(self.get_polynomial_ring(**kwargs),**kwargs)
  def __init__(self, json):
    self.label = json['label']
    self.coefficients = [int(i) for i in (json['coeffs'].split(','))]
    self.degree = json['degree']
    disc_abs_key = json['disc_abs_key']
    disc_sign = int(json['disc_sign'])
    self.discriminant = ZZ(disc_abs_key[3:]) * disc_sign
    self.galois_group = "%dT%d" % (json['galois']['n'], json['galois']['t'])
    try:
      self.regulator = json['reg']
    except:
      # could use sage to get the regulator, but might be slow
      pass

def _get_fields_from_api_page(base_url, requests, **kwargs):
  full_url = base_url + api_routines.api_amp_list(requests) + "&" + \
      "_fields="+api_routines.api_comma_list(['label','degree','disc_abs_key',
      'disc_sign','galois','reg','coeffs'])
  try:
    offset = int(kwargs['base_item'])
    full_url += "&_offset="+str(offset)
  except:
    pass

  try:
    single_field = kwargs['single_field']
    #This is a bit of a hack. Set the 'max_items' keyword to 2, so that you can detect
    #if the database returns more than one item, but so that you don't drag out too much
    #unnecessary data
    kwargs['max_items'] = 2
  except:
    single_field = False

  fields = []
  count = 0
  max_count = None
  try:
    max_count = int(kwargs['max_items'])
  except:
    pass
  while True:
    try:
      page = urlopen(full_url)
      result = json.loads(page.read())
    except:
      break
    count_this_page = int(result['offset']) - int(result['start'])
    count += count_this_page

    for c in result['data']:
      fields.append(lmfdb_number_field(c))
    if count_this_page < 100:
      break
    if max_count is not None:
      if count >= max_count:
        break
    full_url = url_base + result['next']

  if len(fields) == 0:
    raise RuntimeError
  if single_field:
    if len(fields) != 1:
      print('Warning! Code is returning a single field, but database returned more than one')
    return fields[0]
  if max_count is not None:
    return fields[ : min(len(fields),max_count)]
  return fields

def search( ** kwargs):
  searches=[]
  try:
    searches.append("label="+kwargs['label'])
    #Searches by label return a single value only, so change the
    #return type to be a single value
    kwargs['single_field'] = True
    del kwargs['label']
  except:
    pass

  try:
    searches.append("degree="+api_routines.api_int(kwargs['degree']))
    del kwargs['degree']
  except:
    pass

  try:
    searches.append("class_number="+api_routines.api_int(kwargs['class_number']))
    del kwargs['class_number']
  except:
    pass

  try:
    sort = searches.append("_sort=" + kwargs['sort'])
  except:
    pass

  if len(searches) == 0:
    print('No searches specified, no data will be returned')
    return None
  fields = _get_fields_from_api_page(url_api, searches, **kwargs)
  return fields
