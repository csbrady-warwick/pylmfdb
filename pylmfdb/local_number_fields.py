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
import lmfdb_api

url_api = lmfdb_api.url_base + 'api/localfields/fields/?_format=json&'

class lmfdb_local_number_field:

  coefficients = None
  degree = None
  discriminant_ideal = None
  galois_group = None
  label = None

  def get_polynomial_ring(self, **kwargs):
    return PolynomialRing(QQ, **kwargs)(self.coefficients)
  def __init__(self, json):
    self.label = json['label']
    self.coefficients = [int(i) for i in (json['coeffs'])]
    GG = json['gal']
    self.degree = GG[0]
    self.discriminant_ideal = "p^{0}".format(json['c'])
    self.galois_group = "%dT%d" % (GG[0], GG[1])

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
    searches.append("p="+api_routines.api_int(kwargs['prime']))
    del kwargs['prime']
  except:
    pass

  try:
    searches.append("n="+api_routines.api_int(kwargs['degree']))
    del kwargs['degree']
  except:
    pass

  try:
    searches.append("c="+api_routines.api_int(kwargs['discriminant_exponent']))
    del kwargs['discriminant_exponent']
  except:
    pass

  try:
    searches.append("e="+api_routines.api_int(kwargs['ramification_index']))
    del kwargs['ramification_index']
  except:
    pass

  try:
    sort = searches.append("_sort=" + kwargs['sort'])
  except:
    pass

  if len(searches) == 0:
    print('No searches specified, no data will be returned')
    return None
  db_fields=['coeffs','label','gal','c']
  fields = lmfdb_api._get_fields_from_api_page(url_api, searches, db_fields,
      lmfdb_local_number_field, **kwargs)
  return fields
