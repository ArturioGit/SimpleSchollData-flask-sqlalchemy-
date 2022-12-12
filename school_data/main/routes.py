from flask import Blueprint, url_for, render_template
from school_data.utils import url_history_util

main = Blueprint('main', __name__)


@main.after_request
def save_response(response):
    return url_history_util.save_response(response)


@main.route('/')
@main.route('/main')
def about():
    return render_template('main.html')
