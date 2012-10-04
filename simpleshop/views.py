from plata.shop.models import OrderItem
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.forms.formsets import formset_factory
from django.views.decorators.http import require_POST
from feincms.content.application.models import app_reverse

import simplejson as json

import plata
from plata.discount.models import Discount

from plata.shop import forms as shop_forms
from plata.shop.views import Shop

from .models import Contact, Product, Order

class CheckoutForm(shop_forms.BaseCheckoutForm):
    class Meta:
        fields = ['email', 'notes'] + ['billing_%s' % f for f in Contact.ADDRESS_FIELDS]
        model = Order
        widgets = {
            'billing_address': forms.Textarea(attrs={'rows': '2'}),
            'notes': forms.Textarea(attrs={'rows': '4'})
        }

    def __init__(self, *args, **kwargs):
        shop = kwargs.get('shop')
        request = kwargs.get('request')
        contact = shop.contact_from_user(request.user)

        if contact:
            initial = {}
            for f in contact.ADDRESS_FIELDS:
                initial['billing_%s' % f] = getattr(contact, f)
                kwargs['initial'] = initial
            initial['email'] = contact.user.email

        super(CheckoutForm, self).__init__(*args, **kwargs)

        if not contact:
            self.fields['create_account'] = forms.BooleanField(
                label=_('create account'),
                required=False, initial=True)


class CustomShop(Shop):

    def checkout_form(self, request, order):
        return CheckoutForm

    def get_context(self, request, context, **kwargs):
        """
        Helper method returning a context dict. Override this if you
        need additional context variables.
        """
        ctx = {
            'base_template': self.base_template,
            'price_includes_tax': plata.settings.PLATA_PRICE_INCLUDES_TAX,
            }
        ctx.update(context)
        ctx.update(kwargs)
        return ctx

    def render(self, request, template, context):
        """ render for application content """
        return template, context

    def redirect(self, url_name):
        return redirect(app_reverse(url_name,
                                    'simpleshop.urls'))

    base_template = 'site_base.html'

shop = CustomShop(Contact, Order, Discount)

def product_list(request):
    """ We don't need no pagination """
    return 'product/product_list.html', \
           {'object_list': Product.objects.filter(is_active=True) }


class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(label=_('quantity'), initial=0,
        min_value=0, max_value=100)


@require_POST
def product_detail(request, object_id):
    product = get_object_or_404(Product.objects.filter(is_active=True), pk=object_id)

    if request.method == 'POST':
        form = OrderItemForm(request.POST)

        if form.is_valid():
            order = shop.order_from_request(request, create=True)
            try:
                order.modify_item(product, form.cleaned_data.get('quantity'))
                messages.success(request, _('The cart has been updated.'))
            except ValidationError, e:
                if e.code == 'order_sealed':
                    [messages.error(request, msg) for msg in e.messages]
                else:
                    raise

            return HttpResponse('ok')
        else:
            return HttpResponse(json.dumps(form.errors),
                                mimetype='application/json')
