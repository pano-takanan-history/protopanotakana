import csv
from lingpy import Wordlist
from collections import defaultdict

datasets = [
    'blumpanotacana',
    'oliveiraprotopanoan',
    'girardprototakanan',
    'valenzuelazariquieypanotakana'
    ]
visited = []
language_table = defaultdict()
concept_table = defaultdict()
formtable = defaultdict()

for ds in datasets:
    wl = Wordlist.from_cldf(
        'cldf-resources/' + ds + '/cldf/cldf-metadata.json',
        columns=(
            'parameter_id', 'concept_name', 'concept_concepticon_id', 'concept_concepticon_gloss', 'concept_proto_id',
            'language_id', 'language_name', 'language_family', 'language_glottocode',
            'value', 'form', 'segments', 'cognacy'
            ),
        namespace=(
            ('concept_name', 'concept'),
            ('language_id', 'doculect'),
            ('language_glottocode', 'glottolog'),
            ('segments', 'tokens'),
            ('cognacy', 'cognacy'),
            ('concept_concepticon_id', 'concepticon'),
            ('cogid_cognateset_id', 'cogid'),
            ('concept_concepticon_gloss', 'concepticon_gloss')
            )
        )

    for item in wl:
        # Add languages
        checkup = [wl[item, 'language_name'], ds]
        if checkup not in visited and wl[item, 'language_family'] == 'Pano-Tacanan':
            visited.append(checkup)
            language_table[wl[item, 'language_name']] = [
                wl[item, 'doculect'],
                wl[item, 'glottolog'],
                ds
                ]

        # Add concepts
        if wl[item, 'parameter_id'] not in concept_table:
            concept_table[wl[item, 'parameter_id']] = [
                wl[item, 'concepticon_gloss'],
                wl[item, 'concepticon'],
                wl[item, 'concept_proto_id']
                ]

for item in concept_table:
    print(item, concept_table[item])

with open('languages.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(['Name', 'ID', 'Glottocode', 'Dataset'])

    for key, values in language_table.items():
        writer.writerow([key] + values)

with open('concepts.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(['Parameter_ID', 'Concepticon_Gloss', 'Concepticon_ID', 'Proto_ID'])

    for key, values in concept_table.items():
        writer.writerow([key] + values)
