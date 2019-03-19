from .Segment import Segment

class Alphabet(object):
  #is_consonant, is_voiced, place, manner, vowel_height, vowel_backness, is_rounded, is_long
  Segments = {
    'á': ['aː', Segment(False, True,  '', '', 'open', 'front', False, True)],
    'a': ['a', Segment(False,True, '', '', 'open', 'front', False, False)],
    'e': ['ɛ', Segment(False, True, '', '', 'open-mid', 'front', False, False)],
    'ě': ['ɛ', Segment(False, True, '', '', 'open-mid', 'front', False, False)],
    'é': ['ɛː', Segment(False, True, '', '', 'open-mid', 'front', False, True)],
    'í': ['iː', Segment(False, True, '', '',    'close', 'front', False, True)],
    'i': ['ɪ', Segment(False, True, '', '', 'near-close', 'front', False, False)],
    'y': ['ɪ', Segment(False, True, '', '', 'near-close', 'front', False, False)],
    'ý': ['iː', Segment(False, True, '','', 'close', 'front', False, True)],
    'ó': ['oː', Segment(False, True, '','','close-mid', 'back', True, True)],
    'o': ['o', Segment(False, True,'','','close-mid', 'back', True, False)],
    'u': ['u', Segment(False,True, '','','close', 'back', True, False)],
    'ú': ['uː', Segment(False, True,'','','close', 'back', True, True)],
    'ů': ['uː', Segment(False,True,'','','close', 'back', True, True)],
    'c': ['t͡s', Segment(True,False, 'alveolar', 'africate','','',False,False)],
    'č': ['t͡ʃ', Segment(True,False, 'postalveolar', 'africate','','',False,False)],
    'ď': ['ɟ', Segment(True,True, 'palatal', 'stop','','',False,False)],
    'h': ['ɦ', Segment(True,True, 'glottal', 'fricative','','',False,False)],
    'ch': ['x', Segment(True,False, 'velar', 'fricative','','',False,False)],
    'ň': ['ɲ', Segment(True,True, 'palatal', 'nasal','','',False,False)],
    'r': ['r', Segment(True,True, 'alveolar', 'trill','','',False,False)],
    'ř': ['r̝', Segment(True,True, 'alveolar', 'trill','','',False,False)],
    'š': ['ʃ', Segment(True,False, 'postalveolar', 'fricative','','',False,False)],
    'ʃ': ['ʃ', Segment(True,False, 'postalveolar', 'fricative','','',False,False)],
    'ť': ['c', Segment(True,False, 'palatal', 'stop','','',False,False)],
    'w': ['v', Segment(True,True, 'labiodental', 'fricative','','',False,False)],
    'ž': ['ʒ', Segment(True,True, 'postalveolar', 'fricative','','',False,False)],
    'g': ['g', Segment(True,True, 'velar', 'stop','','',False,False)],
    'k': ['k', Segment(True,False, 'velar', 'stop','','',False,False)],
    's': ['s', Segment(True,False, 'alveolar', 'fricative','','',False,False)],
    'z': ['z', Segment(True,True, 'alveolar', 'fricative','','',False,False)],
    'j': ['j', Segment(True,True, 'palatal', 'aproximant','','',False,False)],
    'd': ['d', Segment(True,True, 'alveolar', 'stop','','',False,False)],
    't': ['t', Segment(True,False, 'alveolar', 'stop','','',False,False)],
    'n': ['n', Segment(True,True, 'alveolar', 'nasal','','',False,False)],
    'm': ['m', Segment(True,True, 'bilabial', 'nasal','','',False,False)],
    'v': ['v', Segment(True,True, 'labiodental', 'fricative','','',False,False)],
    'b': ['b', Segment(True,True, 'bilabial', 'stop','','',False,False)],
    'p': ['p', Segment(True,False, 'bilabial', 'stop','','',False,False)],
    'l': ['l', Segment(True,True, 'alveolar', 'lateral aproximant','','',False,False)],
    'f': ['f', Segment(True,False, 'labiodental', 'fricative','','',False,False)],
    ' ': [' ', Segment(False,False, '', '','','',False,False)],
    ',': [',', Segment(False,False, '', '','','',False,False)],
    '.': ['.', Segment(False,False, '', '','','',False,False)],
    '|': ['|', Segment(False,False, '', '','','',False,False)]
  }

  def get_symbol_by_phoneme(self, phoneme):
    for entry in Alphabet.Segments:
      if entry != ' ':
        current_phoneme = Alphabet.Segments[entry][1]
        current_voicing = current_phoneme.is_voiced
        current_place = current_phoneme.place
        current_manner = current_phoneme.manner

        if (phoneme.place == current_phoneme.place
            and phoneme.manner == current_phoneme.manner
            and phoneme.is_voiced == current_phoneme.is_voiced
           ):
            return Alphabet.Segments[entry][0]
            break

    raise(Exception("SegmentNotFound"))



  def get_phonetic_representation(self, letter):
    return Alphabet.Segments[letter][0]

  def get_phonetic_description(self, letter):
    try:
      return Alphabet.Segments[letter][1]
    except KeyError:
      return Segment(False, False, '','','','', False, False)

  def get_textual_representation(self, symbol):
    letters = []
    letters_IPA = []

    for entry in Alphabet.Segments:
      key = entry
      letters.append(key)
      letters_IPA.append(Alphabet.Segments[key][0])


    i = letters_IPA.index(symbol)
    return letters[i]
