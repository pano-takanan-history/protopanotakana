import pathlib
import attr
from clldutils.misc import slug
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
    Borrowing = attr.ib(default=None)
    Dataset = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "protopanotakana"
    writer_options = dict(keep_languages=False, keep_parameters=False)
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    concept_class = CustomConcept

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
            concepts[concept["ID"]] = concept["ID"]

        args.log.info("added concepts")

        # add language
        languages = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"],
                    Dataset=language["Dataset"],
                    SubGroup=language["SubGroup"]
                    )
            languages[language["ID"]] = language["ID"]

        args.log.info("added languages")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

        N = {}
        for idx, cogids, morphemes in wl.iter_rows("partial_cognacy", "morphemes"):
            new_cogids = []
            if morphemes:
                for cogid, morpheme in zip(cogids, morphemes):
                    if not morpheme.startswith("_"):
                        new_cogids += [cogid]
            else:
                new_cogids = [c for c in cogids if c]

            if new_cogids == []:
                new_cogids = [c for c in cogids if c]

            N[idx] = " ".join([str(x) for x in new_cogids])
        wl.add_entries("partial_cognacy", N, lambda x: x, override=True)
        wl.renumber("partial_cognacy")  # creates numeric cogid

        # add data
        for (
            idx,
            language,
            concept,
            value,
            form,
            tokens,
            comment,
            source,
            cognacy,
            partial_cognacy,
            alignment,
            morphemes,
            borrowing,
            dataset
        ) in pb(
            wl.iter_rows(
                "doculect",
                "concept",
                "value",
                "form",
                "segments",
                "comment",
                "source",
                "cognacy",
                "partial_cognacy",
                "alignment",
                'morphemes',
                'borrowing',
                'dataset'
            ),
            desc="cldfify"
        ):
            if language not in languages:
                errors.add(("language", language))
                print(language)
            elif concept not in concepts:
                errors.add(("concept", concept))
                print(concept)
            else:
                lexeme = args.writer.add_form_with_segments(
                    Language_ID=language,
                    Parameter_ID=concept,
                    Value=value.strip(),
                    Form=form.strip(),
                    Segments=tokens,
                    Comment=comment,
                    Source=source,
                    Cognacy=cognacy,
                    Partial_Cognacy=partial_cognacy,
                    Alignment=alignment,
                    Morphemes=morphemes,
                    Borrowing=borrowing,
                    Dataset=dataset
                )

                args.writer.add_cognate(
                    lexeme=lexeme,
                    Cognateset_ID=cognacy,
                    Alignment=alignment,
                    Alignment_Method="false",
                    Alignment_Source="expert"
                    )

