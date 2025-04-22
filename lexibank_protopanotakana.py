import pathlib
from collections import defaultdict
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
            if language["Glottocode"] in ['arao1248', 'araz1236', 'cavi1250', 'esee1248', 'taca1255', 'guar1292', 'reye1240']:
                subgroup = 'Takana'
            elif 'proto' in language["Name"]:
                subgroup = 'Proto'
            else:
                subgroup = 'Pano'
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"],
                    Dataset=language["Dataset"],
                    SubGroup=subgroup
                    )
            languages[language["Glottocode"]] = language["ID"]

        args.log.info("added languages")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

        N = defaultdict()
        M = defaultdict()
        new_id = 1
        new_id2 = 1
        check = defaultdict()
        check_cogid = defaultdict()
        for idx, cogids, cogid, ds in wl.iter_rows("partial_cognacy", "cognacy", 'dataset'):
            new_cogid = []
            new_cogids = []
            if cogids:
                # Set cogid
                if (ds, cogids) not in check_cogid:
                    check_cogid[(ds, cogids)] = new_id2
                    new_id2 += 1
                new_cogid = check_cogid[(ds, cogids)]

                # Set cogids
                cogids = cogids.split(' ')
                for cid in cogids:
                    if (ds, cid) not in check:
                        check[(ds, cid)] = new_id
                        new_id += 1
                new_cogids = [check[(ds, cid)] for cid in cogids]
            else:
                if (ds, cogid) not in check:
                    check[(ds, cogid)] = new_id
                    new_id += 1
                
                if (ds, cogid) not in check_cogid:
                    check_cogid[(ds, cogid)] = new_id2
                    new_id2 += 1
                new_cogid = check_cogid[(ds, cogid)]
                new_cogids = [check[(ds, cogid)]]

            N[idx] = " ".join([str(x) for x in new_cogids])
            M[idx] = new_cogid

        wl.add_entries("partial_cognacy", N, lambda x: x, override=True)
        wl.add_entries("cognacy", M, lambda x: x, override=True)

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
                # print(cognacy, partial_cognacy)
                lexeme = args.writer.add_form_with_segments(
                    Language_ID=languages[language],
                    Parameter_ID=concept,
                    Value=value.strip(),
                    Form=form.strip(),
                    Segments=tokens,
                    Comment=comment,
                    Source=source,
                    Cognacy=cognacy,
                    Partial_Cognacy=partial_cognacy,
                    Alignment=" ".join(alignment),
                    Morphemes=" ".join(morphemes),
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

