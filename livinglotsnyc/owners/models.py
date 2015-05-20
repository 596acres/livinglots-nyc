from livinglots_owners.models import BaseOwner, BaseOwnerContact, BaseOwnerGroup


class Owner(BaseOwner):

    class Meta:
        ordering = ['owner_type', 'name',]


class OwnerContact(BaseOwnerContact):

    class Meta:
        ordering = ['name',]


class OwnerGroup(BaseOwnerGroup):
    pass
