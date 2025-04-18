
import django
from django.test import TestCase

from core.models import Part

class PartTestCase(TestCase):

    def setUp(self):
        return super().setUp()
    
    def test_create_valid_part(self):
        part = Part.objects.create(
            name = 'Heavy coil',
            sku = 'SDJDDH8223DHJ',
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