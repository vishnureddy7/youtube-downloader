from database import mongo_client
from log import get_logger
from models.error_handler import CustomException
from config.messages import *

logger = get_logger(__name__)


def run_find_one_query(collection, query, projection=None, error=False,
                       error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs find one query on mongo database collection
    :param collection: str
    :param query: dict
    :param projection: dict
    :param error: bool
    :param error_msg: str
    :return: dict || None
    """
    logger.debug("entering function run_find_one_query")
    if projection is None:
        projection = dict()
    document = mongo_client.db[collection].find_one(query, projection)
    if document is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_find_one_query")
    return document


def run_find_many_query(collection, query, projection=None, limit=10, error=False,
                        error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs find many query on mongo database collection
    :param collection: str
    :param query: dict
    :param projection: dict
    :param limit: int
    :param error: bool
    :param error_msg: str
    :return: mongo cursor
    """
    logger.debug("entering function run_find_many_query")
    if projection is None:
        projection = dict()
    cursor = mongo_client.db[collection].find(query, projection)
    if cursor is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_find_many_query")
    return cursor if cursor is None else cursor.limit(limit)


def run_insert_one_query(collection, document, error=False,
                         error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs insert one query on mongo database collection
    :param collection: str
    :param document: dict
    :param error: boolean
    :param error_msg: str
    :return: ObjectId
    """
    logger.debug("entering function run_insert_one_query")
    response = mongo_client.db[collection].insert_one(document)
    if response is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_insert_one_query")
    return 0 if response is None else 1


def run_insert_many_query(collection, documents, error=False,
                          error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs insert many query on mongo database collection
    :param collection: str
    :param documents: list
    :param error: bool
    :param error_msg: str
    :return: list
    """
    logger.debug("entering function run_insert_many_query")
    resp = mongo_client.db[collection].insert_many(documents)
    if resp is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_insert_many_query")
    return 0 if resp is None else len(resp.inserted_ids)


def run_update_one_query(collection, filter_query, update_query, error=False,
                         error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs update one query on mongo database collection
    :param collection: str
    :param filter_query: dict
    :param update_query: dict
    :param error: bool
    :param error_msg: str
    :return: tuple
    """
    logger.debug("entering function run_update_one_query")
    resp = mongo_client.db[collection].update_one(filter_query, update_query)
    if resp is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_update_one_query")
    return (0, 0) if resp is None else resp.matched_count, resp.modified_count


def run_update_many_query(collection, filter_query, update_query, error=False,
                          error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs update many query on mongo database collection
    :param collection: str
    :param filter_query: dict
    :param update_query: dict
    :param error: bool
    :param error_msg: str
    :return: tuple
    """
    logger.debug("entering function run_update_many_query")
    resp = mongo_client.db[collection].update_many(filter_query, update_query)
    if resp is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_update_many_query")
    return (0, 0) if resp is None else resp.matched_count, resp.modified_count


def run_delete_one_query(collection, query, error=False,
                         error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs delete one query on mongo database collection
    :param collection: str
    :param query: dict
    :param error: bool
    :param error_msg: str
    :return: int
    """
    logger.debug("entering function run_delete_one_query")
    resp = mongo_client.db[collection].delete_one(query)
    if resp is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_delete_one_query")
    return 0 if resp is None else resp.deleted_count


def run_delete_many_query(collection, query, error=False,
                          error_msg=SOMETHING_WENT_WRONG_ERR_MSG):
    """
    Runs delete many query on mongo database collection
    :param collection: str
    :param query: dict
    :param error: bool
    :param error_msg: str
    :return: int
    """
    logger.debug("entering function run_delete_many_query")
    resp = mongo_client.db[collection].delete_many(query)
    if resp is None and error:
        raise CustomException(error_msg)
    logger.debug("exiting function run_delete_many_query")
    return 0 if resp is None else resp.deleted_count
