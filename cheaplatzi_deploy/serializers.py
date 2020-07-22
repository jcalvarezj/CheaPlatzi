from rest_framework import serializers 
from cheaplatzi_deploy.models import ProductType, Ecommerce, Product
 
 
class ProductTypeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = ProductType
        fields = ('id',
                  'name',
                  'description',
                  'status',
                  'created_at',
                  'updated_at')


class EcommerceSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Ecommerce
        fields = ('id',
                  'name',
                  'description',
                  'url',
                  'image',
                  'country',
                  'status',
                  'created_at',
                  'updated_at')

class ProductSerializer(serializers.ModelSerializer):
    # id_ecommerce = EcommerceSerializer(many=False,read_only=True)
 
    class Meta:
        model = Product
        fields = ('id',
                  'id_type_product',
                  'id_ecommerce',
                  'name',
                  'description',
                  'price',
                  'image',
                  'image',
                  'url',
                  'barcode',
                  'status',
                  'created_at',
                  'updated_at')
    