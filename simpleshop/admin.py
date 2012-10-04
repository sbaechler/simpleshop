from orderable.admin import OrderableAdmin
from django.contrib import admin
from django import forms
from feincms.templatetags.feincms_thumbnail import thumbnail
from django.conf import settings

from . import models

class ProductAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'description': forms.widgets.Textarea(attrs={'class':'tinymce'}),
            'short_description': forms.widgets.Textarea(attrs={'class':'tinymce'}),
        }


class ProductAdmin(OrderableAdmin):
    def thumb(self, obj):
        try:
            return u'<img src="%s" >' % thumbnail(obj.image, '200x60')
        except ValueError:
            return u'No Image'
    thumb.allow_tags = True

    form = ProductAdminForm

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js',
              settings.FEINCMS_RICHTEXT_INIT_CONTEXT['TINYMCE_JS_URL'],
              'tinymce_admin/init.js',
            )

    list_display = ('thumb', 'is_active', 'name')
    list_display_links = ('name',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

admin.site.register(models.Product, ProductAdmin)
