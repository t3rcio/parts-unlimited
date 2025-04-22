
from django.conf import settings
from django.db import models
from django.utils import timezone

class Base(models.Model):
    '''
    A Base model
    '''
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    def to_dict(self):
        return  {}

    class Meta:
        abstract = True

class Part(Base):
    '''
    Part's model
    '''
    SEARCH_FIELDS = ['name', 'sku', 'weight_ounces', 'description']
    DESCRIPTION_MAX_LENGHT = 1024
    name = models.CharField(max_length=150, default='')
    sku = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024, default='')
    weight_ounces = models.PositiveIntegerField(default=0)
    is_active = models.SmallIntegerField(default=1)

    def __str__(self):
        return 'Part {name} - SKU: {sku}'.format(
            name=self.name,
            sku=self.sku
        )
    def save(self, *args, **kwargs):
        if not self.name:
            raise Exception('Name can not be empty')
        if not self.sku:
            raise Exception('SKU can not be empty')
        if self.weight_ounces < 0:
            raise Exception('weight_ounces must be bigger than 0')
        if self.description and len(self.description) > Part.DESCRIPTION_MAX_LENGHT:
            raise Exception('Description can not be bigger the 1024 chars')
        
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'description': self.description,
            'weight_ounces': self.weight_ounces,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime(settings.FORMAT_DATETIME),
            'updated_at': self.updated_at.strftime(settings.FORMAT_DATETIME) if self.updated_at else ''
        } 
    class Meta:
        ordering = ('name', '-created_at', )

