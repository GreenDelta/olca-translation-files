import codecs


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