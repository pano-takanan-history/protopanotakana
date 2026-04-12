from lingpy import Wordlist
from clldutils.misc import slug
import csv

unique_bpt = []
bpt = Wordlist.from_cldf(
    '../cldf/cldf-metadata.json',
    # columns to be loaded from CLDF set
    columns=(
        "language_id",
        "concept_concepticon_gloss",
        "concept_concepticon_id",
        "segments",
        "form",
        "language_family",
        "language_glottocode"
        ),
    # a list of tuples of source and target
    namespace=(
        ("language_id", "doculect"),
        ("concept_concepticon_gloss", "concept"),
        ("concept_concepticon_id", "concepticon_id"),
        ("segments", "tokens"),
        ("language_family", "family"),
        ("language_glottocode", "glottocode")
        )
    )

unique_c_bpt = []
bpt_langs = []

for item in bpt:
    if bpt[item, 'glottocode'] not in bpt_langs:
        bpt_langs.append(bpt[item, 'glottocode'])
    if (bpt[item, "concept"], bpt[item, "glottocode"]) not in unique_bpt:
        unique_bpt.append((bpt[item, "concept"], bpt[item, "glottocode"]))
        if bpt[item, "concept"] not in unique_c_bpt:
            unique_c_bpt.append(bpt[item, "concept"])

wl = Wordlist.from_cldf(
    '../../amazonianvoices/cldf/cldf-metadata.json',
    # columns to be loaded from CLDF set
    columns=(
        "language_id",
        "concept_concepticon_gloss",
        "concept_concepticon_id",
        "segments",
        "form",
        "language_family",
        "language_glottocode"
        ),
    # a list of tuples of source and target
    namespace=(
        ("language_id", "doculect"),
        ("concept_concepticon_gloss", "concept"),
        ("concept_concepticon_id", "concepticon_id"),
        ("segments", "tokens"),
        ("language_family", "family"),
        ("language_glottocode", "glottocode")
        )
    )

unique_c = []
additions = []
for item in wl:
    if wl[item, 'family'] == 'Pano-Tacanan' and (wl[item, 'concept'], wl[item, "glottocode"]) not in unique_bpt:
        # Check if concept exists in the data
        if wl[item, 'concept'] not in unique_c_bpt and wl[item, 'concept'] not in unique_c:
            unique_c.append(wl[item, "concept"])
    
        additions.append([
            '',
            slug(wl[item, "concept"]),
            wl[item, 'doculect'],
            wl[item, 'form'],
            wl[item, 'value'],
            wl[item, 'tokens'],
            '',
            '',
            '',
            '',
            ''
        ])
    
    elif wl[item, 'glottocode'] not in bpt_langs and wl[item, 'family'] == 'Pano-Tacanan':
        additions.append([
            '',
            slug(wl[item, "concept"]),
            wl[item, 'doculect'],
            wl[item, 'form'],
            wl[item, 'value'],
            ' '.join(wl[item, 'tokens']),
            '',
            '',
            '',
            '',
            ''
        ])
    
    # TODO: Add form check for cases where it is there!

# for item in new_concepts:
#     print(item)

print('Check if any of the following can be mapped:')
for item in unique_c:
    print(item)

with open('additions.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerows(additions)
