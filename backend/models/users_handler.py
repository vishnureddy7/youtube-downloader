import time
import config
from uuid import uuid4
from flask import Blueprint, jsonify, request
from flask_login import UserMixin, login_user, current_user
from flask_login import logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from database.query_util import *
from util.cache import local_user_cache
from util.resp_util import *
from util.validation_util import *
from config.messages import *

logger = get_logger(__name__)


class User(UserMixin):
    """
    UserMixin Object for Flask-Login Application
    """

    def __init__(self, userid, email):
        self.id = userid
        self.email = email

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


users_blueprint = Blueprint("user_handler", __name__)

login_manager = LoginManager()


@users_blueprint.record_once
def on_load(state):
    login_manager.init_app(state.app)


login_manager.login_view = "user_handler.login_to_access"


@users_blueprint.route("/login_to_access")
def login_to_access():
    return jsonify(get_error_response(NOT_AUTHORIZED_FOR_THIS_API))


@login_manager.user_loader
def load_user(user_id):
    return load_user_object(user_id)


def load_user_object(user_id):
    """
    Load user object from mongo database
    :param user_id: str
    :return: User Object
    """
    logger.debug("entering function load_user_object")

    if user_id in local_user_cache:
        time_diff = time.time() - local_user_cache[user_id]["prev_time"]
        if time_diff < config.USER_CACHE_TIME:
            logger.info("got user object from local cache for user id %s", user_id)
            return local_user_cache[user_id]["obj"]

    find_query = {"user_id": user_id}
    project_query = {"_id": 0, "user_id": 1, "email": 1}
    result = run_find_one_query(config.USERS_COL, find_query, project_query, error=False)
    if result is not None:
        logger.info("loaded the user obj for user id = %s from db", user_id)
        user_obj = User(user_id, result["email"])
        local_user_cache[user_id] = {"prev_time": time.time(), "obj": user_obj}
        result = user_obj

    logger.debug("exiting function load_user_object")
    return result


@users_blueprint.route("/register", methods=["POST"])
def register_post():
    """
    Register a new user
    :return: json
    """
    logger.info("entering function register_post")
    response = register_user(request.json)
    logger.info("exiting function register_post")
    return jsonify(response)


def register_user(req_data):
    """
    Register New User
    1. Check for given fields
    2. Check if email already exists
    3. Check if mobile already exists
    4. Insert New record to Database
    :param req_data: dict
    :return: dict
    """
    logger.debug("entering function register_user")
    validate_fields(req_data, ["email", "mobile", "password", "first_name", "last_name"])

    user_email = req_data["email"]
    user_mobile = req_data["mobile"]
    user_password = req_data["password"]
    user_first_name = req_data["first_name"]
    user_last_name = req_data["last_name"]

    existing_email_query = {"email": user_email}
    result = run_find_one_query(config.USERS_COL, existing_email_query, error=False)
    if result is not None:
        logger.error("email already exists, query result = %s", result)
        return get_failure_response(EMAIL_EXISTS_ERR_MSG)

    existing_mobile_query = {"mobile": user_mobile}
    result = run_find_one_query(config.USERS_COL, existing_mobile_query, error=False)
    if result is not None:
        logger.error("mobile already exists, query result = %s", result)
        return get_failure_response(MOBILE_EXISTS_ERR_MSG)

    user_id = uuid4().hex
    doc = {
        "user_id": user_id,
        "first_name": user_first_name,
        "last_name": user_last_name,
        "email": user_email,
        "mobile": user_mobile,
        "password": generate_password_hash(user_password)
    }
    logger.info("inserting new user into database")
    run_insert_one_query(config.USERS_COL, doc, error=True, error_msg=REGISTRATION_FAILED_ERR_MSG)
    logger.info("registration successful for email = %s", doc["email"])

    logger.debug("exiting function register_user")
    return get_success_response(REGISTRATION_SUCCESS_MSG)


@users_blueprint.route("/login", methods=["POST"])
def login_post():
    """
    Login API to check given user credentials
    :return: json
    """
    logger.debug("entering function login_post")
    response = check_user_credentials(request.json)
    logger.debug("exiting function login_post")
    return jsonify(response)


def check_user_credentials(req_data):
    """
    Validate given user credentials and login the user
    :param req_data: dict
    :return: dict
    """
    logger.debug("entering function check_user_credentials")
    validate_fields(req_data, ["email", "password"])

    find_query = {"email": req_data["email"]}
    project_query = {"_id": 0, "password": 1, "user_id": 1}
    result = run_find_one_query(config.USERS_COL, find_query, project_query, error=True,
                                error_msg=USER_NOT_EXIST_ERR_MSG)

    if not check_password_hash(result["password"], req_data["password"]):
        raise CustomException(WRONG_CREDENTIALS_ERR_MSG, 401)

    is_remember = True if "remember" in req_data and req_data["remember"] else False
    login_user(User(result["user_id"], req_data["email"]), remember=is_remember)
    logger.info("user login successful for %s", req_data["user_id"])

    logger.debug("exiting function check_user_credentials")
    return get_success_response(LOGIN_SUCCESS_MSG)


@users_blueprint.route("/get_profile", methods=["GET"])
@login_required
def get_profile():
    """
    Get current user profile
    :return: json
    """
    logger.debug("entering function get_profile")
    response = read_user_profile()
    logger.debug("exiting function get_profile")
    return jsonify(response)


def read_user_profile():
    """
    Get current user profile from database
    :return: dict
    """
    logger.debug("entering function read_profile")
    find_query = {"user_id": current_user.id}
    project_query = {"_id": 0, "user_id": 0, "password": 0}
    result = run_find_one_query(config.USERS_COL, find_query, project_query, error=True,
                                error_msg=NO_USER_ERR_MSG)
    logger.info("fetched user profile for %s", current_user.id)
    response = get_success_response(data=result)
    logger.debug("exiting function read_profile")
    return response


@users_blueprint.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    """
    Update current logged in user profile
    :return: json
    """
    logger.debug("entering function update_profile")
    response = update_user_profile(request.json)
    logger.debug("exiting function update_profile")
    return jsonify(response)


def update_user_profile(req_data):
    """
    Update the current logged in user profile to database
    :param req_data: dict
    :return: dict
    """
    logger.debug("entering function update_user_profile")

    update_fields = {}
    for field in req_data:
        update_fields[field] = req_data[field]
    if "password" in req_data:
        update_fields["password"] = generate_password_hash(req_data["password"])

    find_query = {"user_id": current_user.id}
    update_query = {"$set": update_fields}
    run_update_one_query(config.USERS_COL, find_query, update_query,
                         error=True, error_msg=PROFILE_UPDATE_FAILED_ERR_MSG)
    logger.info("Profile update success for %s", current_user.id)

    logger.debug("exiting function update_user_profile")
    return get_success_response(PROFILE_UPDATE_SUCCESS_MSG)


@users_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Logout user API
    :return: json
    """
    logger.debug("entering function logout")
    logout_user()
    logger.debug("exiting function logout")
    return jsonify(get_success_response(LOGOUT_SUCCESS_MSG))
