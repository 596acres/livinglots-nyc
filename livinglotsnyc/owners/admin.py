from django.contrib import admin

from livinglots_owners.admin import BaseOwnerAdmin, BaseOwnerContactAdmin

from .models import Owner, OwnerContact


class OwnerAdmin(BaseOwnerAdmin):
    pass


class OwnerContactAdmin(BaseOwnerContactAdmin):
    pass


admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerContact, OwnerContactAdmin)
