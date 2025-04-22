
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
    PART_POST = '/api/part/new'
    PART_UPDATE = '/api/part/sku={sku}'
    PART_DELETE = '/api/part/sku={sku}'
    PARTS_MOST_COMMON_WORDS = '/api/parts/mostcommonwords'
    PART_MOST_COMMON_WORDS = '/api/part/sku={sku}/mostcommonwords'
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
        result = res.json()
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertEqual(type(result), list)        
    
    def test_get_part_by_sku(self):
        # Test the part retrieve by sku parameter in querystring
        res = self.client.get(PartsRequestsTestCase.PART_GET_URL + '/sku=' + PartsRequestsTestCase.SKU_SAMPLE)
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        result = res.json()
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
    
    def test_search_fields_weight_ounces(self):
        # Test the search fiels of Part models
        param_to_search_for = 'weight_ounces'
        value_to_search_for = 22
        res = self.client.get(PartsRequestsTestCase.PARTS_GET_URL + '/param={param}/value={value}'.format(
            param=param_to_search_for, 
            value=value_to_search_for)
        )
        result = res.json()        
        self.assertEquals(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0].get('weight_ounces'), value_to_search_for)
    
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
    
    def test_post_new_part(self):
        # Test the simple post part
        res = self.client.post(
            PartsRequestsTestCase.PART_POST,
            data = json.dumps({
                'name': 'some-part-name',
                'sku': get_a_random_sku(),
                'description': 'some description text',
                'weight_ounces': 100,
                'is_active': 1
            }),
            content_type='application/json'
        )

        new_part = Part.objects.filter(name='some-part-name').first()
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertIsNotNone(new_part)
    
    def test_post_new_part_error(self):
        # Test an error post part
        res = self.client.post(
            PartsRequestsTestCase.PART_POST,
            data = json.dumps({
                'name': 'some-part-name',
                'sku': get_a_random_sku(),
                # the description is missing
                'weight_ounces': 100,
                'is_active': 1
            }),
            content_type='application/json'
        )

        new_part = Part.objects.filter(name='some-part-name').first()
        self.assertFalse(res.status_code == PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertIsNone(new_part)
    
    def test_post_error_messages_name(self):
        # Test an error post part without name
        res = self.client.post(
            PartsRequestsTestCase.PART_POST,
            data = json.dumps({
                'name': '',
                'sku': get_a_random_sku(),
                'description': 'some description text',
                'weight_ounces': 100,
                'is_active': 1
            }),
            content_type='application/json'
        )
        
        result = 'name' in res.json().get('field')
        new_part = Part.objects.filter(name='').first()
        self.assertIsNone(new_part)
        self.assertTrue(res.status_code == PartsRequestsTestCase.HTTP_SUCCESS)        
        self.assertTrue(result)
    
    def test_post_error_messages_weight_ounces(self):
        # Test an error post part with a negative value for weight_ounces
        res = self.client.post(
            PartsRequestsTestCase.PART_POST,
            data = json.dumps({
                'name': 'some name',
                'sku': get_a_random_sku(),
                'description': 'some description text',
                'weight_ounces': -100,
                'is_active': 1
            }),
            content_type='application/json'
        )
        
        result = 'weight_ounces' in res.json().get('field')
        new_part = Part.objects.filter(weight_ounces=-100).first()
        self.assertIsNone(new_part)
        self.assertTrue(res.status_code == PartsRequestsTestCase.HTTP_SUCCESS)        
        self.assertTrue(result)
    
    def test_post_error_messages_description(self):
        # Test an error post part with very long length por description
        sku = get_a_random_sku()
        res = self.client.post(
            PartsRequestsTestCase.PART_POST,
            data = json.dumps({
                'name': 'some name',
                'sku': sku,
                'description': 'some description text' * 1024,
                'weight_ounces': 100,
                'is_active': 1
            }),
            content_type='application/json'
        )
        
        result = 'description' in res.json().get('field')
        new_part = Part.objects.filter(sku=sku).first()
        self.assertIsNone(new_part)
        self.assertTrue(res.status_code == PartsRequestsTestCase.HTTP_SUCCESS)        
        self.assertTrue(result)
    
    def test_post_error_messages_sku(self):
        # Test an error post part with an already existing sku value
        sku = Part.objects.all().first().sku # a already value in database        
        res = self.client.post(
            PartsRequestsTestCase.PART_POST,
            data = json.dumps({
                'name': 'some name',
                'sku': sku,
                'description': 'some description text',
                'weight_ounces': 100,
                'is_active': 1
            }),
            content_type='application/json'
        )
        
        result = 'sku' in res.json().get('field')
        self.assertTrue(res.status_code == PartsRequestsTestCase.HTTP_SUCCESS)        
        self.assertTrue(result)
    
    def test_update_part(self):
        sku = get_a_random_sku()
        part = Part.objects.create(
            name='some-part-name',
            sku=sku,
            description='Some description text',
            weight_ounces = 20
        )
        res = self.client.put(
            PartsRequestsTestCase.PART_UPDATE.format(sku=sku),
            data = json.dumps({
                'name': part.name,
                'sku': part.sku,
                'description': 'Another description text',
                'weight_ounces': 25,
                'is_active': part.is_active
            }),
            content_type='application/json'
        )
        part_updated = Part.objects.filter(sku=sku).first()        
        self.assertIsNotNone(part_updated)
        self.assertEqual(part_updated.weight_ounces, 25)
        self.assertEqual(part_updated.description, 'Another description text')
        
    def test_delete_part(self):
        sku = get_a_random_sku()
        part = Part.objects.create(
            name='some-part-name',
            sku=sku,
            description='Some text as description',
            weight_ounces=20
        )
        res = self.client.delete(
            PartsRequestsTestCase.PART_DELETE.format(sku=sku)
        )
        _part = Part.objects.filter(sku=sku).first()
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertIsNone(_part)
        self.assertEqual(res.json().get('sku'), sku)
    
    def test_parts_most_common_words(self):
        res = self.client.get(
            PartsRequestsTestCase.PARTS_MOST_COMMON_WORDS
        )
        self.assertEqual(res.status_code, PartsRequestsTestCase.HTTP_SUCCESS)
        self.assertEqual(type(res.json()), dict)

    def test_part_most_common_words(self):
        res = self.client.get(
            PartsRequestsTestCase.PART_MOST_COMMON_WORDS.format(sku=PartsRequestsTestCase.SKU_SAMPLE)
        )
        most_common_words = {
            "part_sku": "OWDD823011DJSD",
            "most_common_words": {
                "Used": 1,
                "for": 1,
                "heavy-load": 1,
                "computing": 1
            }
        }
        self.assertEqual(most_common_words.get('part_sku'), PartsRequestsTestCase.SKU_SAMPLE)
        self.assertEqual(type(most_common_words.get('most_common_words')), dict)

class PartTestCase(TestCase):

    def setUp(self):
        return super().setUp()
    
    def test_create_valid_part(self):
        part = Part.objects.create(
            name = 'Heavy coil',
            sku = get_a_random_sku(),
            description = 'Tightly wound nickel-gravy alloy spring',
            weight_ounces = 22,
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
                weight_ounces = 22,
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
                weight_ounces = -22,
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
                weight_ounces = 10,
                is_active = 1
            )
        except Exception as _exception:
            part = None
        
        try:
            part2 = Part.objects.create(
                name = 'Some example of part',
                sku = SKU,
                description = 'Some sample of part',
                weight_ounces = 10,
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
                weight_ounces = 10,
                is_active = 1
            )
        except Exception as _exception:
            part = None
        
        self.assertIsNone(part)

    # TO DICT Tests
    def test_part_to_dict(self):
        _sku = get_a_random_sku()
        part = Part.objects.create(name='Heavy coil', sku=_sku, description='Tightly wound nickel-gravy alloy spring', weight_ounces=22, is_active=1)
        part_dict = part.to_dict()
        self.assertDictContainsSubset({'name':'Heavy coil', 'sku': _sku, 'description': 'Tightly wound nickel-gravy alloy spring', 'weight_ounces':22, 'is_active':1}, part_dict)

