import codecs
import re
import os


stopwords = ["a", "a's", "able", "about", "above", "according", "accordingly",
             "across", "actually", "after", "afterwards", "again", "against",
             "ain't", "all", "allow", "allows", "almost", "alone", "along",
             "already", "also", "although", "always", "am", "among", "amongst",
             "an", "and", "another", "any", "anybody", "anyhow", "anyone",
             "anything", "anyway", "anyways", "anywhere", "apart", "appear",
             "appreciate", "appropriate", "are", "aren't", "around", "as",
             "aside", "ask", "asking", "associated", "at", "available", "away",
             "awfully", "b", "be", "became", "because", "become", "becomes",
             "becoming", "been", "before", "beforehand", "behind", "being",
             "believe", "below", "beside", "besides", "best", "better",
             "between", "beyond", "both", "brief", "but", "by", "c", "c'mon",
             "c's", "came", "can", "can't", "cannot", "cant", "cause",
             "causes", "certain", "certainly", "changes", "clearly", "co",
             "com", "come", "comes", "concerning", "consequently", "consider",
             "considering", "contain", "containing", "contains",
             "corresponding", "could", "couldn't", "course", "currently", "d",
             "definitely", "described", "despite", "did", "didn't",
             "different", "do", "does", "doesn't", "doing", "don't", "done",
             "down", "downwards", "during", "e", "each", "edu", "eg", "eight",
             "either", "else", "elsewhere", "enough", "entirely", "especially",
             "et", "etc", "even", "ever", "every", "everybody", "everyone",
             "everything", "everywhere", "ex", "exactly", "example", "except",
             "f", "far", "few", "fifth", "first", "five", "followed",
             "following", "follows", "for", "former", "formerly", "forth",
             "four", "from", "further", "furthermore", "g", "get", "gets",
             "getting", "given", "gives", "go", "goes", "going", "gone", "got",
             "gotten", "greetings", "h", "had", "hadn't", "happens", "hardly",
             "has", "hasn't", "have", "haven't", "having", "he", "he's",
             "hello", "help", "hence", "her", "here", "here's", "hereafter",
             "hereby", "herein", "hereupon", "hers", "herself", "hi", "him",
             "himself", "his", "hither", "hopefully", "how", "howbeit",
             "however", "i", "i'd", "i'll", "i'm", "i've", "ie", "if",
             "ignored", "immediate", "in", "inasmuch", "inc", "indeed",
             "indicate", "indicated", "indicates", "inner", "insofar",
             "instead", "into", "inward", "is", "isn't", "it", "it'd",
             "it'll", "it's", "its", "itself", "j", "just", "k", "keep",
             "keeps", "kept", "know", "knows", "known", "l", "last", "lately",
             "later", "latter", "latterly", "least", "less", "lest", "let",
             "let's", "like", "liked", "likely", "little", "look", "looking",
             "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me",
             "mean", "meanwhile", "merely", "might", "more", "moreover", "most",
             "mostly", "much", "must", "my", "myself", "n", "name", "namely",
             "nd", "near", "nearly", "necessary", "need", "needs", "neither",
             "never", "nevertheless", "new", "next", "nine", "no", "nobody",
             "non", "none", "noone", "nor", "normally", "not", "nothing",
             "novel", "now", "nowhere", "o", "obviously", "of", "off", "often",
             "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only",
             "onto", "or", "other", "others", "otherwise", "ought", "our",
             "ours", "ourselves", "out", "outside", "over", "overall", "own",
             "p", "particular", "particularly", "per", "perhaps", "placed",
             "please", "plus", "possible", "presumably", "probably", "provides",
             "q", "que", "quite", "qv", "r", "rather", "rd", "re", "really",
             "reasonably", "regarding", "regardless", "regards", "relatively",
             "respectively", "right", "s", "said", "same", "saw", "say",
             "saying", "says", "second", "secondly", "see", "seeing", "seem",
             "seemed", "seeming", "seems", "seen", "self", "selves", "sensible",
             "sent", "serious", "seriously", "seven", "several", "shall", "she",
             "should", "shouldn't", "since", "six", "so", "some", "somebody",
             "somehow", "someone", "something", "sometime", "sometimes",
             "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
             "specifying", "still", "sub", "such", "sup", "sure", "t", "t's",
             "take", "taken", "tell", "tends", "th", "than", "thank", "thanks",
             "thanx", "that", "that's", "thats", "the", "their", "theirs",
             "them", "themselves", "then", "thence", "there", "there's",
             "thereafter", "thereby", "therefore", "therein", "theres",
             "thereupon", "these", "they", "they'd", "they'll", "they're",
             "they've", "think", "third", "this", "thorough", "thoroughly",
             "those", "though", "three", "through", "throughout", "thru",
             "thus", "to", "together", "too", "took", "toward", "towards",
             "tried", "tries", "truly", "try", "trying", "twice", "two", "u",
             "un", "under", "unfortunately", "unless", "unlikely", "until",
             "unto", "up", "upon", "us", "use", "used", "useful", "uses",
             "using", "usually", "uucp", "v", "value", "various", "very", "via",
             "viz", "vs", "w", "want", "wants", "was", "wasn't", "way", "we",
             "we'd", "we'll", "we're", "we've", "welcome", "well", "went",
             "were", "weren't", "what", "what's", "whatever", "when",
             "whence", "whenever", "where", "where's", "whereafter", "whereas",
             "whereby", "wherein", "whereupon", "wherever", "whether", "which",
             "while", "whither", "who", "who's", "whoever", "whole", "whom",
             "whose", "why", "will", "willing", "wish", "with", "within",
             "without", "won't", "wonder", "would", "would", "wouldn't", "x",
             "y", "yes", "yet", "you", "you'd", "you'll", "you're",
             "you've", "your", "yours", "yourself", "yourselves", "z", "zero"]


def read_message_file(path):
    """
    Reads a message file and returns a map with the translations in this file.
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


def write_message_file(messages, path):
    keys = [k for k in messages]
    keys.sort()
    with codecs.open(path, 'w', 'ISO-8859-1') as f:
        for k in keys:
            entry = "%s=%s" % (k, messages[k])
            f.write(entry)


def append_message(message_file, key, value):
    messages = read_message_file(message_file)
    doit = True
    for k in messages:
        if k == key:
            print("'%s' already is a key in %s" % (key, message_file))
            doit = False
            break
        if value == messages[k]:
            print("'%s' already is a value of key '%s' in %s" %
                  (value, k, message_file))
            doit = False
            break
    if doit:
        entry = "%s=%s\n" % (key, value)
        print("append %s to %s" % (entry.strip(), message_file))
        with codecs.open(message_file, mode='a', encoding='ISO-8859-1') as f:
            f.write(entry)


def check_message_file(translated_file, default_file):
    print("check file %s:" % translated_file)
    translations = read_message_file(translated_file)
    defaults = read_message_file(default_file)
    for key in defaults:
        if key not in translations:
            print("  %s: entry is missing" % key)
    for key in translations:
        if key not in defaults:
            print("  %s: should be removed" % key)


def print_java_fields(messages):
    if type(messages) == str:
        messages = read_message_file(messages)
    keys = []
    for key in messages:
        keys.append(key)
    keys.sort()
    letter = None
    for key in keys:
        first = key[0].lower()
        if first != letter:
            letter = first
            print()
        print("\tpublic static String %s;" % key)


def suggest_key(message):
    """
    Suggests a key for the given message.
    :type message: str
    """
    m = re.sub('[^A-Za-z]', ' ', message)
    key = ""
    for word in m.split(' '):
        if len(word) == 0:
            continue
        part = word.strip().lower()
        if part in stopwords:
            continue
        key += part[0].upper() + part[1:]
    key = re.sub('[^A-Za-z]', '', key)
    return key


def find_string_candidates(app_dir):
    for root, dirs, files in os.walk(app_dir):
        for f in files:
            if f.endswith(('.java', '.html')):
                _find_strings_in_file(root, f)


def _find_strings_in_file(dir, file_name):
    p = re.compile('"@(.*)"')
    path = os.path.join(dir, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        i = 0
        for line in f:
            r = p.search(line)
            if r is not None:
                message = r.group(1)
                print("found '%s' in %s line %s:" % (message,file_name, i))
                print("  proposed message entry:")
                key = suggest_key(message)
                print("  %s=%s" % (key, message))
                print("\n")
            i += 1


