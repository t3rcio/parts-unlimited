
import django
from django.test import TestCase

import json
import random
from string import ascii_uppercase

from core.models import Part

SKU_MAX_SIZE = 30

def get_a_random_sku():
    _sku = ''
    for i in range(0, SKU_MAX_SIZE):
        _sku += random.choice(ascii_uppercase)
    return _sku

class PartsRequestsTestCase(TestCase):
    '''
    Tests for API requests
    '''
    PARTS_GET_URL ='/api/parts'
    PART_GET_URL = '/api/part'
    SKU_SAMPLE = 'OWDD823011DJSD'
    HTTP_SUCCESS = 200
    HTTP_ERROR_REQUEST = 400
    HTTP_NOT_FOUND = 404
    HTTP_SERVER_ERROR = 500    
    
    def setUp(self):
        return super().setUp()
    
    def test_parts_list(self):
        # Test the parts list view
        res = self.client.get(PartsRequestsTestCase.PARTS_GET_URL)
        result = json.loads(res.json())        
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertEqual(type(result), list)        
    
    def test_get_part_by_sku(self):
        # Test the part retrieve by sku parameter in querystring
        res = self.client.get(PartsRequestsTestCase.PART_GET_URL + '/sku=' + PartsRequestsTestCase.SKU_SAMPLE)
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        result = json.loads(res.json())        
        self.assertEqual(result.get('sku'), PartsRequestsTestCase.SKU_SAMPLE)
    
    def test_404_parts(self):
        # Test the search for a inexistent part 
        res = self.client.get(PartsRequestsTestCase.PART_GET_URL + '/sku=some-sku-code')
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_NOT_FOUND)
    
    def test_search_fields(self):
        # Test the search fiels of Part models
        param_to_search_for = 'name'
        value_to_search_for = 'Macrochip'
        res = self.client.get(PartsRequestsTestCase.PARTS_GET_URL + '/param={param}/value={value}'.format(
            param=param_to_search_for, 
            value=value_to_search_for)
        )
        result = res.json()        
        self.assertEquals(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0].get('name'), value_to_search_for)
    
    def test_search_fields_weight_onces(self):
        # Test the search fiels of Part models
        param_to_search_for = 'weight_onces'
        value_to_search_for = 22
        res = self.client.get(PartsRequestsTestCase.PARTS_GET_URL + '/param={param}/value={value}'.format(
            param=param_to_search_for, 
            value=value_to_search_for)
        )
        result = res.json()        
        self.assertEquals(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0].get('weight_onces'), value_to_search_for)
    
    def test_search_field_description(self):
        # Test the search fiels of Part models
        param_to_search_for = 'description'
        value_to_search_for = 'heavy'
        res = self.client.get(PartsRequestsTestCase.PARTS_GET_URL + '/param={param}/value={value}'.format(
            param=param_to_search_for, 
            value=value_to_search_for)
        )
        result = res.json()        
        self.assertEquals(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0].get('name'), 'Macrochip')
    
    def test_inexistent_search_field(self):
        # Test the search fiels with inexistent param
        param_to_search_for = 'some-inexistent-param'
        value_to_search_for = 'heavy'
        res = self.client.get(PartsRequestsTestCase.PARTS_GET_URL + '/param={param}/value={value}'.format(
            param=param_to_search_for, 
            value=value_to_search_for)
        )
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_ERROR_REQUEST)


class PartTestCase(TestCase):

    def setUp(self):
        return super().setUp()
    
    def test_create_valid_part(self):
        part = Part.objects.create(
            name = 'Heavy coil',
            sku = get_a_random_sku(),
            description = 'Tightly wound nickel-gravy alloy spring',
            weight_onces = 22,
            is_active = 1
        )
        self.assertIsNotNone(part)
    
    def test_create_invalid_part(self):
        part = None
        try:
            part = Part.objects.create(
                name = 'Heavy coil',
                sku = '',
                description = "Some part's description",
                weight_onces = 22,
                is_active = 1
            )
        except Exception as _exception:
            part = None
        self.assertIsNone(part)
    
    def test_create_invaid_part_weight_negative(self):
        part = None
        try:
            part = Part.objects.create(
                name = 'Heavy coil',
                sku = '',
                description = "Some part's description",
                weight_onces = -22,
                is_active = 1
            )
        except Exception as _exception:
            part = None
        self.assertIsNone(part)    

    def test_unique_sku(self):
        SKU = 'SOME-SKY-CODE-HERE'
        part = part2 = None
        try:
            part = Part.objects.create(
                name = 'Some example of part',
                sku = SKU,
                description = 'Some sample of part',
                weight_onces = 10,
                is_active = 1
            )
        except Exception as _exception:
            part = None
        
        try:
            part2 = Part.objects.create(
                name = 'Some example of part',
                sku = SKU,
                description = 'Some sample of part',
                weight_onces = 10,
                is_active = 1
            )
        except django.db.utils.IntegrityError:
            part2 = None
        
        self.assertIsNotNone(part)
        self.assertIsNone(part2)
    
    def test_description_length_1024_chars(self):
        a_very_long_description_with_2068_chars ='''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse vel nisl eget lorem facilisis semper. Donec ac aliquam mi. Vivamus eu consequat dolor, eget scelerisque velit. Nulla sed magna congue, vestibulum nibh non, auctor orci. Aenean a neque sit amet erat varius aliquam. Nam pharetra rhoncus est nec auctor. Donec ac sem ac est pharetra semper. Quisque in purus congue, consectetur arcu ac, pharetra nulla.

        Phasellus id semper augue. Praesent vitae augue vel dui elementum ultricies. Sed imperdiet rutrum nibh, vel finibus elit placerat id. In sed posuere ipsum, eu rhoncus quam. Nam sollicitudin velit quis egestas commodo. Nullam tempor nisl vitae rhoncus placerat. Etiam sollicitudin egestas tincidunt.

        Donec feugiat libero leo, hendrerit volutpat leo sagittis non. Quisque urna nulla, pellentesque vitae sem at, efficitur auctor elit. Phasellus tempor convallis felis, in sodales metus hendrerit a. In commodo massa sapien, eu fermentum tortor viverra et. Nunc ullamcorper bibendum turpis at vestibulum. Duis ullamcorper et ante vel eleifend. Donec eget quam ut arcu gravida dapibus ut ac orci. Vestibulum vel tellus risus. Nunc vel lacinia velit. Integer ornare lectus tincidunt justo hendrerit pretium. In interdum lacus et tellus mattis, vitae pulvinar dolor finibus. Morbi congue diam faucibus augue posuere maximus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Praesent nec nunc nunc. Integer ut nulla ullamcorper arcu pulvinar venenatis non tristique nulla.

        Praesent at semper elit, vel rhoncus ligula. Nullam facilisis scelerisque lorem, nec accumsan lectus vestibulum et. Aliquam sagittis elementum leo, a pretium nisi dictum laoreet. Nulla facilisi. Praesent augue diam, sagittis id turpis sed, hendrerit maximus eros. Sed ac libero id erat posuere varius. Duis eu scelerisque nisl, ac elementum velit. Nulla metus elit, sagittis et ligula nec, venenatis porta sapien. Suspendisse ac pellentesque sem, at pellentesque eros.

        Etiam tincidunt dui sem, sit amet semper ex molestie eget. Sed imperdiet sed sem et cursus. Vestibulum luctus turpis et leo cursus, vel molestie nisi tincidunt. Proin nec velit odio. Quisque suscipit, mi vitae pharetra imperdiet, dolor magna tincidunt justo, nec pharetra orci odio eu quam. Pellentesque vitae leo non ligula feugiat rutrum. Duis sodales tortor vel sem faucibus, non pulvinar lectus sollicitudin. Morbi convallis, dolor eget laoreet hendrerit, dolor quam lobortis mauris, eget porta est mi sed dui.
        '''
        part = None
        try:
            part = Part.objects.create(
                name = 'Some example of part',
                sku = 'SOME-SKU-CODE-HERE',
                description = a_very_long_description_with_2068_chars,
                weight_onces = 10,
                is_active = 1
            )
        except Exception as _exception:
            part = None
        
        self.assertIsNone(part)

    # TO DICT Tests
    def test_part_to_dict(self):
        _sku = get_a_random_sku()
        part = Part.objects.create(name='Heavy coil', sku=_sku, description='Tightly wound nickel-gravy alloy spring', weight_onces=22, is_active=1)
        part_dict = part.to_dict()
        self.assertDictContainsSubset({'name':'Heavy coil', 'sku': _sku, 'description': 'Tightly wound nickel-gravy alloy spring', 'weight_onces':22, 'is_active':1}, part_dict)

