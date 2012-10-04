from plata.payment.modules import cod
from django.shortcuts import redirect
from feincms.content.application.models import app_reverse

class CodPaymentProcessor(cod.PaymentProcessor):
    def redirect(self, url_name):
        return redirect(app_reverse(url_name,
                                    'simpleshop.urls'))