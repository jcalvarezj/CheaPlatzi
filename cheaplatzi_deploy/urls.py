from django.conf.urls import url 
from cheaplatzi_deploy import views 
 
urlpatterns = [ 
    url(r'^api/product_types$', views.producttype_list),
    url(r'^api/product_types/(?P<pk>[0-9]+)$', views.producttype_detail),
    url(r'^api/product_types/active$', views.producttype_list_active),
    url(r'^api/ecommerce$', views.ecommerce_list),
    url(r'^api/ecommerce/(?P<pk>[0-9]+)$', views.ecommerce_detail),
    url(r'^api/ecommerce/active$', views.ecommerce_list_active),
    url(r'^api/product$', views.product_list),
    url(r'^api/product/(?P<pk>[0-9]+)$', views.product_detail),
    url(r'^api/product/active$', views.product_list_active),
]