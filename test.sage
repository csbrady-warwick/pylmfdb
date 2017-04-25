import pylmfdb.number_fields as number_fields
import sys

def display_fields(fields):

  for index,el in enumerate(fields):
    print('Element {0} has label {1}'.format(index+1,el.label))
    u = el.get_polynomial_ring(name='a')
    print('Element {0} has defining polynomial {1}'.format(index+1,u))
    u.<a> = el.get_number_field()
    if el.regulator is None:
      u.<a> = el.get_number_field()
      reg = u.regulator()
      print('Element {0} has calculated regulator {1}'.format(index+1,reg))
    else:
      reg = el.regulator
      print('Element {0} has stored regulator {1}'.format(index+1,reg))


#Options to search currently are
#degree - Integer to search by degree
#class_number - Integer to search by class number
#label - String to search by label (will find only one item)
#max_items - Integer to specify the maximum number of elements to return
#base_item - Integer to specify where to start returning values from
#            use with max_items to return data in chunks
#sort - String specifying which database field to sort the results on
print('********************************************')
print('Test 1 : Search by label')
print('********************************************')

fields = number_fields.search(label='2.0.103.1')
display_fields(fields)
print('********************************************')
print('')
print('')
print('********************************************')
print('Test 2 : Search by degree and class number')
print('********************************************')
print('Searching for first 5 items of degree = 3 and class_number = 10, sorted by label')
base_item = 0
fields = number_fields.search(degree=3, class_number = 10, max_items=5, base_item = base_item, sort='label')
print('Retrieved {0} elements, starting from element {1}'.format(len(fields),base_item))
display_fields(fields)
print('********************************************')

