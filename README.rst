Simple Shop
===========

A very basic shop for FeinCMS_ that can be included as application content.
It's currently only single-page and recommended for shops with less than 20 items.
It's powered by Plata_.

Requirements:

* `django-orderable <https://github.com/tkaemming/django-orderable>`_,
* pdfdocument
* reportlab
* FeinCMS_
* Plata_

.. _FeinCMS: https://github.com/matthiask/feincms
.. _Plata: https://github.com/sbaechler/plata


Settings
--------

The site operator is notificated via email. Therefore set those settings::

    PLATA_NOTIFICATION_EMAIL_ALWAYS = ['shopadmin@example.com']
    PLATA_NOTIFICATION_EMAIL_SHIPPING = ['warehouse@example.com']


Here is an example settings code for the simple shop::

    PLATA_PRICE_INCLUDES_TAX = True

    PLATA_REPORTING_ADDRESSLINE = u'My great shop'

    PLATA_REPORTING_STATIONERY = 'mysite.stationery.ShopStationery'

    PLATA_PAYMENT_MODULES = [
        'simpleshop.payment_modules.CodPaymentProcessor',
    ]

    PLATA_ORDER_PROCESSORS = [
        'plata.shop.processors.InitializeOrderProcessor',
        'plata.shop.processors.DiscountProcessor',
        'plata.shop.processors.TaxProcessor',
        'plata.shop.processors.MeansOfPaymentDiscountProcessor',
        'plata.shop.processors.ItemSummationProcessor',
        #'plata.shop.processors.ZeroShippingProcessor',
        'plata.shop.processors.OrderSummationProcessor',
        ]

    # PLATA_SHIPPING_FIXEDAMOUNT = {'cost': Decimal('8.0'), 'tax': Decimal('8.0')}

    PLATA_SHOP_PRODUCT = 'simpleshop.Product'
    CURRENCIES = ('CHF',)


Stationery
----------

It's recommended that you create your own stationery.
Just copy the default stationery class ``ExampleStationery`` from
``venv/lib/site-packages/pdfdocument/elements.py``
to a ``stationery`` module in your project folder.


Email
-----

The email templates are in ``templates/plata/notifications``.
The first line in the template is the email subject. It has to be followed
by an empty line.
You can use django template language for the email templates. But no HTML.
