from flask import Blueprint, jsonify
from log import get_logger
from util.resp_util import get_error_response

logger = get_logger(__name__)


class CustomException(Exception):
    """
    This class is used for CustomExceptions thrown from APIs
    """

    def __init__(self, message, status_code=500):
        """
        :param message: str
        error message to reply to api request
        :param status_code: int
        status code to reply to api request
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code


error_blueprint = Blueprint("errors", __name__)


@error_blueprint.app_errorhandler(CustomException)
def handle_error(error):
    """
    :param error: CustomException
    :return: json
    """
    logger.debug("entering function handle_error")
    if error.status_code == 500:
        # print stacktrace for internal server errors
        logger.exception("internal server error %s", error)
    else:
        logger.error("custom error message= %s", error.message)
    response = get_error_response(error.message)
    logger.debug("exiting function handle_error")
    return jsonify(response), error.status_code
