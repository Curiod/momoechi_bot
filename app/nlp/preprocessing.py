import re
import nltk
from pyaspeller import YandexSpeller
from pymystem3 import Mystem
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

PUNCT_TO_REMOVE = '!"#$%&\'()*+,—./:;<=>?@[\\]^_`{|}~'
STOPWORDS = set(stopwords.words('russian'))


def get_pos(token):
        """ 
        Returns main part-of-speech tag for token. 
        """
        analysis = token.get('analysis')
        if not analysis:
            return None

        gr = analysis[0].get('gr', '')
        return gr.split('=')[0].split(',')[0]


def remove_punct_stopwords(text: str):
    """
    Удаление пунктуации и стоп-слов
    """
    text = text.translate(str.maketrans('-', ' ', PUNCT_TO_REMOVE))
    text = " ".join([word for word in text.split() if word not in STOPWORDS])

    return text


def contains_non_russian_or_non_digit(text: str) -> bool:
    """
    Проверка на содержание нерусскозычных символов
    """
    pattern = r'[^а-яё0-9]'
    return bool(re.search(pattern, text))


def get_pos(token):
    """
    Возвращает часть речи (см. pyaspeller)
    """
    analysis = token.get('analysis')
    if not analysis:
        return None

    gr = analysis[0].get('gr', '')
    return gr.split('=')[0].split(',')[0]
    
    
def preprocess_text(batch):
    """
    Обработка текста:
    - Лемматизация
    - Исправление ошибок
    - Приведение к нижнему регистру
    - Возвращает только существительные и прилагательные (пока что)
    - Удаление стоп-слов
    """
    m = Mystem()
    speller = YandexSpeller(lang='ru')

    # Объединение нескольких текстов для уменьшения частоты вызовов внешних файлов/запросов
    merged_text = ' '.join([t.lower() + ' SP ' for t in batch])

    # Исправление ошибок
    checked_text = speller.spelled(merged_text)

    # Только прилагательные и существительные 
    pos = ['A', 'S']  

    doc = set()
    res = []

    # Морфологический разбор
    tokens = m.analyze(remove_punct_stopwords(checked_text))
    nouns_and_adjectives = []

    for t in tokens:
        text = t.get('text').strip()
        
        # латинские обозначения, названия компаний и т. д.
        if contains_non_russian_or_non_digit(text):
            nouns_and_adjectives.append(text)
            continue
            

        if len(text) < 2 and text !='SP':
            continue
        elif isinstance(t.get('analysis'), list) and len(t.get('analysis'))==0:
            nouns_and_adjectives.append(text)
        elif get_pos(t) in pos:
            nouns_and_adjectives.append(t.get('analysis')[0]['lex'])
        
    # Фильтрация частей речи и разделение на отдельные документы
    for t in nouns_and_adjectives:
        if t != '\n' and t.strip() != '':
            if t != 'SP':
                doc.add(t)
            else:
                res.append(' '.join(list(doc)))
                doc = set()

    return res




