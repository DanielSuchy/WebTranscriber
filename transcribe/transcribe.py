from flask import (
  Blueprint, render_template, request
)

bp = Blueprint('transcribe', __name__, url_prefix='/transcribe')

@bp.route('/', methods=('GET', 'POST'))
def presenters():
  source_text = "vložte text pro transkripci do IPA"
  target_text = "zde se zobrazí přeložený text"
  if request.method == 'POST':
      source_text = request.form['source_text']
      target_text = source_text

  return render_template('transcribe/transcribe.html',
                          source_text = source_text,
                          target_text = target_text
                        )
