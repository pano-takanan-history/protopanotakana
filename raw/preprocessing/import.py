from lingpy import Wordlist
from collections import defaultdict

datasets = ['blumpanotacana', 'oliveiraprotopanoan', 'girardprototakanan', 'valenzuelazariquieypanotakana']

language_table = defaultdict()

for ds in datasets:
    wl = Wordlist.from_cldf('cldf-resources/' + ds + '/cldf/cldf-metadata.json')

    for item in wl:

        if wl[item, 'language_name'] not in language_table:
            language_table[wl[item, 'language_name']] = [
                wl[item, 'glottolog'],
                wl[item, 'doculect'],
                ds
                ]

for item in language_table:
    print(item, language_table[item])