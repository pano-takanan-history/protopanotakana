from collections import defaultdict
from lingpy import Wordlist
from edictor.wordlist import fetch_wordlist
import csv


bpt = Wordlist.from_cldf(
    "../../blumpanotacana/cldf/cldf-metadata.json",
    # columns to be loaded from CLDF set
    columns=(
        "language_id",
        "language_glottocode",
        "concept_concepticon_gloss",
        "segments",
        "form"
        ),
    # a list of tuples of source and target
    namespace=(
        ("language_id", "doculect"),
        ("language_glottocode", "glottocode"),
        ("concept_concepticon_gloss", "concept"),
        ("segments", "tokens"),
        )
    )

lookup = defaultdict()
for item in bpt:
    if bpt[item, 'glottocode'] in ['cash1251', 'cash1252']:
        check = (bpt[item, 'concept'], bpt[item, 'form'])
        if check in lookup:
            lookup[check] = ['Cashibo', 'Kakataibo']
        else:
            lookup[check] = [bpt[item, 'doculect']]
            # print(check)

wl = Wordlist.from_cldf(
    "../cldf/cldf-metadata.json",
    # columns to be loaded from CLDF set
    columns=(
        "language_id",
        "language_glottocode",
        "concept_concepticon_gloss",
        "segments",
        "form"
        ),
    # a list of tuples of source and target
    namespace=(
        ("language_id", "doculect"),
        ("language_glottocode", "glottocode"),
        ("concept_concepticon_gloss", "concept"),
        ("segments", "tokens"),
        )
    )


with open('raw.tsv', "w", encoding="utf-8") as f:
    f.write(
        fetch_wordlist(
            "protopanotakana",
            columns=[
                "CONCEPT",
                "DOCULECT",
                "FORM",
                "VALUE",
                "TOKENS",
                "COGID",
                "COGIDS",
                "ALIGNMENT",
                "MORPHEMES",
                "NOTE",
                "DATASET",
                "CONCEPTICON_GLOSS"
            ],
            base_url='http://lingulist.de/pth/',
            script_url='get_data.py'
        ))

# TODO: Add Concepticon GLOSS to SQLite
fixed = []
manual = []
with open("raw.tsv", newline='') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    for row in tsv_reader:
        # print(row)
        datasets = row[11].split(' ')
        if row[2] == 'Kashibo' and 'blumpanotacana' in datasets:
            check = (row[12], row[3])
            if check in lookup:
                for item in lookup[check]:
                    row[2] = item
                    fixed.append(row)
            else:
                manual.append(row)
                print('Problem: ', check)
        else:
            fixed.append(row)

with open('raw_kakataibo.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerows(fixed)
    writer.writerows(manual)
