# unicoding: utf-8
from flask import *

bp = Blueprint("index", __name__, url_prefix="/index")


@bp.route("/")
def hello():
    return "Hello, World!"
