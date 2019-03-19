class Segment(object):

  possible_place = ['bilabial', 'labiodental', 'dental', 'alveolar', 'postalveolar', 'retroflex', 'palatal', 'velar', 'uvular', 'pharyngeal', 'glottal']
  possible_manner = ['stop', 'fricative', 'africate', 'tap', 'flap', 'tap/flap', 'aproximant', 'lateral aproximant', 'nasal', 'trill']
  possible_height = ['close', 'near-close', 'close-mid', 'mid', 'open-mid', 'near-open', 'open']
  possible_backness = ['front', 'central', 'back']
  def __init__(self, is_consonant, is_voiced, place, manner, vowel_height, vowel_backness, is_rounded, is_long):
    self.is_voiced = bool(is_voiced)
    self.is_consonant = is_consonant
    self.place = self.get_place(place)
    self.manner = self.get_manner(manner)
    self.backness = self.get_backness(vowel_backness)
    self.height = self.get_height(vowel_height)
    self.is_long = is_long

    if self.manner in ['stop', 'fricative', 'africate']:
      self.is_obstruent = True
    else:
      self.is_obstruent = False

  def get_place(self, place):
    if place in Segment.possible_place or place=='':
      return place
    else:
      raise(Exception('IncorrectPlace'))

  def get_manner(self, manner):
    if manner == 'tap' or manner == 'flap':
      return 'tap/flap'
    elif manner in self.possible_manner or manner == '':
      return manner
    else:
      raise(Exception('IncorrectManner'))

  def get_backness(self, vowel_backness):
    if vowel_backness in Segment.possible_backness or vowel_backness == '':
      return vowel_backness
    else:
      raise(Exception('IncorrectBackness'))

  def get_height(self, vowel_height):
    if vowel_height in  Segment.possible_height or vowel_height == '':
      return vowel_height
    else:
      raise(Exception('IncorrectHeight'))