from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from ninja import NinjaAPI

from core.models import Part

import json
import sys
import traceback
import logging

logging.basicConfig(
    filename = settings.LOG_FILENAME
)

api = NinjaAPI(
    openapi_extra={
        'info': {
            'termsOfService' : 'https://github.com/t3rcio/parts-unlimited'
        },
        'title': 'API Server - Parts Unlimited Project',
        'description': 'API DEMO - Parts Unlimited',
    }
)

@api.get('/parts')
def parts(request):
    parts = Part.objects.all()
    parts_collection = [
        p.to_dict() for p in parts    
    ]
    response = json.dumps(parts_collection)
    return JsonResponse(response, safe=False)

