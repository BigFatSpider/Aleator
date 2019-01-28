from wordfilter import *
from os import path

if __name__ == '__main__':
    datadir = path.abspath(path.join(path.dirname(__file__), path.join('..', 'data')))
    nouns = words_from_file(path.join(datadir, 'nounlist.txt'))
    adverbs = words_by_ending('ly')
    nounsadverbs = nouns + adverbs
    nounsadverbs = remove_duplicates(nounsadverbs)
    vowels_removed = remove_vowels(nounsadverbs)
    short_words = {}
    for key in vowels_removed.keys():
        if len(key) < 8:
            short_words[key] = vowels_removed[key]
    linetexts = [short_words[key].lower() + '\t' + key.lower() for key in short_words.keys()]
    linetexts.sort()
    with open(path.join(datadir, 'curatedwords.txt'), 'w') as fout:
        for line in linetexts:
            num_written = fout.write(line + '\n')

