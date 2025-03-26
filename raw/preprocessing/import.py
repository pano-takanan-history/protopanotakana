import csv
from collections import defaultdict
from lingpy import Wordlist

datasets = [
    'blumpanotacana',
    'oliveiraprotopanoan',
    'girardprototakanan',
    'valenzuelazariquieypanotakana'
    ]

visited = []
language_table = defaultdict()
concept_table = defaultdict()
form_table = defaultdict()
concept_lookup = defaultdict()

for ds in datasets:
    wl = Wordlist.from_cldf(
        'cldf-resources/' + ds + '/cldf/cldf-metadata.json',
        columns=(
            'id', 'parameter_id', 'concept_name', 'concept_concepticon_id', 'concept_concepticon_gloss',
            'concept_proto_id', 'language_id', 'language_name', 'language_family',
            'language_glottocode', 'value', 'form', 'segments', 'cognacy', 'partial_cognacy',
            'comment', 'alignment', 'source', 'morphemes', 'borrowing'
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

    for i, item in enumerate(wl):
        # Add languages
        checkup_concept = [wl[item, 'language_name'], ds]
        language_id = wl[item, 'doculect'] + '_' + ds
        if checkup_concept not in visited and wl[item, 'language_family'] == 'Pano-Tacanan':
            visited.append(checkup_concept)
            language_table[wl[item, 'language_name']] = [
                language_id,
                wl[item, 'glottolog'],
                ds
                ]

        # Add concepts
        concept_id = wl[item, 'parameter_id'] + '_' + ds
        gloss = wl[item, 'concepticon_gloss']

        if concept_id not in concept_table:
            concept_table[concept_id] = [
                wl[item, 'concept'],
                gloss,
                wl[item, 'concepticon'],
                wl[item, 'concept_proto_id']
                ]

            # Add Concepticon gloss in FormTable
            concept_lookup[concept_id] = gloss if gloss != '' else wl[item, 'concept']

        form_table[i] = [
            wl[item, 'id'],
            language_id,
            parameter_id,
            concept_lookup[concept_id],
            wl[item, 'value'],
            wl[item, 'form'],
            wl[item, 'tokens'],
            wl[item, 'comment'],
            wl[item, 'source'],
            wl[item, 'cognacy'],
            wl[item, 'partial_cognacy'],
            wl[item, 'alignment'],
            wl[item, 'morphemes'],
            wl[item, 'borrowing'],
            ds
        ]

for item in concept_table:
    print(item, concept_table[item])

language_table = dict(sorted(language_table.items(), key=lambda item: item[1][1]))

with open('../../etc/languages.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(['Name', 'ID', 'Glottocode', 'Dataset'])

    for key, values in language_table.items():
        writer.writerow([key] + values)

concept_table = dict(sorted(concept_table.items(), key=lambda item: item[1][0]))
with open('../../etc/concepts.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(['Parameter_ID', 'Concept', 'Concepticon_Gloss', 'Concepticon_ID', 'Proto_ID'])

    for key, values in concept_table.items():
        writer.writerow([key] + values)

with open('../../raw/raw.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow([
        'ID', 'Form_ID', 'Language_ID', 'Parameter_ID', 'Concept', 'Value', 'Form', 'Segments', 'Comment',
        'Source', 'Cognacy', 'Partial_Cognacy', 'Alignment', 'Morphemes', 'Borrowing', 'Dataset'
        ])

    for key, values in form_table.items():
        writer.writerow([key] + values)
