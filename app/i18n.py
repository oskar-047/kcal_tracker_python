from __future__ import annotations
import json
from pathlib import Path
from typing import Dict


class _SafeVars(dict):
    def __missing__(self, key):
        return "{" + key + "}"



class I18n:

    # Class constructor
    def __init__(self, data_dir: Path, default_locale: str = "en"):
        self.data_dir = data_dir # Path to lan.json files, all traductions
        self.default_locale = default_locale
        self._catalogs: Dict[str, Dict[str, str]] = {} # Cache for file data

    # Function used to load the text of a selected lan (returns a Dict with all texts)
    def _load(self, locale: str) -> Dict[str, str]:
        # Check if locale (selected lan) is on the _catalogs var, if not, the script loads all locale text from json to the _catalogs var (cache)
        if locale not in self._catalogs:

            path = self.data_dir / f"{locale}.json"

            # Opens the selected locale file with r (read only) and utf-8 (text format) and saves it on f
            with path.open("r", encoding="utf-8") as f:
                # Add a new entry on the _catalogs dictionary and loads all locale text
                self._catalogs[locale] = json.load(f) 

        # Returns the dictionary with the text data of the selected locale
        return self._catalogs[locale]

    # The function that converts a key into the text (using the selected lan)
    def t(self, key: str, locale: str, **vars) -> str:
        catalog = self._load(locale)

        if key in catalog:
            return catalog[key].format_map(_SafeVars(vars))

        default_catalog = self._load(self.default_locale)
        if key in default_catalog:
            return default_catalog[key].format_map(_SafeVars(vars))

        return key


# This function returns a function with a fixed lan used by jinja2 on the templates
def make_t(i18n: I18n, lan):
    return lambda key, **vars: i18n.t(key, lan, **vars)