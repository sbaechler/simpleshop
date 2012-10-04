""" A very basic shop for FeinCMS that can be included as application content.
    It's currently only single-page for <20 items.
    Powered by Plata.
    Requires django-orderable: https://github.com/tkaemming/django-orderable
    Plata and FeinCMS.

    The admin is notificated via email. Therefore set those settings:

    PLATA_NOTIFICATION_EMAIL_ALWAYS = ['shopadmin@example.com']
    PLATA_NOTIFICATION_EMAIL_SHIPPING = ['warehouse@example.com']

"""
VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))