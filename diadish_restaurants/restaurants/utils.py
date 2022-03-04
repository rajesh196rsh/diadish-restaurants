import logging

logger = logging.getLogger(__name__)


def get_ip_address(request):
    """
    Analyse request data and returns the ip address of user

    param: 
        request: copy of request data from user
    return:
        ip_address: ip address of user
    """
    ip_address = ''
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        logger.debug("x_forwarded_for {}".format(x_forwarded_for))
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    except Exception as e:
        logger.debug(e)
    logger.debug("returning ip address {}".format(ip_address))
    return ip_address

