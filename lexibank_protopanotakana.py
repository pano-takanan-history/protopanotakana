import pathlib
import dataclasses
from edictor.wordlist import fetch_wordlist
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language, Lexeme, Concept
from lingpy import Wordlist
#from pyetymdict.dataset import Language as BaseLanguage, Dataset as BaseDataset


def unmerge(sequence):
    out = []
    for tok in sequence:
        out += tok.split('.')
    return out


@dataclasses.dataclass
class CustomLanguage(Language):
    """Adding new columns to Lexeme."""
    Dataset: Optional[str] = None
    SubGroup: Optional[str] = None


@dataclasses.dataclass
class CustomConcept(Concept):
    Proto_ID: Optional[str] = None


@dataclasses.dataclass
class CustomLexeme(Lexeme):
    Partial_Cognacy: Optional[str] = None
    Alignment: Optional[str] = None
    Morphemes: Optional[str] = None
    Dataset: Optional[str] = None
    GroupedSounds: Optional[str] = None


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
                        "DATASET",
                        "CONCEPTICON_GLOSS"
                    ],
                    base_url='http://lingulist.de/pth/',
                    script_url='get_data.py'
                )
            )

    def cmd_makecldf(self, args):
        # add bib
        # self.schema(args.writer.cldf)
        # self.local_schema(args.writer.cldf)
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
        languages = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"],
                    Dataset=language["Dataset"],
                    SubGroup=language["Subgroup"]
                    )
            languages[language['Name']] = language['ID']

        args.log.info("added languages")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

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
            dataset,
            _
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
                "dataset",
                "concepticon_gloss"
            ),
            desc="cldfify"
        ):
            # Remove tagged entries
            # print(concept, tokens)
            if '*' not in concept:
                if language not in languages:
                    errors.add(("language", language))
                    print('Missing language:', language)
                elif concept not in concepts:
                    errors.add(("concept", concept))
                    print('Missing concept:', concept)

                else:
                    lexeme = args.writer.add_form_with_segments(
                        Language_ID=languages[language],
                        Parameter_ID=concepts[concept],
                        Value=value.strip() if value else form.strip(),
                        Form=form.strip(),
                        Segments=unmerge(tokens),
                        GroupedSounds=tokens,
                        Comment=comment,
                        Cognacy=cognacy,
                        Partial_Cognacy=" ".join([str(x) for x in partial_cognacy]),
                        Alignment=" ".join(alignment),
                        Morphemes=" ".join(morphemes),
                        Dataset=dataset
                    )

                    args.writer.add_cognate(
                        lexeme=lexeme,
                        Cognateset_ID=cognacy,
                        Alignment=alignment,
                        Alignment_Method="false",
                        Alignment_Source="expert"
                        )
