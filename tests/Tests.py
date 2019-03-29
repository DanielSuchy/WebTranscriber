import unittest
from os import listdir, path
from ..transcribe.Transcriber import Transcriber
from ..transcribe.Segment import Segment
from ..transcribe.Alphabet import Alphabet
from ..transcribe.Assimilation import Assimilation

class TestSegment(unittest.TestCase):

  def test_create_segment(self):
    segment = Segment(True, False, 'bilabial', 'stop', '', '', False, False)
    self.assertEqual(segment.is_consonant, True)
    self.assertEqual(segment.is_voiced, False)
    self.assertEqual(segment.place, 'bilabial')
    self.assertEqual(segment.manner,  'stop')

    segment = Segment(False, True, '', '', 'close', 'front', False, False)
    self.assertEqual(segment.is_consonant, False)
    self.assertEqual(segment.is_voiced, True)
    self.assertEqual(segment.height, 'close')
    self.assertEqual(segment.backness, 'front')

  def test_rename_segment(self):
    segment = Segment(True, True, 'alveolar', 'tap', '', '', False, False)
    self.assertEqual(segment.manner, 'tap/flap')

    segment = Segment(True, True, 'alveolar', 'flap', '', '', False, False)
    self.assertEqual(segment.manner, 'tap/flap')


  def test_incorrect_segment(self):
    with self.assertRaises(Exception):
      Segment(True, True, 'test', 'stop', '', '', False, False)

    with self.assertRaises(Exception):
      Segment(True, True, 'bilabial', 'test', '', '', False, False)

    with self.assertRaises(Exception):
      Segment(False, True, '', '', 'close', 'test', False, False)

    with self.assertRaises(Exception):
      Segment(False, True, '', '', 'test', 'front', False, False)

class TestAlphabet(unittest.TestCase):

  def test_get_phonetic_representation(self):
    a = Alphabet()

    phon = a.get_phonetic_representation('á')
    self.assertEqual(phon, 'aː')

    phon = a.get_phonetic_representation('c')
    self.assertEqual(phon, 't͡s')

  def test_get_phonetic_description(self):
    a = Alphabet()

    test_segment = Segment(True, False, 'velar', 'fricative', '', '', False, False)
    phon = a.get_phonetic_description('ch')
    self.assertEqual(vars(phon), vars(test_segment))

    test_segment = Segment(False, True, '', '', 'open', 'front', False, True)
    phon = a.get_phonetic_description('á')
    self.assertEqual(vars(phon), vars(test_segment))

  def test_get_textual_representation(self):
    a = Alphabet()

    letter = a.get_textual_representation('t͡s')
    self.assertEqual(letter, 'c')

    letter = a.get_textual_representation('aː')
    self.assertEqual(letter, 'á')

  def test_get_symbol_by_phoneme(self):
    a = Alphabet()
    k = a.get_symbol_by_phoneme(Segment(True, False, 'velar', 'stop', '', '', False, False))
    self.assertEqual(k, 'k')

    r = a.get_symbol_by_phoneme(Segment(True, True, 'alveolar', 'trill', '', '', False, False))
    self.assertEqual(r, 'r')

    a_long = a.get_symbol_by_phoneme(Segment(False, True, '','', 'open', 'front', False, True))
    self.assertEqual(a_long, 'aː')

class TestTranscriber(unittest.TestCase):

  def test_simple_words(self):
    t = Transcriber('pes')
    self.assertEqual(str(t), 'pɛs')

    t = Transcriber('čaj')
    self.assertEqual(str(t), 't͡ʃaj')

    t = Transcriber('pes pije')
    self.assertEqual(str(t), 'pɛs pɪjɛ')

    t = Transcriber('pes pije vodu')
    self.assertEqual(str(t), 'pɛs pɪjɛ vodu')

  def test_ch(self):
    t = Transcriber('ch')
    self.assertEqual(str(t), 'x')

    t = Transcriber('hroch chrochtá')
    self.assertEqual(str(t), 'ɦrox xroxtaː')

  def test_apply_place_assimilation(self):
    a = Assimilation()
    velar_n = a.apply_place_assimilation('n', 'k')
    self.assertEqual(velar_n, 'ŋ')

    velar_n = a.apply_place_assimilation('n', 'g')
    self.assertEqual(velar_n, 'ŋ')

    labiodental_m = a.apply_place_assimilation('m', 'v')
    self.assertEqual(labiodental_m, 'ɱ')

    t = Transcriber('banka')
    self.assertEqual(str(t), 'baŋka')

    t = Transcriber('tango')
    self.assertEqual(str(t), 'taŋgo')

  def test_apply_voicing_assimilation_segments(self):
    assimilation = Assimilation()
    t = assimilation.apply_voicing_assimilation('d', 'k')
    self.assertEqual(t, 't')

    d = assimilation.apply_voicing_assimilation('t', 'g')
    self.assertEqual(d, 'd')

    k = assimilation.apply_voicing_assimilation('k', 'r')
    self.assertEqual('k', k)

    p = assimilation.apply_voicing_assimilation('b', 'k')
    self.assertEqual('p', p)

    p = assimilation.apply_voicing_assimilation('p', 'k')
    self.assertEqual('p', p)

    s = assimilation.apply_voicing_assimilation('z', 'k')
    self.assertEqual('s', s)

  def test_get_last_consonant(self):
    transcriber = Transcriber('')
    k = transcriber.get_last_consonant('lebka', 2)
    self.assertEqual(k, 'k')

    b = transcriber.get_last_consonant('věždba', 2)
    self.assertEqual(b, 'b')

    p = transcriber.get_last_consonant('prst', 0)
    self.assertEqual(p, 'p')

    k = transcriber.get_last_consonant('odkráčet', 1)
    self.assertEqual(k, 'k')

    h = transcriber.get_last_consonant('typ hlásky', 2)
    self.assertEqual(h, 'h')

  def test_enword_voicing(self):
    assimilation = Assimilation()
    p = assimilation.apply_voicing_assimilation('b', ' ')
    self.assertEqual(p, 'p')

    transcriber = Transcriber('blb')
    #self.assertEqual(str(transcriber), 'blp')
    self.assertEqual(str(transcriber), 'bl̩p')

    transcriber = Transcriber('chlup')
    self.assertEqual(str(transcriber), 'xlup')

  def test_apply_voicing_assimilation_words(self):
    transcriber = Transcriber('lebka')
    self.assertEqual(str(transcriber), 'lɛpka')

    transcriber = Transcriber('odkráčet')
    self.assertEqual(str(transcriber), 'ʔotkraːt͡ʃɛt')

    transcriber = Transcriber('rozkrojit')
    self.assertEqual(str(transcriber), 'roskrojɪt')

    transcriber = Transcriber('kdo')
    self.assertEqual(str(transcriber), 'gdo')

    transcriber = Transcriber('sblížit se')
    self.assertEqual(str(transcriber), 'zbliːʒɪt sɛ')

    transcriber = Transcriber('věštba')
    self.assertEqual(str(transcriber), 'vjɛʒdba')

    # transcriber = Transcriber('švédský')
    # self.assertEqual(str(transcriber),  'ʃvɛːtskiː')

  def test_multiple_word_assimilation(self):
    transcriber = Transcriber('typ hlásky')
    self.assertEqual(str(transcriber), 'tɪb ɦlaːskɪ')

    transcriber = Transcriber('hod kladivem')
    self.assertEqual(str(transcriber), 'ɦot klaɟɪvɛm')

    transcriber = Transcriber('hod diskem')
    self.assertEqual(str(transcriber), 'ɦod ɟɪskɛm')

    transcriber = Transcriber('hod míčem')
    self.assertEqual(str(transcriber), 'ɦot miːt͡ʃɛm')

    transcriber = Transcriber('let letadla')
    self.assertEqual(str(transcriber), 'lɛt lɛtadla')


  def test_handle_soft_e(self):
    transcriber = Transcriber('')

    vj = transcriber.handle_soft_e('v')
    self.assertEqual('vj', vj)

    mn = transcriber.handle_soft_e('m')
    self.assertEqual('mɲ', mn)

    d = transcriber.handle_soft_e('d')
    self.assertEqual('ɟ', d)

    c = transcriber.handle_soft_e('t')
    self.assertEqual('c', c)

    transcriber = Transcriber('době')
    self.assertEqual(str(transcriber), 'dobjɛ')

    transcriber = Transcriber('kromě')
    self.assertEqual(str(transcriber), 'kromɲɛ')

    transcriber = Transcriber('silně')
    self.assertEqual(str(transcriber), 'sɪlɲɛ')

    transcriber = Transcriber('těmi')
    self.assertEqual(str(transcriber), 'cɛmɪ')

    transcriber = Transcriber('měděně')
    self.assertEqual(str(transcriber), 'mɲɛɟɛɲɛ')

    transcriber = Transcriber('uměnovědě')
    self.assertEqual(str(transcriber), 'ʔumɲɛnovjɛɟɛ')

  def test_handle_i_palatalization(self):
    transcriber = Transcriber('')
    t = transcriber.handle_i_palatalization('t')
    self.assertEqual(t, 'c')

    d = transcriber.handle_i_palatalization('d')
    self.assertEqual(d, 'ɟ')

    n = transcriber.handle_i_palatalization('n')
    self.assertEqual(n, 'ɲ')

    transcriber = Transcriber('nemocnice')
    self.assertEqual(str(transcriber), 'nɛmot͡sɲɪt͡sɛ')

    transcriber = Transcriber('pohltila')
    self.assertEqual(str(transcriber), 'poɦl̩cɪla')

    transcriber = Transcriber('hladina')
    self.assertEqual(str(transcriber), 'ɦlaɟɪna')

    transcriber = Transcriber('zapomnění')
    self.assertEqual(str(transcriber), 'zapomɲɛɲiː')

  def test_handle_glottal_stop(self):
    transcriber = Transcriber('co otestovat')
    self.assertEqual(str(transcriber), 't͡so ʔotɛstovat')

    transcriber = Transcriber('na oddělení')
    self.assertEqual(str(transcriber), 'na ʔodɟɛlɛɲiː')

    transcriber = Transcriber('a asi ano')
    self.assertEqual(str(transcriber), 'ʔa ʔasɪ ʔano')

  def test_handle_diftong(self):
    transcriber = Transcriber('louka')
    self.assertEqual(str(transcriber), 'lo͡uka')

    transcriber = Transcriber('používat')
    self.assertEqual(str(transcriber), 'po͡uʒiːvat')

    transcriber = Transcriber('často učí')
    self.assertEqual(str(transcriber), 't͡ʃasto ʔut͡ʃiː')

    transcriber = Transcriber('outfit')
    self.assertEqual(str(transcriber), 'ʔo͡utfɪt')

  def test_handle_sylabic_consonant(self):
    transcriber = Transcriber('plch')
    self.assertEqual(str(transcriber), 'pl̩x')

    transcriber = Transcriber('plech')
    self.assertEqual(str(transcriber), 'plɛx')

    transcriber = Transcriber('prchnout')
    self.assertEqual(str(transcriber), 'pr̩xno͡ut')

  def test_handle_soft_r_assimilation(self):
    transcriber = Transcriber('příroda')
    self.assertEqual(str(transcriber), 'pr̝̊iːroda')

    transcriber = Transcriber('keř')
    self.assertEqual(str(transcriber), 'kɛr̝̊')

    transcriber = Transcriber('řek')
    self.assertEqual(str(transcriber), 'r̝ɛk')

    transcriber = Transcriber('dři')
    self.assertEqual(str(transcriber), 'dr̝ɪ')

  def test_prosodic_interval(self):
    transcriber = Transcriber("slovo, slovo")
    self.assertEqual(str(transcriber), 'slovo | slovo')

    transcriber = Transcriber("slovo. slovo")
    self.assertEqual(str(transcriber), 'slovo || slovo')

    transcriber = Transcriber('typ, hlásky')
    self.assertEqual(str(transcriber), 'tɪp | ɦlaːskɪ')

  def test_full_sentences(self):
    transcriber = Transcriber("Kokos kapal na koberec")
    self.assertEqual(str(transcriber), "kokos kapal na kobɛrɛt͡s")

    transcriber = Transcriber("Provoz balil vesnici do smogu")
    self.assertEqual(str(transcriber), "provoz balɪl vɛsɲɪt͡sɪ do smogu")

    transcriber = Transcriber("Hrozba upadla v zapomnění")
    self.assertEqual(str(transcriber), "ɦrozba ʔupadla v zapomɲɛɲiː")

    transcriber = Transcriber("Fotka vzbudila pozornost")
    self.assertEqual(str(transcriber), "fotka vzbuɟɪla pozornost")

    transcriber = Transcriber("Vozka spadl z kozlíku")
    self.assertEqual(str(transcriber), "voska spadl̩ s kozliːku")

    transcriber = Transcriber("Prosba všechny zaskočila")
    self.assertEqual(str(transcriber), "prozba fʃɛxnɪ zaskot͡ʃɪla")

    transcriber = Transcriber("Troska vyšla ze sklepení")
    self.assertEqual(str(transcriber), "troska vɪʃla zɛ sklɛpɛɲiː")

    transcriber = Transcriber("Podej mi prosím tě tamten kokos")
    self.assertEqual(str(transcriber), "podɛj mɪ prosiːm cɛ tamtɛn kokos")

    transcriber = Transcriber("Podzimní setba rolníkům nevyšla")
    self.assertEqual(str(transcriber), "podzɪmɲiː sɛdba rolɲiːkuːm nɛvɪʃla") # is africate????????

    transcriber = Transcriber("Připrav se radši na hustý provoz")
    self.assertEqual(str(transcriber), "pr̝̊ɪpraf sɛ ratʃɪ na ɦustiː provos")

    transcriber = Transcriber("Porod kazil klid na oddělení")
    self.assertEqual(str(transcriber), "porot kazɪl klɪt na ʔodɟɛlɛɲiː")

    transcriber = Transcriber("kokos baštil ve vaně")
    self.assertEqual(str(transcriber), "kokoz baʃcɪl vɛ vaɲɛ")

    transcriber = Transcriber("Říznutá vodka nebyla k pití")
    self.assertEqual(str(transcriber), "r̝iːznutaː votka nɛbɪla k pɪciː")

    transcriber = Transcriber("Provoz kalil náladu chodců")
    self.assertEqual(str(transcriber), "provos kalɪl naːladu xott͡suː")

    transcriber = Transcriber("Robot bažil po klidu v ústraní")
    self.assertEqual(str(transcriber), "robod baʒɪl po klɪdu v ʔuːstraɲiː")

    transcriber = Transcriber("Špinavá chodba zela prázdnotou")
    self.assertEqual(str(transcriber), "ʃpɪnavaː xodba zɛla praːzdnoto͡u")

    transcriber = Transcriber("Tohle byl opravdu rychlý porod")
    self.assertEqual(str(transcriber), "toɦlɛ bɪl ʔopravdu rɪxliː porot")

    transcriber = Transcriber("Tuhle mi připadlo, že jsem robot")
    self.assertEqual(str(transcriber), "tuɦlɛ mɪ pr̝̊ɪpadlo | ʒɛ jsɛm robot")

    transcriber = Transcriber("V noci se robot kasal svými výkony")
    self.assertEqual(str(transcriber), "v not͡sɪ sɛ robot kasal sviːmɪ viːkonɪ")

    transcriber = Transcriber("Porod bavil všechny přítomné")
    self.assertEqual(str(transcriber), "porod bavɪl fʃɛxnɪ pr̝̊iːtomnɛː")



if __name__ == "__main__":
	unittest.main()
