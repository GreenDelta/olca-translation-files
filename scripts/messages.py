import codecs
import re


def read_file(path):
    """
    Returns a map that contains the messages of the file with the given path.
    """
    with codecs.open(path, 'r', 'ISO-8859-1') as f:
        m = {}
        for row in f:
            if '=' not in row:
                continue
            key, value = row.partition('=')[::2]
            key = key.strip()
            value = value.strip()
            m[key] = value
        return m


def check_file(translated_file, default_file):
    print("check file %s:" % translated_file)
    translations = read_file(translated_file)
    defaults = read_file(default_file)
    for key in defaults:
        if key not in translations:
            print("  %s: entry is missing" % key)
    for key in translations:
        if key not in defaults:
            print("  %s: should be removed" % key)


def suggest_key(message):
    """
    Suggests a key for the given message.
    :type message: str
    """
    stopwords = []
    with open('stopwords.txt', 'r') as f:
        for word in f:
            stopwords.append(word.strip().lower())
    key = ""
    for m in message.split(' '):
        part = m.strip().lower()
        if part in stopwords:
            continue
        key += part[0].upper() + part[1:]
    key = re.sub('[^A-Za-z]', '', key)
    return key