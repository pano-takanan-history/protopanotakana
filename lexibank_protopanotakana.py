import pathlib
from collections import defaultdict
import attr
from clldutils.misc import slug
from edictor.wordlist import fetch_wordlist
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language, Lexeme, Concept
from lingpy import Wordlist


@attr.s
class CustomLanguage(Language):
    """Adding new columns to Lexeme."""
    Dataset = attr.ib(default=None)
    SubGroup = attr.ib(default=None)


@attr.s
class CustomConcept(Concept):
    Proto_ID = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Partial_Cognacy = attr.ib(default=None)
    Alignment = attr.ib(default=None)
    Morphemes = attr.ib(default=None)
    Dataset = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "protopanotakana"
    writer_options = dict(keep_languages=False, keep_parameters=False)
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    concept_class = CustomConcept


    def cmd_download(self, _):
        """Download the most recent data from Edictor."""
        print("updating ...")
        with open(self.raw_dir.joinpath("raw.tsv"), "w", encoding="utf-8") as f:
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
                        "DATASET"
                    ],
                    base_url='http://lingulist.de/pth/',
                    script_url='get_data.py'
                )
            )

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.concepts:
            args.writer.add_concept(
                    ID=concept["ID"],
                    Name=concept["Concept"],
                    Concepticon_ID=concept["Concepticon_ID"],
                    Concepticon_Gloss=concept["Concepticon_Gloss"],
                    Proto_ID=concept["Proto_ID"]
                    )
            concepts[concept["Concept"]] = concept["ID"]

        args.log.info("added concepts")

        # add language
        languages = []
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"],
                    Dataset=language["Dataset"],
                    SubGroup=language["Subgroup"]
                    )
            languages.append(language['ID'])

        args.log.info("added languages")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

        lookup = {}
        # add data
        for (
            _,
            concept,
            language,
            form,
            value,
            tokens,
            cognacy,
            partial_cognacy,
            alignment,
            morphemes,
            comment,
            dataset
        ) in pb(
            wl.iter_rows(
                "concept",
                "doculect",
                "form",
                "value",
                "tokens",
                "cogid",
                "cogids",
                "alignment",
                "morphemes",
                "note",
                "dataset"
            ),
            desc="cldfify"
        ):
            if '*' not in concept:
                idv = (language, concept, "".join(tokens))
                dataset = dataset.split(", ")
                print(dataset)
                print('---')
                if idv not in lookup:
                    lookup[idv] = dataset
                for item in dataset:
                    if item not in lookup[idv]:
                        lookup[idv].append(item)

        # add data
        for (
            _,
            concept,
            language,
            form,
            value,
            tokens,
            cognacy,
            partial_cognacy,
            alignment,
            morphemes,
            comment,
            dataset
        ) in pb(
            wl.iter_rows(
                "concept",
                "doculect",
                "form",
                "value",
                "tokens",
                "cogid",
                "cogids",
                "alignment",
                "morphemes",
                "note",
                "dataset"
            ),
            desc="cldfify"
        ):
            idv = (language, concept, "".join(tokens))
            if idv in lookup:
                if language not in languages:
                    errors.add(("language", language))
                    print('Missing language:', language)
                elif concept not in concepts:
                    errors.add(("concept", concept))
                    print('Missing concept:', concept)

                else:
                    lexeme = args.writer.add_form_with_segments(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=value.strip() if value else form.strip(),
                        Form=form.strip(),
                        Segments=tokens,
                        Comment=comment,
                        Cognacy=cognacy,
                        Partial_Cognacy=" ".join([str(x) for x in partial_cognacy]),
                        Alignment=" ".join(alignment),
                        Morphemes=" ".join(morphemes),
                        Dataset=" ".join(lookup[idv])
                    )

                    args.writer.add_cognate(
                        lexeme=lexeme,
                        Cognateset_ID=cognacy,
                        Alignment=alignment,
                        Alignment_Method="false",
                        Alignment_Source="expert"
                        )

                lookup.pop(idv)
