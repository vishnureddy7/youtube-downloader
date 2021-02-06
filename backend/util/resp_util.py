from log import get_logger

logger = get_logger(__name__)


def get_success_response(message=None, data=None):
    """
    Returns dict with success status with given message and data in it
    :param message: str
    :param data: any
    :return: dict
    """
    return get_response("success", message, data)


def get_failure_response(message=None, data=None):
    """
    Returns dict with failure status with given message and data in it
    :param message: str
    :param data: any
    :return: dict
    """
    return get_response("failure", message, data)


def get_error_response(message=None, data=None):
    """
    Returns dict with error status with given message and data in it
    :param message: str
    :param data: any
    :return: dict
    """
    return get_response("error", message, data)


def get_response(status, message=None, data=None):
    """
    Returns dict with given status
    :param status: str
    :param message: str
    :param data: any
    :return: dict
    """
    logger.debug("entering function get_response")
    response = {
        "status": status
    }
    if message is not None:
        response["message"] = message
    if data is not None:
        response["data"] = data
    logger.debug("exiting function get_response")
    return response
