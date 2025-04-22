'''
Populates the database with parts
Just for tests
'''

import sqlite3
import random
import os
import sys
from faker import Faker

sys.path.insert(0, '/home/tercio/Projetos/parts-unlimited/app')    
os.environ["DJANGO_SETTINGS_MODULE"] = "parts_unlimited.settings"

import django
django.setup()
from django.conf import settings
from django.utils import timezone

fake = Faker()

db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

MAX_ITEMS = 1025 # 1025 items.. why a 1025? Nothing special, just a random number ;-)

for _ in range(MAX_ITEMS):
    name = fake.word().capitalize() + " " + fake.word().capitalize()
    sku = fake.bothify(text='????########')
    description = fake.sentence(nb_words=6)
    weight_ounces = random.randint(1, 50)
    is_active = random.randint(0, 1)
    created_at = timezone.now().strftime(settings.FORMAT_DATETIME)

    cursor.execute('''
        INSERT INTO core_part (name, sku, description, weight_ounces, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, sku, description, weight_ounces, is_active, created_at)
    )

conn.commit()
conn.close()

print("Done!")
