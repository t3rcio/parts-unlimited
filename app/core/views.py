from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from ninja import NinjaAPI
from ninja import Schema

from core.models import Part
from core.paging import paginate_items

import json
import sys
import traceback
import logging

logging.basicConfig(
    filename = settings.LOG_FILENAME
)

MIN_SIZE_WORD = 3
WORDS_MOST_COMMON_LIMIT = 5
PAGE_SIZE = 10
class PartSchema(Schema):
    name: str
    sku: str
    description: str
    weight_ounces: int
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

def home(request):
    return redirect ('/api/docs')

def existent_part(sku):
    '''
    Verify if part with sku value already exists on database
    '''
    return Part.objects.filter(sku=sku).count() > 0


@api.get('/parts')
def parts(request, page=1):
    data = {}
    parts = Part.objects.all()
    parts_collection = [
        p.to_dict() for p in parts    
    ]
    items, pages = paginate_items(parts_collection, page_size=PAGE_SIZE)
    data['items'] = items.get(page)
    data['pages'] = pages
    data['current_page'] = page
    data['next_page'] = '/api/parts?page=' + str(page+1) if page < pages else ''
    data['previous_page'] = '/api/parts?page=' + str(page-1) if page > 1 else ''
    response = JsonResponse(data, safe=False)    
    return response

@api.get('/part/sku={sku}')
def parts_by_sku(request, sku):
    response = HttpResponse()
    try:
        part = Part.objects.get(sku=sku)
        data = part.to_dict()
        response = JsonResponse(data, safe=False)
    except Part.DoesNotExist:
        response.status_code = 404
    except Exception as _exception:
        trace = traceback.format_exc()
        logging.error(trace + '\n' + str(_exception))
        response.status_code = 500
    
    return response

@api.get('/parts/param={param}/value={value}')
def parts_by_parameters(request, param, value, page=1):
    response = HttpResponse()
    args = dict()
    data = {}
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
        
        parts_collection = [p.to_dict() for p in parts]
        items, pages = paginate_items(parts_collection, page_size=PAGE_SIZE)
        data['items'] = items.get(page)
        data['pages'] = pages
        data['current_page'] = page
        data['next_page'] = ('/api/parts/param={param}/value={value}?page=' + str(page+1) if page < pages else '').format(param=param, value=value)
        data['previous_page'] = ('/api/parts/param={param}/value={value}?page=' + str(page-1) if page > 1 else '').format(param=param, value=value)
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
            and ('weight_ounces' not in _error) \
            and ('description' not in _error) \
            and ('sku' not in _error):
            response = HttpResponse()
            response.status_code = 500
            response.text = 'An exception has occured'
        else:
            if 'name' in _error:
                error_dict['field'] = 'name'
            elif 'weight_ounces' in _error:
                error_dict['field'] = 'weight_ounces'
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
            and ('weight_ounces' not in _error) \
            and ('description' not in _error) \
            and ('sku' not in _error):
            response = HttpResponse()
            response.status_code = 500
            response.text = 'An exception has occured'
        else:
            if 'name' in _error:
                error_dict['field'] = 'name'
            elif 'weight_ounces' in _error:
                error_dict['field'] = 'weight_ounces'
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

@api.get('/parts/mostcommonwords')
def most_common_words(request):
    '''
    Return the most common words in all parts
    '''
    descriptions = ''.join(Part.objects.all().values_list('description', flat=True))
    res = dict()
    for d in descriptions.split(' '):
        if d not in res and len(d) > MIN_SIZE_WORD:
            res[d] = descriptions.count(d)
    sorted_items = sorted(res.items(), key=lambda x : x[1], reverse=True)
    res = {}
    for k, v in sorted_items[0:WORDS_MOST_COMMON_LIMIT]:
        res[k] = v
    response = JsonResponse(data=res)
    return response

@api.get('part/sku={sku}/mostcommonwords')
def most_commom_words_by_part(request, sku):
    '''
    Return the most common words in a especific part description
    '''
    part = Part.objects.filter(sku=sku).first()
    if not part:
        response = JsonResponse(data={})
        return response
    res = {}
    for d in part.description.split(' '):
        if d not in res and len(d) > MIN_SIZE_WORD:
            res[d] = part.description.count(d)
    sorted_res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    res = {}
    for k, v in sorted_res[0:WORDS_MOST_COMMON_LIMIT]:
        res[k] = v
    response = JsonResponse(data={'part_sku': sku, 'most_common_words': res })
    return response    
