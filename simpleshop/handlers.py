"""
    Add this to your settings:
    PLATA_NOTIFICATION_EMAIL_ALWAYS = ['shopadmin@example.com']
    PLATA_NOTIFICATION_EMAIL_SHIPPING = ['warehouse@example.com']

"""
from django.utils.translation import activate
from plata.shop import notifications
from django.conf import settings

class EmailHandler(notifications.BaseHandler):
    ALWAYS = getattr(settings, 'PLATA_NOTIFICATION_EMAIL_ALWAYS', [])
    SHIPPING = getattr(settings, 'PLATA_NOTIFICATION_EMAIL_SHIPPING', [])

    def __call__(self, sender, order, **kwargs):
        cash_on_delivery = False
        try:
            if order.payments.all()[0].payment_module_key == 'cod':
                cash_on_delivery = True
        except:
            pass

        if order.language_code:
            activate(order.language_code)

        invoice_message = self.create_email_message('plata/notifications/order_paid.txt',
            order=order,
            **kwargs)
        invoice_message.attach(order.order_id + '.pdf', self.invoice_pdf(order), 'application/pdf')
        invoice_message.to.append(order.email)
        invoice_message.bcc.extend(self.ALWAYS)

        packing_slip_message = self.create_email_message('plata/notifications/packing_slip.txt',
            order=order,
            **kwargs)
        packing_slip_message.attach(
            order.order_id + '-LS.pdf',
            self.packing_slip_pdf(order),
            'application/pdf')
        packing_slip_message.to.extend(self.ALWAYS)

        if cash_on_delivery:
            invoice_message.bcc.extend(self.SHIPPING)
        else:
            packing_slip_message.to.extend(self.SHIPPING)

        invoice_message.send()
        packing_slip_message.send()

