from livinglots_owners.models import BaseOwner, BaseOwnerContact


class Owner(BaseOwner):

    class Meta:
        ordering = ['owner_type', 'name',]


class OwnerContact(BaseOwnerContact):
    pass
