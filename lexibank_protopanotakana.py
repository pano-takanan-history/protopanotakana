from collections import defaultdict
import pathlib
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from lingpy import Wordlist


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "template"

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concepts[concept.concepticon_gloss] = idx

        args.log.info("added concepts")

        # add language
        languages = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"]
                    )
            languages[language["ID"]] = language["Name"]
        args.log.info("added languages")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("data.tsv")))

        # add data
        for (
            idx,
            language,
            concept,
            value,
            note
        ) in pb(
            wl.iter_rows(
                "doculect",
                "concept",
                "form",
                "note"
            ),
            desc="cldfify"
        ):
            if value != "":
                if language not in languages:
                    errors.add(("language", language))
                elif concept in concepts:
                    # lexeme = args.writer.add_form_with_segments(
                    args.writer.add_forms_from_value(
                        Parameter_ID=concepts[concept],
                        Language_ID=languages[language],
                        Value=value.strip(),
                        Comment=note,
                        Source=''
                    )
