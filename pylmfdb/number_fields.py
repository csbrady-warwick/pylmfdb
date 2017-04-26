# use the six compatibility layer
import sys
try:
  from sage.all import NumberField, PolynomialRing, QQ, ZZ
  insage = True
except:
  insage = False
import json
import api_routines
import lmfdb_api

url_api = lmfdb_api.url_base + 'api/numberfields/fields/?_format=json&'

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
  dbfields = ['label','degree','disc_abs_key', 'disc_sign','galois','reg','coeffs']
  fields = lmfdb_api._get_fields_from_api_page(url_api, searches, dbfields, lmfdb_number_field, **kwargs)
  return fields
