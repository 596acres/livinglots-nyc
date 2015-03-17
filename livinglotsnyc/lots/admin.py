from django import forms
from django.contrib import admin

from autocomplete_light import ChoiceWidget

from livinglots_forms.widgets import AddAnotherWidgetWrapper
from livinglots_lots.admin import BaseLotAdmin

from owners.models import Owner
from .models import Lot


class LotAdminForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=Owner.objects.all().order_by('name'),
        widget=AddAnotherWidgetWrapper(ChoiceWidget('OwnerAutocomplete'), Owner)
    )

    class Meta:
        model = Lot


class LotAdmin(BaseLotAdmin):
    form = LotAdminForm
    fieldsets = (
            ('NYC specific', {
                'fields': ('bbl',
                           ('borough', 'block', 'lot_number',)),
            }),
        ) + BaseLotAdmin.fieldsets + (
            ('Ownership', {
                'fields': (('owner', 'owner_contact',), 'owner_opt_in',),
            }),
            ('Gutterspace', {
                'fields': ('gutterspace',),
            }),
        )
    list_display = ('pk', 'bbl', 'address_line1', 'borough', 'known_use')
    search_fields = ('bbl', 'address_line1', 'name',)


admin.site.unregister(Lot)
admin.site.register(Lot, LotAdmin)
