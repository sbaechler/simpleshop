from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.content.application import models as app_models

from plata.product.models import ProductBase
from plata.shop.models import PriceBase
from orderable.models import OrderableModel
from plata.shop.models import Order as OrderBase

from plata.shop import signals as shop_signals
from feincms.content.application.models import app_reverse

from .handlers import EmailHandler

# Signal handlers
#shop_signals.contact_created.connect(
#    notifications.ContactCreatedHandler(),
#    weak=False)
shop_signals.order_paid.connect(
    EmailHandler(),
    weak=False)



SALUTATION_CHOICES = (('m', _('Mr')),
                      ('f', _('Ms')),
)

class Order(OrderBase):
    billing_salutation = models.CharField(_('salutation'), max_length=1,
                  choices=SALUTATION_CHOICES, default=SALUTATION_CHOICES[0][0])
    shipping_salutation = models.CharField(_('salutation'), max_length=1, blank=True)


class Product(ProductBase, PriceBase, OrderableModel):
    """
    This product model is a price too, which means that only one price
    can exist. The administration interface is even simpler when following
    this approach.
    """

    is_active = models.BooleanField(_('is active'), default=True)
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    short_description = models.TextField(_('intro description'))
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), blank=True, null=True,
                              upload_to='shop_images')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __unicode__(self):
        return self.name

    @app_models.permalink
    def get_absolute_url(self):
        return ('plata_product_detail', 'simpleshop.urls',
                (), {'object_id': self.pk})

    def get_list_url(self):
        return u'%s#%s' % (
            app_reverse('plata_product_list', 'simpleshop.urls' ),
            self.slug)

    def get_price(self, *args, **kwargs):
        return self

    def price_display(self):
        return u'Fr. %.2f' % self.unit_price

    def handle_order_item(self, orderitem):
        ProductBase.handle_order_item(self, orderitem)
        PriceBase.handle_order_item(self, orderitem)



class Contact(models.Model):
    ADDRESS_FIELDS = ['salutation', 'first_name', 'last_name', 'address',
        'zip_code', 'city']

    user = models.OneToOneField(User, verbose_name=_('user'),
        related_name='contactuser')

    salutation = models.CharField(_('salutation'), max_length=1,
                  choices=SALUTATION_CHOICES, default=SALUTATION_CHOICES[0][0])
    company = models.CharField(_('company'), max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    address = models.TextField(_('address'))
    zip_code = models.CharField(_('ZIP code'), max_length=50)
    city = models.CharField(_('city'), max_length=100)
    notes = models.TextField(_('notes'), blank=True)
    created = models.DateTimeField(_('created'), default=datetime.now)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __unicode__(self):
        return unicode(self.user)

    def update_from_order(self, order, request=None):
        for field in self.ADDRESS_FIELDS:
            f = 'billing_' + field
            setattr(self, field, getattr(order, f))