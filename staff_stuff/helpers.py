from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from .filter import get_filter_query




def getlist_helper(self,request:Request):
    query = get_filter_query(self.model,request,pre=self.related_fields)
    page = self.paginate_queryset(query,request)
    
    seri = self.serializer(page,many=True,fields=request.query_params.get("fields"))
    

    return self.get_paginated_response(seri.data, status=status.HTTP_200_OK)

def getdetails_helper(self,request:Request,obj_id):
    obj = get_object_or_404(self.model,pk=obj_id)
    seri = self.serializer(obj,fields=request.query_params.get("fields"))
    
    return Response(seri.data, status=status.HTTP_200_OK)

def post_helper(self, request:Request):
        seri = self.serializer(data=request.data)
        if seri.is_valid():

            seri.save()
            return Response(seri.data, status=status.HTTP_201_CREATED)
        return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)

def put_helper(self,request:Request, obj_id):
    obj = get_object_or_404(self.model,pk=obj_id)
    seri = self.serializer(obj,data=request.data,partial=True)
    
    if seri.is_valid():
        seri.save()

        return Response(seri.data, status=status.HTTP_200_OK)
    return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_helper(self,request:Request, obj_id):
    obj = get_object_or_404(self.model,pk=obj_id)
    seri = self.serializer(obj).data
    obj.delete()

    return Response(seri, status=status.HTTP_200_OK)

