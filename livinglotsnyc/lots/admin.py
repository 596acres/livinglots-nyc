from django.contrib import admin

from livinglots_lots.admin import BaseLotAdmin

from .models import Lot


class LotAdmin(BaseLotAdmin):
    fieldsets = (
            ('NYC specific', {
                'fields': ('bbl',
                           ('borough', 'block', 'lot_number',)),
            }),
        ) + BaseLotAdmin.fieldsets + (
            ('Ownership', {
                'fields': ('owner',),
            }),
        )
    list_display = ('bbl', 'address_line1', 'borough', 'known_use')
    search_fields = ('bbl', 'address_line1', 'name',)


admin.site.unregister(Lot)
admin.site.register(Lot, LotAdmin)
