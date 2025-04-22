from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from ninja import NinjaAPI
from ninja import Schema

from core.models import Part

import json
import sys
import traceback
import logging

logging.basicConfig(
    filename = settings.LOG_FILENAME
)

class PartSchema(Schema):
    name: str
    sku: str
    description: str
    weight_onces: int
    is_active: int

api = NinjaAPI(
    openapi_extra={
        'info': {
            'termsOfService' : 'https://github.com/t3rcio/parts-unlimited'
        },
        'title': 'API Server - Parts Unlimited Project',
        'description': 'API DEMO - Parts Unlimited',
    }
)

def existent_part(sku):
    '''
    Verify if part with sku value already exists on database
    '''
    return Part.objects.filter(sku=sku).count() > 0


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

@api.get('/parts/param={param}/value={value}')
def parts_by_parameters(request, param, value):
    response = HttpResponse()
    args = dict()
    try:
        if param not in Part.SEARCH_FIELDS:
            response = HttpResponse()
            response.status_code = 400
            response.content = 'The parameter is not a search field. The coiches are: {fields}' .format(
                fields = ', '.join(Part.SEARCH_FIELDS)
            )
            return response
        if param == 'description':
            param = param + '__icontains'
        
        args[param] = value        
        parts = Part.objects.filter(**args)
        if not parts:
            data = []
            response = JsonResponse(data, safe=False)
            return response
        
        data = [p.to_dict() for p in parts]
        response = JsonResponse(data, safe=False)
        return response
    except Exception as _exception:
        trace = traceback.format_exc()
        logging.error(trace + '\n' + str(_exception))
        response.status_code = 500
    return response        

@api.post('/part/new')
def new_part(request, part: PartSchema):
    response = HttpResponse()
    try:
        if not request.method == 'POST' or not request.body:
            response.status_code = 400
            response.text = 'Method not allowed'
            return response
        
        data = json.loads(request.body)    
        response = JsonResponse(data = {'error': 'Part sku already exists', 'field': 'sku'})
        if not existent_part(data.get('sku')):
            new_part = Part.objects.create(**data)
            response = JsonResponse(
                data=new_part.to_dict(),
                safe=False
            )
    except Exception as _exception:
        trace = traceback.format_exc()
        logging.error(trace + '\n' + str(_exception))
        _error = str(_exception).lower()
        error_dict = {
            'error': _error,
            'field': ''
        }
        if ('name' not in _error) \
            and ('weight_onces' not in _error) \
            and ('description' not in _error) \
            and ('sku' not in _error):
            response = HttpResponse()
            response.status_code = 500
            response.text = 'An exception has occured'
        else:
            if 'name' in _error:
                error_dict['field'] = 'name'
            elif 'weight_onces' in _error:
                error_dict['field'] = 'weight_onces'
            elif 'description' in _error:
                error_dict['field'] = 'description'
            elif 'sku' in _error:
                error_dict['field'] = 'sku'
            response = JsonResponse(data=error_dict, safe=False)
    return response    
    
@api.put('/part/sku={sku}')
def update_part(request, sku, part:PartSchema):
    response = HttpResponse()
    try:
        data = json.loads(request.body)    
        response = JsonResponse(data={'error': 'Part sku does not exists', 'field': 'sku'})
        if not existent_part(sku):
            return response
        
        part = Part.objects.filter(sku=sku).first()
        part.__dict__.update(data)
        part.updated_at = timezone.now()
        part.save()
        response = JsonResponse(data=part.to_dict(), safe=False)
    
    except Exception as _exception:
        trace = traceback.format_exc()
        logging.error(trace + '\n' + str(_exception))
        _error = str(_exception).lower()
        error_dict = {
            'error': _error,
            'field': ''
        }
        if ('name' not in _error) \
            and ('weight_onces' not in _error) \
            and ('description' not in _error) \
            and ('sku' not in _error):
            response = HttpResponse()
            response.status_code = 500
            response.text = 'An exception has occured'
        else:
            if 'name' in _error:
                error_dict['field'] = 'name'
            elif 'weight_onces' in _error:
                error_dict['field'] = 'weight_onces'
            elif 'description' in _error:
                error_dict['field'] = 'description'
            elif 'sku' in _error:
                error_dict['field'] = 'sku'
            response = JsonResponse(data=error_dict, safe=False)
    return response

@api.delete('/part/sku={sku}')
def delete_part(request, sku):
    response = HttpResponse()
    try:
        response = JsonResponse(data={'error': 'Part sku does not exists', 'field': 'sku'})
        if not existent_part(sku):
            return response
        
        part = Part.objects.filter(sku=sku).first()        
        part.delete()
        response = JsonResponse(data={'message':'Part deleted', 'sku': sku})
    
    except Exception as _exception:
        trace = traceback.format_exc()
        logging.error(trace + '\n' + str(_exception))
    return response
     