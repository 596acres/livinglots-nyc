import logging

from django.conf import settings

import mailchimp
from mailchimp.chimpy.chimpy import ChimpyException


def subscribe(email, full_name=None, first_name=None, last_name=None,
              is_participating=False, **kwargs):
    """Subscribe the given email to the mailing list."""
    merge_dict = {
        'EMAIL': email,
    }

    if is_participating:
        merge_dict['GROUPINGS'] = [settings.MAILCHIMP_PARTCICIPATION_GROUP,]

    if full_name:
        try:
            first_name, last_name = full_name.split()
        except Exception:
            first_name = full_name
    if first_name:
        merge_dict['FNAME'] = first_name
    if last_name:
        merge_dict['LNAME'] = last_name

    if settings.DEBUG:
        logging.debug('Would be subscribing %s to the mailing list with '
                      'merge_dict %s' % (email, merge_dict,))
        return

    try:
        mailchimp.utils.get_connection() \
                .get_list_by_id(settings.MAILCHIMP_LIST_ID) \
                .subscribe(email, merge_dict)
    except ChimpyException:
        # Thrown if user already subscribed--ignore
        return


def subscribe_obj(obj, **kwargs):
    """
    Subscribe an object representing a person to the mailing list.  Assumes 
    there will be an email attribute on the object.
    """
    if not obj or not obj.email:
        return

    if not kwargs:
        kwargs = {}

    if obj.name:
        kwargs['full_name'] = obj.name
    subscribe(obj.email, **kwargs)
