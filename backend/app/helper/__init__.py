from flask import Blueprint

helper = Blueprint(
    "helper",
    __name__,
    url_prefix="/helper",
)

from . import routes