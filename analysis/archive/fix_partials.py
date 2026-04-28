import csv
import numpy as np
from collections import defaultdict
from edictor.wordlist import fetch_wordlist
from lingpy import Wordlist, Alignments
from lingpy.compare.partial import Partial
from lingreg.lingreg import get_copar, score_cognateset, reduce_cogids

# with open('data.tsv', "w", encoding="utf-8") as f:
#     f.write(
#         fetch_wordlist(
#             "protopanotakana",
#             columns=[
#                 "CONCEPT",
#                 "DOCULECT",
#                 "FORM",
#                 "VALUE",
#                 "TOKENS",
#                 "COGID",
#                 "COGIDS",
#                 "ALIGNMENT",
#                 "MORPHEMES",
#                 "NOTE",
#                 "DATASET"
#             ],
#             base_url='http://lingulist.de/pth/',
#             script_url='get_data.py'
#         ))


# wl = Wordlist('data.tsv')

# # Run automated partial cognate detection
# lex = Partial(wl, segments='tokens', check=True)
# lex.get_scorer(runs=10000)
# lex.partial_cluster(threshold=0.55, method="lexstat", cluster_method="infomap", ref="autocogids")
# lex.output('tsv', filename='autocogids')

# # ------------------------------------
# # Update missing cogids
# alms = Alignments('autocogids.tsv', ref='cogids', transcriptions='tokens')

# output = [['ID', 'CONCEPT', 'DOCULECT', 'FORM', 'VALUE', 'TOKENS', 'COGID', 'COGIDS', 'ALIGNMENT', 'MORPHEMES', 'NOTE', 'DATASET']]

# counter = 9999
# for item in alms:
#     cogids = str(alms[item, 'cogids']).split(' ')
#     form = str(alms[item, 'tokens']).split(' + ')
#     # print(form)
#     if len(cogids) != len(str(alms[item, 'autocogids']).split(' ')):
#         new_cogids = []
#         for i in str(alms[item, 'autocogids']).split(' '):
#             counter += 1
#             new_cogids.append(str(counter))

#         if len(cogids) == 1:
#             if form[0] in ['e', 'a']:
#                 new_cogids[1] = cogids[0]
#             else:
#                 new_cogids[0] = cogids[0]
#         alms[item, "cogids"] = ' '.join(new_cogids)

# alms.renumber('cogids')

# for item in alms:
#     alms[item, 'cogids'] = str(alms[item, 'cogids']).split(' ')

# alms.add_entries("alignments_in_source", "alignment", lambda x: x)
# alms.align(ref='cogids')

# for item in alms:
#     print(alms[item, 'cogids'])
#     print(alms[item, 'alignment'])
#     print(alms[item, 'alignments_in_source'])
#     print('----')

# i = 0
# for i, item in enumerate(alms):
#     i += 1
#     output.append([
#         i,
#         alms[item, 'CONCEPT'],
#         alms[item, 'DOCULECT'],
#         alms[item, 'FORM'],
#         alms[item, 'VALUE'],
#         alms[item, 'TOKENS'],
#         alms[item, 'COGID'],
#         ' '.join(alms[item, 'COGIDS']),
#         alms[item, 'ALIGNMENT'],
#         ' '.join(alms[item, 'MORPHEMES']),
#         alms[item, 'NOTE'],
#         alms[item, 'DATASET']
#     ])

# with open('new_data.tsv', 'w', encoding='utf8') as file:
#     writer = csv.writer(file, delimiter='\t')
#     writer.writerows(output)

# # ------------------------------------
# # Re-run autocogids
# lex = Partial('new_data.tsv', segments='tokens', check=True)
# lex.get_scorer(runs=10000)
# lex.partial_cluster(threshold=0.55, method="lexstat", cluster_method="infomap", ref="autocogids")

# lex.add_entries("old_cogids", 'cogids', lambda x: x, override=True)
# lex.add_entries("cogids", 'autocogids', lambda x: x, override=True)

# # alms = Alignments('autocogids_2.tsv', ref='cogids', transcriptions='tokens')
# alms.align(ref='cogids')

# for item in alms:
#     print(alms[item, 'alignment'])

# alms.output('tsv', filename='autocogids_2')

# ------------------------------------

# alms = reduce_cogids('autocogids_2.tsv', min_refs=3)

# alms = get_copar(alms, ref='cogids')

# for cid in alms.msa["cogids"]:
#     score = np.log(score_cognateset(cid, alms))
#     score_m = np.mean(score)
#     print(cid, score)


# alms = Alignments('autocogids_2.tsv', ref='cogids', transcriptions='tokens')

# check = []
# for i, msa in alms.msa['cogids'].items():
#     unique = defaultdict(list)
#     langs = []
#     # print(msa)
#     for i, entry in enumerate(msa['ID']):
#         # entry = 'ID' in dataset
#         # 'seqs' is form
#         alignment = str(msa['seqs'][i])
#         concept = alms[entry, 'concept']
#         for j, morph in enumerate(' '.join(alms[entry, 'alignment']).split(' + ')):
#             cid = str(alms[entry, 'old_cogids']).split(' ')[j]
#             if morph == alignment and (cid, concept) not in unique:
#                 langs.append([
#                     alms[entry, 'doculect'],
#                     str(alms[entry, 'tokens']).split(' + ')[j],
#                     cid
#                     ])
#                 if cid not in unique[concept]:
#                     unique[concept].append(cid)

#     if len(unique[concept]) > 1:
#         # print(msa)

#         check.append([concept, unique[concept]])

# with open('check.tsv', 'w', encoding='utf8') as file:
#     writer = csv.writer(file, delimiter='\t')
#     writer.writerows(check)
