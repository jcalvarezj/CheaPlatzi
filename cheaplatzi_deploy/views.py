from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from cheaplatzi_deploy.models import ProductType, Ecommerce, Product
from cheaplatzi_deploy.serializers import ProductTypeSerializer, EcommerceSerializer, ProductSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def producttype_list(request):
    if request.method == 'GET':
        productTypes = ProductType.objects.all()
        
        name = request.GET.get('name', None)
        if name is not None:
            productTypes = productTypes.filter(name__icontains=name)
        
        producttypes_serializer = ProductTypeSerializer(productTypes, many=True)
        return JsonResponse(producttypes_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        producttype_data = JSONParser().parse(request)
        producttypes_serializer = ProductTypeSerializer(data=producttype_data)
        if producttypes_serializer.is_valid():
            producttypes_serializer.save()
            return JsonResponse(producttypes_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(producttypes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = ProductType.objects.all().delete()
        return JsonResponse({'message': '{} Product types were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def ecommerce_list(request):
    if request.method == 'GET':
        Ecommerces = Ecommerce.objects.all()
        
        name = request.GET.get('name', None)
        if name is not None:
            Ecommerces = Ecommerces.filter(name__icontains=name)
        
        ecommerce_serializer = EcommerceSerializer(Ecommerces, many=True)
        return JsonResponse(ecommerce_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        ecommerce_data = JSONParser().parse(request)
        ecommerce_serializer = EcommerceSerializer(data=ecommerce_data)
        if ecommerce_serializer.is_valid():
            ecommerce_serializer.save()
            return JsonResponse(ecommerce_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(ecommerce_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Ecommerce.objects.all().delete()
        return JsonResponse({'message': '{} Product types were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'DELETE'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.filter(status=True)
        
        name = request.GET.get('name', None)
        id_type_product = request.GET.get('id_type_product', None)
        id_ecommerce = request.GET.get('id_ecommerce', None)
        if name is not None:
            products = products.filter(name__icontains=name)

        if id_type_product is not None:
            products = products.filter(id_type_product=id_type_product)
        
        if id_ecommerce is not None:
            products = products.filter(id_ecommerce=id_ecommerce)

        product_serializer = ProductSerializer(products, many=True)
        return JsonResponse(product_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(data=product_data, many=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED,  safe=False) 
        return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST,  safe=False)
    elif request.method == 'DELETE':
        count = Product.objects.all().delete()
        return JsonResponse({'message': '{} Product types were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def producttype_detail(request, pk):
    producttype = ProductType.objects.get(pk=pk)
 
    if request.method == 'GET': 
        producttypes_serializer = ProductTypeSerializer(producttype) 
        return JsonResponse(producttypes_serializer.data) 
    elif request.method == 'PUT': 
        producttype_data = JSONParser().parse(request) 
        producttypes_serializer = ProductTypeSerializer(producttype, data=producttype_data) 
        if producttypes_serializer.is_valid(): 
            producttypes_serializer.save() 
            return JsonResponse(producttypes_serializer.data) 
        return JsonResponse(producttypes_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        producttype.delete() 
        return JsonResponse({'message': 'Product Type was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def ecommerce_detail(request, pk):
    ecommerces = Ecommerce.objects.get(pk=pk)
 
    if request.method == 'GET': 
        ecommerces_serializer = EcommerceSerializer(ecommerces) 
        return JsonResponse(ecommerces_serializer.data) 
    elif request.method == 'PUT': 
        ecommerce_data = JSONParser().parse(request) 
        ecommerces_serializer = EcommerceSerializer(ecommerces, data=ecommerce_data) 
        if ecommerces_serializer.is_valid(): 
            ecommerces_serializer.save()
            return JsonResponse(ecommerces_serializer.data) 
        return JsonResponse(ecommerces_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        ecommerces.delete() 
        return JsonResponse({'message': 'Product Type was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    products = Product.objects.get(pk=pk)
 
    if request.method == 'GET': 
        product_serializer = ProductSerializer(products) 
        return JsonResponse(product_serializer.data) 
    elif request.method == 'PUT': 
        product_data = JSONParser().parse(request) 
        product_serializer = ProductSerializer(products, data=product_data) 
        if product_serializer.is_valid(): 
            product_serializer.save()
            return JsonResponse(product_serializer.data) 
        return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        Product.delete() 
        return JsonResponse({'message': 'Product Type was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def producttype_list_active(request):
    productTypes = ProductType.objects.filter(status=True)
        
    if request.method == 'GET': 
        producttypes_serializer = ProductTypeSerializer(productTypes, many=True)
        return JsonResponse(producttypes_serializer.data, safe=False)

@api_view(['GET'])
def ecommerce_list_active(request):
    ecommerces = Ecommerce.objects.filter(status=True)
        
    if request.method == 'GET': 
        ecommerce_serializer = EcommerceSerializer(ecommerces, many=True)
        return JsonResponse(ecommerce_serializer.data, safe=False)

@api_view(['GET'])
def product_list_active(request):
    products = Product.objects.filter(status=True)
        
    if request.method == 'GET': 
        products_serializer = ProductSerializer(products, many=True)
        return JsonResponse(products_serializer.data, safe=False)
