
from django.db import models
from django.utils import timezone

class Base(models.Model):
    '''
    A Base model
    '''
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

class Part(Base):
    '''
    Part's model
    '''
    name = models.CharField(max_length=150, default='')
    sku = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024, default='')
    weight_onces = models.PositiveIntegerField(default=0)
    is_active = models.SmallIntegerField(default=1)

    def __str__(self):
        return 'Part {name} - SKU: {sku}'.format(
            self.name,
            self.sku
        )
    
    class Meta:
        ordering = ('name', '-created_at', )

