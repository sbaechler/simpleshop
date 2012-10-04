from django.conf.urls.defaults import include, patterns, url
from django.shortcuts import redirect
from .views import product_detail, product_list, shop

urlpatterns = patterns('',
    url(r'^shop/', include(shop.urls)),
    url(r'^products/$', product_list, name='plata_product_list'),
    url(r'^products/(?P<object_id>\d+)/$', product_detail,
                                        name='plata_product_detail'),
    url(r'^$', lambda request: redirect('products/')),
    url(r'^reporting/', include('plata.reporting.urls')),
)
