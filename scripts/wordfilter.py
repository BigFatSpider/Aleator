def longest_possible_word_length():
    return 189819

class iterlines(object):
    def __init__(self, filehandle):
        self._filehandle = filehandle

    def __iter__(self):
        self._filehandle.seek(0)
        return self

    def __next__(self):
        line = self._filehandle.readline()
        if line == '':
            raise StopIteration
        return line.strip('\n')

def generate_wordlist_from_file(filename, pred):
    with open(filename, 'r') as f:
        for word in iterlines(f):
            if pred(word.replace('\n', '')):
                yield word

def generate_wordlist_from_dict(pred):
    for word in generate_wordlist_from_file('/usr/share/dict/words', pred):
        yield word

def generate_wordlist(pred, wordlist=None, filename=None):
    if wordlist is not None:
        return [word for word in wordlist if pred(word)]
    if filename is not None:
        return [word for word in generate_wordlist_from_file(filename, pred)]
    return [word for word in generate_wordlist_from_dict(pred)]

def words_by_ending(ending, wordlist=None):
    def endswith(word):
        return word.endswith(ending)
    return generate_wordlist(endswith, wordlist)

def words_by_start(start, wordlist=None):
    def startswith(word):
        return word.startswith(start)
    return generate_wordlist(startswith, wordlist)

def words_by_length(length, wordlist=None):
    def is_correct_length(word):
        return len(word) == length
    def is_correct_length_tuple(word):
        return len(word) >= length[0] and len(word) <= length[1]
    if isinstance(length, tuple):
        return generate_wordlist(is_correct_length_tuple, wordlist)
    return generate_wordlist(is_correct_length, wordlist)

def words_by_maxlength(maxlength, wordlist=None):
    return words_by_length((1, maxlength), wordlist)

def words_by_minlength(minlength, wordlist=None):
    return words_by_length((minlength, longest_possible_word_length()), wordlist)

def len_hist(wordlist, should_print=False):
    def extend_to_length(arr, newlen):
        oldlen = len(arr)
        if newlen > oldlen:
            arr.extend([0] * (newlen - oldlen))
            assert(len(arr) == newlen)

    hist = []
    for word in wordlist:
        oldlen = len(hist)
        wordlen = len(word)
        if wordlen >= oldlen:
            extend_to_length(hist, wordlen + 1)
            assert(len(hist) == wordlen + 1)
        hist[wordlen] += 1
    if should_print:
        print_len_hist(hist)
    return hist

def print_len_hist(h):
    print('Word length histogram:')
    total = 0
    for idx in range(len(h)):
        if h[idx] > 0:
            print('\t' + str(h[idx]) + ' words of length ' + str(idx))
            total += h[idx]
    print(str(total) + ' words total')

def remove_duplicates(wordlist):
    unique_words = set()
    for word in wordlist:
        unique_words.add(word)
    wordlist = list(unique_words)
    return wordlist

def words_from_file(filename):
    return generate_wordlist(lambda w: True, None, filename)

def remove_vowels(wordlist, include_y=False):
    wordmap = dict()
    vowels = 'aeiouy' if include_y else 'aeiou'
    for word in wordlist:
        trimmed = ''.join([c for c in word if c.lower() not in vowels])
        wordmap[trimmed] = word
    return wordmap

