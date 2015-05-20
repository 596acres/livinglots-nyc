from django.contrib import admin
from django.forms import ModelForm, SelectMultiple


import autocomplete_light
from easy_select2 import apply_select2

from livinglots_owners.admin import (BaseOwnerAdmin, BaseOwnerContactAdmin,
                                     BaseOwnerGroupAdmin)

from .models import Owner, OwnerContact, OwnerGroup


class OwnerAdmin(BaseOwnerAdmin):
    # NB: setting fields = '__all__', less concerned about security since we 
    # are in the admin site
    form = autocomplete_light.modelform_factory(Owner, fields='__all__')


class OwnerContactAdmin(BaseOwnerContactAdmin):
    pass


class OwnerGroupAdminForm(ModelForm):
    class Meta:
        fields = ['name', 'owner_type', 'owners',]
        widgets = {
            'owners': apply_select2(SelectMultiple),
        }


class OwnerGroupAdmin(BaseOwnerGroupAdmin):
    form = OwnerGroupAdminForm


admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerContact, OwnerContactAdmin)
admin.site.register(OwnerGroup, OwnerGroupAdmin)
