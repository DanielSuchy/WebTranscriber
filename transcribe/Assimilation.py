from .Alphabet import Alphabet
from .Segment import Segment

class Assimilation(object):

  def __init__(self):
    self.alphabet = Alphabet()

  def apply_place_assimilation(self, letter, next_letter):
    next_segment = self.alphabet.get_phonetic_description(next_letter)

    if letter == 'n' and next_segment.place == 'velar':
      letter = 'ŋ'
    elif letter == 'm' and next_segment.place == 'labiodental':
      letter = 'ɱ'

    return letter

  def apply_voicing_assimilation(self, letter, next_letter):
    current_segment = self.alphabet.get_phonetic_description(letter)

    if next_letter == ' ' and current_segment.is_obstruent == True:
      new_segment = Segment(current_segment.is_consonant, False, current_segment.place, current_segment.manner, '', '', False, False)
      letter = self.alphabet.get_symbol_by_phoneme(new_segment)
      return letter

    next_segment = self.alphabet.get_phonetic_description(next_letter)

    if current_segment.place == 'labiodental' and current_segment.manner == 'fricative' and next_segment.is_obstruent == True:
      current_segment.is_obstruent = False #v behaves as non-obstruent only if is being asimilated

    if (current_segment.is_obstruent == True
        and next_segment.is_consonant == True
        and next_segment.is_obstruent == True
        or (letter == 'v' and next_letter != ' ') # exception
       ):
      new_segment = Segment(current_segment.is_consonant, next_segment.is_voiced, current_segment.place, current_segment.manner, '','',False, False)
      letter = self.alphabet.get_symbol_by_phoneme(new_segment)
    return letter
