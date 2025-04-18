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
        self.assertIsNone(part)
