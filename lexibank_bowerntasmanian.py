from pathlib import Path

import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import Language as BaseLanguage
from pylexibank import FormSpec


@attr.s
class CustomLanguage(BaseLanguage):
    RegionCode = attr.ib(default=None)
    Region = attr.ib(default=None)
    MacroRegion = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "bowerntasmanian"
    language_class = CustomLanguage

    form_spec = FormSpec(
        brackets={"[": "]", "{": "}", "(": ")", "‘": "’"},
        separators=";/,",
        missing_data=("?", "-", "--"),
        strip_inside_brackets=True,
    )
    
    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        args.writer.add_sources()
        
        languages = args.writer.add_languages(lookup_factory="Name")
        
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory="Name"
        )
        # manually patch a few concepts because of « (in concepticon) = " in data
        concepts['blue-tongued lizard ("goanna")'] = '49_bluetonguedlizardgoanna'
        concepts['trunk ("tree")'] = '577_trunktree'
        
        for i, row in enumerate(self.raw_dir.read_csv('data.tsv', dicts=True, delimiter="\t"), 1):
            # skip rows with undefined master glosses as these seem to be
            # unusual/unidentified forms.
            if not row['MasterGloss']:
                continue
            
            # skip these unknown languages
            if row['region'] in ("", "unknown15"):
                continue
            
            lang = languages.get(row['region'])

            if lang is None:
                raise ValueError('Unknown language %d: %s' % (i, row['region']))
            
            args.writer.add_forms_from_value(
                Local_ID=row['recordid'],
                Language_ID=lang,
                Parameter_ID=concepts[row['MasterGloss']],
                Value=row['originalform'],
                Source=["Bowern2012"],
            )


