class ParcelAlreadyInLot(Exception):
    """
    An attempt was made to add a parcel to a lot but the parcel is already
    part of a lot.
    """
    pass
