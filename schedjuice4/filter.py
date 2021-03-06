from django.db import models
from rest_framework.request import Request

# default django filter-backend needs the use of GenericViews, 
# so I wrote one myself. ez.

def get_fields_from_request(model, request):
    q =  {k:v for k, v in request.GET.items() if v}
    
    fields = set([i.name for i in model._meta.get_fields()])
    invalid_keys = set(q.keys()).union(fields) - set(q.keys()).intersection(fields)
    
    for i in invalid_keys:
        q.pop(i,None)
    return q

def get_filter_query(model:models.Model,request:Request,pre=[]):
    q = get_fields_from_request(model, request)

    return model.objects.filter(**q).prefetch_related(*pre)





