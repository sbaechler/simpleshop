import plata
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import FeinCMSInline
from django import forms

class ProductInline(FeinCMSInline):
    raw_id_fields = ('product',)

class SingleProductTeaserContent(models.Model):
    product = models.ForeignKey(plata.product_model())

    feincms_item_editor_inline = ProductInline

    class Meta:
        abstract = True
        verbose_name = _('Product teaser')
        verbose_name_plural = _('Product teasers')

    @property
    def media(self):
        media = forms.Media()
        media.add_js(('plata/cart.js',))
        return media


    def __unicode__(self):
        return unicode(self.product)

    def render(self, **kwargs):
        request = kwargs.get('request')  # need request for csrf token
        return render_to_string('content/product/single_teaser.html',
                                { 'product': self.product },
                                context_instance=RequestContext(request))