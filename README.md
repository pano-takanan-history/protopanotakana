# Template for lexibank-repositories.

## How to cite

If you use these data please cite
- the original source
  > Blum, Frederic. 2024. Template for Workshops on "How to digitize data using the Lexibank-skeleton".
- the derived dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


This repository functions as a template to set up a new lexibank-dataset.

This dataset is licensed under a CC-BY-4.0 license


Conceptlists in Concepticon:
- [Rzymski-2020-1624](https://concepticon.clld.org/contributions/Rzymski-2020-1624)
## Notes

## Description

This repository contains a template that will be used for workshops on 'How to create a LexiBank dataset' and the annotation of such a dataset using EDICTOR (<https://digling.org/edictor/>). The goal is to creating a dataset in Lexibank style (List et al. 2023), which is a specific form of CLDF datasets (Forkel et al. 2018).

Feel free to use und share this repository, or to contribute directly if you see any errors.

### Overview of the repository

The folder is separated into four main folders:

1. `raw/`: Here, the raw data and the bibliography data is stored.
2. `etc/`: This is the folder for metadata, like linking to Glottolog and the orthography profiles.
3. `cldf/`: The final dataset converted to CLDF is stored here.
4. `analysis/`: All additional files related to analyzing the data are given in this folder.

Additionally, there are a couple of files that are relevant to the general workflow:

- `lexibank_template.py`: The script that stores the conversion of the raw data to CLDF
- `metadata.json`: Additional metadata like the conceptlist that is going to be used

#### Raw data

The raw data is a tsv (tab-separated) file that contains, in its most basic form, four columns: the doculect (language), the concept, the form of the word, and the option of adding a comment. We recommend opening tsv-files either with LibreOffice or an editor (like VS Code or vim), but to avoid Microsoft Word, which adds a lot of content in the background.

Along the raw folder, there is a file called `sources.bib` which stores the sources used in the data in bibtex-format.

#### Orthography profiles

The orthography profiles converts all words from one orthography to another. Typically, this means converting the words from a written orthography to IPA. We make use of the CLTS catalog (<https://clts.clld.org/>) to map all graphemes and have automated checks to verify we have no errors in the profile. You can find the errors after running the CLDF conversion in a file called `TRANSCRIPTION.md`.

### Initial workflow

Once you have digitized all your data, you can start with the conversion of the repository. We recommend to run this within a fresh virtual environment. If you do not know how or why and you don't program a lot, you do not need to worry about this and ignore that recommendation for the moment. 

First, open a terminal, clone the repository, switch your working directory to it and run the following code:

```shell
pip install -e .
cldfbench catconfig
```

The last part prompts you to clone local copies of Glottolog, Concepticon, and CLTS. This takes some time and space on your disk, but lets you link your data directly to those reference catalogues.

Once you have done this, you can proceed to create a first version of your orthography profile. You can do so by first running a CLDF conversion, and then create an automatic segmentation based on this first version of the dataset. In the CLDF conversion, you specify the most recent versions of the reference catalogues, to assure your data linking is up-to-date.

```shell
cldfbench lexibank.makecldf lexibank_template.py --concepticon-version=v3.1.0 --glottolog-version=v4.8 --clts-version=v2.2.0
cldfbench lexibank.init_profile lexibank_template.py
```

You can now find a rough version of your orthography profile in `etc/orthography.tsv`. This profile definitely needs improvement, but provides you with a reasonable first impression of your data. You have to use your linguistic knowledge and, if possible, look for descriptive material about the language to find the correct IPA representations for all graphemes.

If you now run the CLDF conversion again, the orthography profile is used to segment the data.

```shell
cldfbench lexibank.makecldf lexibank_template.py --concepticon-version=v3.1.0 --glottolog-version=v4.8 --clts-version=v2.2.0
```

If you have errors in the profile, you will receive an information about BIPA errors in your command line, and find additional information in the `TRANSCRIPTION.md` file. Once you have finalized the orthography profile, run the CLDF conversion a last time to have your dataset ready for analysis.

## Analyzing the data

### Mapping the languages

You can easily create a map of the languages involved in your dataset using the tools of `cldfbench`, given that you have assigned a glottocode to your languages in `etc/languages.tsv`.

```shell
pip install cldfviz[cartopy]
cldfbench cldfviz.map ./ --format=png --markersize 15 --language-labels --language-properties-colormaps=viridis
```

To build a png-image, you might need additional requirements which we cannot cover in this tutorial. Please see the following link if you have any troubles installing the `cartopy`-package: <https://scitools.org.uk/cartopy/docs/latest/installing.html>

You can also try out the html-format which does not require `cartopy`:

```shell
pip install cldfviz
cldfbench cldfviz.map ./ --format=html --markersize 15 --language-labels
```

### Converting the data to EDICTOR

To convert the final CLDF data to EDICTOR, first switch into the `analysis`-directory by running `cd analysis`. There you can find a script called `to_edictor.py`, which contains all the relevant code. It consists of four blocks:

1. Reading in the wordlist
2. Running the automated analysis of cognacy using the LexStat algorithm
3. Aligning the cognate sets (we will see later what this means)
4. Output of the data to `example.tsv`.

You can run the script with the following command: `python to_edictor.py`.

### Analyzing the data in EDICTOR

The output of the previous step can be analyzed using the EDICTOR tool, the heart of our approach to computer-assisted language comparison, developed by Prof. Johann-Mattis List. To do so, please open the following link and load the `example.tsv` as data: <https://digling.org/edictor/>.

We will cover the following steps:

- General overview (Settings, Columns, Ordering, Selecting)
- Cognate annotation
- Alignments
- Sound Correspondences

### Extract sound correspondences

Using LingPy, it is possible to automatically extract the sound correspondences that have been inferred from the cognate sets. To do so, just run the following code:

```shell
pip instal lingrex
python write_patterns.py
```

The script makes use of the LingRex package and creates a file `patterns.tsv` that lets you manually inspect the extracted patterns.

### Distances and Trees

The material in this section is based on the LingPy-Tutorial from Mattis List that you can find [here](https://github.com/lingpy/lingpy-tutorial/tree/v1.1).

We will visualize the distances between languages in two ways: Using a splitstree-network, and using a simple tree. To create them, just run the python script with the following command:

```shell
python networks.py
```

You have created two things:

1. A `.dst`-file that you can load into the [SplitsTree](https://software-ab.cs.uni-tuebingen.de/download/splitstree6/welcome.html) application.
2. An ASCII-tree of the languages in your dataset, using a simple Neighbor-Joining algorithm.

The tree is probably not perfect, but provide you with a first glimpse of the phylogenetic structure underlying the dataset.

### Combining the dataset with Grambank data

Given the linking to reference catalogues, we can easily combine our dataset with other CLDF datasets, such as Grambank (Skirgård et al. 2023). An example for this is given in the Blum et al. (2024) paper. To follow the proposed workflow, it is necessary to first clone the Grambank-repository.

```shell
git clone https://github.com/grambank/grambank
cd grambank
git checkout v1.0.3
cd ../
```

You can now create the SQLite databases that we will use to get a quick access to all the data.

```shell
cldf createdb grambank/cldf/StructureDataset-metadata.json grambank.sqlite3
cldf createdb ../cldf/cldf-metadata.json template.sqlite3
```

You can now open a SQLite instance and run the following queries to load both databases.

```SQL
attach 'template.sqlite3' AS db1;
attach 'grambank.sqlite3' AS db2;
```

Through a join-operation, you can retreive all the data from languages stored in this repository that also have data in Grambank.

```SQL
SELECT
    *
FROM
    db1.LanguageTable AS a
INNER JOIN
    db2.ValueTable AS b
ON
    a.cldf_glottocode = b.cldf_languageReference;
```

## References

Blum, F., Barrientos, C., Zariquiey, R., & List, J.-M. (2024). A comparative wordlist for investigating distant relations among languages in Lowland South America. Scientific Data, 11(1). <https://doi.org/10.1038/s41597-024-02928-7>
Forkel, R., List, J.-M., Greenhill, S. J., Rzymski, C., Bank, S., Cysouw, M., Hammarström, H., Haspelmath, M., Kaiping, G. A., & Gray, R. D. (2018). Cross-Linguistic Data Formats, advancing data sharing and re-use in comparative linguistics. Scientific Data, 5(1), 1–10. <https://doi.org/10.1038/sdata.2018.205>
List, J.-M. (2022). EDICTOR. A web-based tool for creating, editing, and publishing etymological datasets. Max Planck Institute for Evolutionary Anthropology.
List, J.-M., Forkel, R., Greenhill, S. J., Rzymski, C., Englisch, J., & Gray, R. D. (2022). Lexibank, a public repository of standardized wordlists with computed phonological and lexical features. Scientific Data, 9(1), 1–16. <https://doi.org/10.1038/s41597-022-01432-0>
List, J.-M., Forkel, R., & Hill, N. (2022). A New Framework for Fast Automated Phonological Reconstruction Using Trimmed Alignments and Sound Correspondence Patterns. In N. Tahmasebi, S. Montariol, A. Kutuzov, S. Hengchen, H. Dubossarsky, & L. Borin (Eds.), Proceedings of the 3rd Workshop on Computational Approaches to Historical Language Change (pp. 89–96). Association for Computational Linguistics. <https://doi.org/10.18653/v1/2022.lchange-1.9>
Skirgård, H., Haynie, H. J., Blasi, D. E., Hammarström, H., Collins, J., Latarche, J. J., Lesage, J., Weber, T., Witzlack-Makarevich, A., Passmore, S., Chira, A., Maurits, L., Dinnage, R., Dunn, M., Reesink, G., Singer, R., Bowern, C., Epps, P., Hill, J., et al. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. Science Advances, 9(16). <https://doi.org/10.1126/sciadv.adg6175>



## Statistics


![Glottolog: 100%](https://img.shields.io/badge/Glottolog-100%25-brightgreen.svg "Glottolog: 100%")
![Concepticon: 100%](https://img.shields.io/badge/Concepticon-100%25-brightgreen.svg "Concepticon: 100%")
![Source: 0%](https://img.shields.io/badge/Source-0%25-red.svg "Source: 0%")
![BIPA: 70%](https://img.shields.io/badge/BIPA-70%25-orange.svg "BIPA: 70%")
![CLTS SoundClass: 70%](https://img.shields.io/badge/CLTS%20SoundClass-70%25-orange.svg "CLTS SoundClass: 70%")

- **Varieties:** 1
- **Concepts:** 30
- **Lexemes:** 30
- **Sources:** 0
- **Synonymy:** 1.00
- **Invalid lexemes:** 0
- **Tokens:** 178
- **Segments:** 33 (10 BIPA errors, 10 CLTS sound class errors, 23 CLTS modified)
- **Inventory size (avg):** 33.00

## Possible Improvements:



- Entries missing sources: 30/30 (100.00%)

# Contributors

Name | GitHub user | Description | Role |
--- | --- | --- | --- |
Frederic Blum | @FredericBlum | creator | Author |




## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [Wordlist](https://github.com/cldf/cldf/tree/master/modules/Wordlist) at [cldf/cldf-metadata.json](cldf/cldf-metadata.json)