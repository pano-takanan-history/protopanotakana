from lingpy import Wordlist
from clldutils.misc import slug
import csv

unique_ppt = []
ppt = Wordlist.from_cldf(
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

unique_c_ppt = []
ppt_langs = []

for item in ppt:
    # if ppt[item, 'glottocode'] not in ppt_langs:
    #     ppt_langs.append(ppt[item, 'glottocode'])
    if (ppt[item, "concept"], ppt[item, "glottocode"]) not in unique_ppt:
        unique_ppt.append((ppt[item, "concept"], ppt[item, "glottocode"]))
        if ppt[item, "concept"] not in unique_c_ppt:
            unique_c_ppt.append(ppt[item, "concept"])

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

unique_c = []
additions = []
add = ["MACAW", "KINGFISHER", "ELECTRIC EEL", "CHESTNUT", "SALIVA", "CASHEW", "COCONUT", "TARO", "MAHOGANY TREE", "FISH TRAP", "SPEAR", "SHAMAN (FOLK HEALER)", "SONG", "BANISTERIUM", "PACA", "WHITE-LIPPED PECCARY", "SPIDER MONKEY", "ANACONDA (WATER BOA)", "DRAGONFLY"]

for item in wl:
    print(wl[item, 'concept'])

    if wl[item, 'concepticon_gloss'] == 'None':
        pass
    elif wl[item, 'family'] == 'Pano-Tacanan' and (wl[item, 'concepticon_gloss'], wl[item, "glottocode"]) not in unique_ppt:
        # Check if concept exists in the data
        if wl[item, 'concepticon_gloss'] not in unique_c_ppt and wl[item, 'concept'] not in unique_c:
            unique_c.append(wl[item, "concepticon_gloss"])

        if wl[item, 'concepticon_gloss'] in add:
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
    
    # elif wl[item, 'glottocode'] not in ppt_langs and wl[item, 'family'] == 'Pano-Tacanan':
    #     additions.append([
    #         '',
    #         slug(wl[item, "concept"]),
    #         wl[item, 'doculect'],
    #         wl[item, 'form'],
    #         wl[item, 'value'],
    #         ' '.join(wl[item, 'tokens']),
    #         '',
    #         '',
    #         '',
    #         '',
    #         ''
    #     ])
    
    # TODO: Add form check for cases where concept is there!
    # 82_camucamu,82,camu-camu,,,camu camu,Myrciaria dubia,Agriculture and vegetation


# for item in additions:
#     print(item)

# print("---")
# print("Total: ", len(additions))
# print('Check if any of the following can be mapped:')
# for item in unique_c:
#     print(item)
# print("---")
# print("Total concepts: ", len(unique_c))

with open('additions.tsv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerows(additions)
