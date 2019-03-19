from flask import (
  Blueprint, render_template, request
)

bp = Blueprint('transcribe', __name__, url_prefix='/transcribe')

@bp.route('/', methods=('GET', 'POST'))
def presenters():
  return render_template('transcribe/transcribe.html')
