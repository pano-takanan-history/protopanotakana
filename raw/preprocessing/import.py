import csv
from collections import defaultdict
from clldutils.misc import slug
from lingpy import Wordlist


def write_table(path, header, table):
    with open(path, 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(header)
        for key, values in table.items():
            writer.writerow(values)


datasets = [
    'blumpanotacana',
    'oliveiraprotopanoan',
    'girardprototakanan',
    'valenzuelazariquieypanotakana',
    'girardprotopanotakanan'
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
            ('language_glottocode', 'glottocode'),
            ('segments', 'tokens'),
            ('cognacy', 'cognacy'),
            ('concept_concepticon_id', 'concepticon'),
            ('cogid_cognateset_id', 'cogid'),
            ('concept_concepticon_gloss', 'concepticon_gloss')
            )
        )

    for i, item in enumerate(wl):
        # Add languages
        glottocode = wl[item, 'glottocode']
        lang_id = slug(wl[item, 'language_name'])
        if glottocode not in ['chip1262', 'movi1243', 'mose1249', 'chim1313']:
            if glottocode not in visited:
                visited.append(glottocode)
                language_table[glottocode] = [
                    wl[item, 'language_name'],
                    lang_id,
                    glottocode,
                    [ds]
                ]

            elif ds not in language_table[glottocode][3]:
                 language_table[glottocode][3].append(ds)

        # Add concepts
        gloss = slug(wl[item, 'concept'])
        conc = wl[item, 'concepticon_gloss']
        pid = wl[item, 'concept_proto_id'] + '_' + ds if wl[item, 'concept_proto_id'] else ''
        checkup_id = wl[item, 'concept'] + '_' + ds
        concept_id = conc if conc is not None else gloss

        if concept_id not in concept_table:
            concept_table[concept_id] = [
                gloss,
                wl[item, 'concept'].replace('*', ''),
                conc,
                wl[item, 'concepticon'],
                [pid]
            ]
            concept_lookup[checkup_id] = concept_id

        elif pid not in concept_table[concept_id][4]:
            concept_table[concept_id][4].append(pid)
            

        form_table[i] = [
            wl[item, 'id'],
            lang_id,
            concept_id,
            conc,
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

language_table = dict(sorted(language_table.items(), key=lambda item: item[1][1]))
for item in language_table:
    language_table[item][3] = ', '.join(language_table[item][3])

header_langs = ['Name', 'ID', 'Glottocode', 'Dataset']
write_table('../../etc/languages.tsv', header_langs, language_table)

concept_table = dict(sorted(concept_table.items(), key=lambda item: (item[1][2] is None, item[1][2])))
for item in concept_table:
    cleaned = [pid for pid in concept_table[item][4] if pid != '']
    concept_table[item][4] = ', '.join(cleaned)

header_concepts = ['ID', 'Concept', 'Concepticon_Gloss', 'Concepticon_ID', 'Proto_ID']
write_table('../../etc/concepts.tsv', header_concepts, concept_table)

header_raw = ['Form_ID', 'Language_ID', 'Parameter_ID', 'Concept', 'Value', 'Form', 'Segments',
            'Comment', 'Source', 'Cognacy', 'Partial_Cognacy', 'Alignment', 'Morphemes', 'Borrowing', 'Dataset'
            ]
write_table('../../raw/raw.tsv', header_raw, form_table)
