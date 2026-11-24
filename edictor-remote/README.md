# Opening the data in EDICTOR

## Installing packages

Please follow along the tutorial here: <https://github.com/digling/edictor/blob/master/README.md>

Do not hesitate to contact me in case you have questions or something in the tutorial is not working as intended.

Once you have installed EDICTOR3, simply run the `edictor server` command within this folder and enter your username and password.

## Creating the SQLite for Upload

`edictor wordlist --name=protopanotakana --namespace='{"language_name": "doculect", "concept_name": "concept","value": "value", "form":"form", "segments": "tokens","comment": "note"}' --addon="language_subgroup:subgroup","cognacy:cogid","partial_cognacy:cogids","alignment:alignment","dataset:dataset","concept_concepticon_gloss:concepticon_gloss"`

## Creating wordlist for BEAST analysis

`edictor wordlist --name=protopanotakana --namespace='{"language_name": "doculect", "concept_name": "concept","value": "value", "form":"form", "segments": "tokens","comment": "note"}' --addon="cognacy:cogid"`

`python -c "from lingpy import *; from lingpy.convert.strings import write_nexus; wl = Wordlist('protopanotakana.tsv'); write_nexus(wl, mode='beastwords', filename='ppt.nex', ref='cogid')"`
