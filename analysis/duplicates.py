import csv
from lingpy import Wordlist


wl = Wordlist.from_cldf(
    '../cldf/cldf-metadata.json',
    columns= ['concept_name', 'language_id', 'language_family', 'value', 'segments', 'concept_concepticon_id'],
    namespace=(
        ('language_id', 'doculect'),
        ('concept_name', 'concept'),
        ('segments', 'tokens'),
        ('concept_concepticon_id', 'concept_id')
    ))

checkup = []

for item in wl:
    language, form, concept = wl[item, 'doculect'], wl[item, 'tokens'], wl[item, 'concept']

    if (language, form) not in checkup:
        checkup.append((language, form))
    else:
        print('Duplicate:', wl[item])
        print()
