api_type_searchers = 'API_SEARCHERS'
api_type_descriptions = 'API_DESCRIPTIONS'
api_type_inventory = 'API_INVENTORY'
api_type_records = 'API_RECORDS'
api_type_error = 'API_ERROR'

def api_string(value):
  return "s" + str(value)

def api_int(value):
  return "i" + str(value)

def api_float(value):
  return "f" + str(value)

def api_sep_list(separator, values):
  return separator.join(str(s) for s in values)

def api_comma_list(values):
  return api_sep_list(',', values)

def api_amp_list(values):
  return api_sep_list('&',values)

def api_prefix_list(prefix, values):
  return str(prefix) + api_comma_list(values)

def api_string_list(values):
  return api_prefix_list('ls',values)

def api_int_list(values):
  return api_prefix_list('li',values)

def api_float_list(values):
  return api_prefix_list('lf',values)
