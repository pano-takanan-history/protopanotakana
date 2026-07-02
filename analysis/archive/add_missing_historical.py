from collections import defaultdict
from lingpy import Wordlist
import csv

ppt = Wordlist.from_cldf(
    '../cldf/cldf-metadata.json',
    # columns to be loaded from CLDF set
    columns=(
        "language_name",
        "concept_concepticon_gloss",
        "concept_concepticon_id",
        "concept_name",
        "segments",
        "form",
        "language_family",
        "language_glottocode"
        ),
    # a list of tuples of source and target
    namespace=(
        ("language_name", "doculect"),
        ("concept_concepticon_gloss", "concept"),
        ("concept_concepticon_id", "concepticon_id"),
        ("segments", "tokens"),
        ("language_family", "family"),
        ("language_glottocode", "glottocode")
        )
    )

lookup = defaultdict(set)
concepts = defaultdict(str)
languages = defaultdict(str)

for item in ppt:
    lookup[ppt[item, "concept"]].add(ppt[item, 'glottocode'])
    concepts[ppt[item, "concept"]] = ppt[item, 'concept_name']
    languages[ppt[item, "glottocode"]] = ppt[item, 'doculect']

wl = Wordlist.from_cldf(
    '../../nordenskioeldmadrededios/cldf/cldf-metadata.json',
    # columns to be loaded from CLDF set
    columns=(
        "language_name",
        "concept_name",
        "concept_concepticon_gloss",
        "concept_concepticon_id",
        "segments",
        "form",
        "value",
        "language_family",
        "language_glottocode"
        ),
    # a list of tuples of source and target
    namespace=(
        ("language_name", "doculect"),
        ("concept_name", "concept"),
        ("concept_concepticon_gloss", "concepticon_gloss"),
        ("concept_concepticon_id", "concepticon_id"),
        ("segments", "tokens"),
        ("language_family", "family"),
        ("language_glottocode", "glottocode")
        )
    )

additions = []
added_c = []

with open("concepts_with_additions.tsv", newline='') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    for row in tsv_reader:
        # print(row)
        added_c.append([row[0]])

exclude = ['reye1240', 'paca1246', 'remo1249', 'poya1241', 'esee1248']
idx = 20778
for item in wl:
    if wl[item, 'concepticon_gloss'] in concepts and \
         wl[item, 'family'] == 'Pano-Takana' and \
            wl[item, 'glottocode'] not in lookup[wl[item, 'concepticon_gloss']] and \
                wl[item, 'glottocode'] not in exclude:
                print(wl[item])
                idx += 1
                additions.append([
                            idx,
                            concepts[wl[item, "concepticon_gloss"]],
                            languages[wl[item, 'glottocode']] if wl[item, 'glottocode'] in languages else wl[item, 'doculect'],
                            wl[item, 'form'],
                            wl[item, 'value'],
                            ' '.join(wl[item, 'tokens']),
                            '0',
                            '0',
                            wl[item, 'tokens'],
                            '',
                            'None',
                            'Nordenskioeld1905',
                            wl[item, "concepticon_gloss"]
                        ])
                
                if [wl[item, "concepticon_gloss"]] not in added_c:
                    added_c.append([wl[item, "concepticon_gloss"]])

print(additions)

with open('historical_to_existing.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerows(additions)

with open('concepts_with_additions.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerows(added_c)
