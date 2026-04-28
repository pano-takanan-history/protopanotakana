from lingpy import Wordlist
import csv

wl = Wordlist.from_cldf(
    '../../amazonianvoices/cldf/cldf-metadata.json',
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
add = ["MACAW", "KINGFISHER", "ELECTRIC EEL", "SALIVA", "TARO", "MAHOGANY TREE", "FISH TRAP", "SPEAR", "SHAMAN (FOLK HEALER)", "SONG", "BANISTERIUM", "PACA", "WHITE-LIPPED PECCARY", "SPIDER MONKEY", "ANACONDA (WATER BOA)", "DRAGONFLY"]

for item in wl:
    if wl[item, 'concepticon_gloss'] in add and wl[item, 'family'] == 'Pano-Tacanan':
        additions.append([
            '0',
            wl[item, "concept"],
            wl[item, 'doculect'],
            wl[item, 'form'],
            wl[item, 'value'],
            wl[item, 'tokens'],
            '0',
            '0',
            wl[item, 'tokens'],
            '',
            'None',
            'amazonianvoices',
            wl[item, "concepticon_gloss"],
        ])

# for item in additions:
#     print(item)

# print("---")
# print("Total: ", len(additions))

with open('additions.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerows(additions)
