from flask import Blueprint, render_template

bp = Blueprint(
    'hello',
    __name__,
    template_folder='../templates'
)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route("/hello")
def hello():
    return "Hello, World!"
