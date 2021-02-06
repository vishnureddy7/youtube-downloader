from log import get_logger
from models.error_handler import CustomException

logger = get_logger(__name__)


class ValidationException(CustomException):
    """
    This class is used for Validation Exceptions
    """

    def __init__(self, message):
        """
        :param message: str
        """
        super().__init__(message, status_code=400)


def validate_fields(req_data, fields, content_type="json"):
    """
    validates if given request data has all fields or not
    :param req_data: dict
    :param fields: list
    :param content_type: str
    :return: None || Exception
    """
    logger.info("entering function validate_fields")
    if req_data is None:
        raise ValidationException(f"excepting {content_type}")
    for field in fields:
        if field not in req_data:
            raise ValidationException(f"{field} is missing in request")
    logger.info("exiting function validate_fields")
