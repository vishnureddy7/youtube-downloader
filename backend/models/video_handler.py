from flask import Blueprint, request, jsonify
from log import get_logger
from youtube_dl import YoutubeDL

from util.resp_util import get_success_response

logger = get_logger(__name__)

ydl = YoutubeDL()

video_blueprint = Blueprint("video", __name__)


@video_blueprint.route("/get_video_details", methods=["GET"])
def get_video_details():
    """
    Get Video details for the given url
    :return: json
    """
    req_json = request.json
    url = req_json['url']
    response = get_youtube_video_details(url)
    return jsonify(get_success_response(data=response))


def get_youtube_video_details(url):
    """
    Get Youtube video details for given url
    :param url: str
    :return: dict
    """
    logger.debug("entering function get_youtube_video_details")
    result = ydl.extract_info(url, download=False)
    all_details = {
        "id": result["id"],
        "title": result["title"],
        "description": result["description"],
        "duration": result["duration"],
        "width": result["width"],
        "height": result["height"],
        "formats": get_youtube_valid_formats(result["formats"])
    }
    logger.debug("exiting function get_youtube_video_details")
    return all_details


def get_youtube_valid_formats(all_formats):
    """
    Get Youtube valid formats from list of all formats
    :param all_formats: list
    :return: list
    """
    logger.debug("entering function get_youtube_valid_formats")
    valid_formats = []
    for format_i in all_formats:
        if is_valid_youtube_format(format_i):
            valid_formats.append(get_limited_details(format_i))
    logger.debug("exiting function get_youtube_valid_formats")
    return valid_formats


def is_valid_youtube_format(format_i):
    """
    check if the given format is valid or not
    :param format_i: dict
    :return: boolean
    """
    return "acodec" in format_i


def get_limited_details(format_i):
    """
    Get only necessary details from youtube-dl video/audio format
    :param format_i: dict
    :return: dict
    """
    return {
        "format": format_i["format_note"],
        "ext": format_i["ext"],
        "width": format_i["width"],
        "height": format_i["height"],
        "url": format_i["url"],
        "filesize": format_i["filesize"]
    }
