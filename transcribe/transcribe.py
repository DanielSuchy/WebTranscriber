from flask import (
  Blueprint, render_template, request
)
from .Transcriber import Transcriber

bp = Blueprint('transcribe', __name__, url_prefix='/transcribe')

@bp.route('/', methods=('GET', 'POST'))
def presenters():
  source_text = "vložte větu pro transkripci do IPA"
  target_text = "zde se zobrazí překlad"
  if request.method == 'POST':
      source_text = request.form['source_text']
      target_text = get_transcription(source_text)

  return render_template('transcribe/transcribe.html',
                          source_text = source_text,
                          target_text = target_text
                        )

def get_transcription(source_text):
    new_text = Transcriber(source_text)
    return new_text
