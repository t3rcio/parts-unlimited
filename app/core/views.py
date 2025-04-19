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
    data = json.dumps(parts_collection)
    response = JsonResponse(data, safe=False)    
    return response

@api.get('/part/sku={sku}')
def parts_by_sku(request, sku):
    response = HttpResponse()
    try:
        part = Part.objects.get(sku=sku)
        data = json.dumps(part.to_dict())
        response = JsonResponse(data, safe=False)
    except Part.DoesNotExist:
        response.status_code = 404
    except Exception as _exception:
        trace = traceback.format_exc()
        logging.error(trace + '\n' + str(_exception))
        response.status_code = 500
    
    return response