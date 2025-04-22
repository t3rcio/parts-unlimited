from django.conf import settings

PAGE_SIZE_DEFAULT = 50
PAGE_SIZE = getattr(settings, 'PAGE_SIZE', PAGE_SIZE_DEFAULT)

def paginate_items(items:list, page_size:int = None) -> dict:
    '''
    Returns a dict with paginated items     
    If page_size is not defined: page_size =  settings.PAGE_SIZE or PAGE_SIZE_DEFAULT(5)
    '''
    pg_size = page_size if page_size else PAGE_SIZE    
    paginated_result = {}
    how_many_pages = int(len(items) / pg_size if not len(items) % pg_size else (len(items) / pg_size) + 1)
    
    if how_many_pages < 1:
        how_many_pages = 1
    
    if how_many_pages == 1:
        paginated_result[1] = items
        return paginated_result, how_many_pages
    
    for i in list(range(0, how_many_pages)):        
        start = (i*pg_size)
        end = (pg_size * (i+1))
        if end > len(items):
            end = len(items) - 1
        
        __items = items[start:end]
        paginated_result[i+1] = __items
    
    return paginated_result, how_many_pages