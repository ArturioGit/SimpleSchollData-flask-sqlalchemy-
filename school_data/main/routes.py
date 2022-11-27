from flask import Blueprint, url_for, render_template

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/main')
def about():
    return render_template('main.html')