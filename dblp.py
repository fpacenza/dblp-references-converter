#!/usr/bin/python3

import requests
import glob
import re
from enum import Enum

import typer
from rich.console import Console
console=Console()
error_console=Console(stderr=True)

# DBLP URLs
DBLP_BASE_URL = 'https://dblp.org/'
DBLP_PUBLICATION_SEARCH_URL = DBLP_BASE_URL + 'search/publ/api?q={title}&format=bibtex'
DBLP_PUBLICATION_BIBTEX = DBLP_BASE_URL + 'rec/{dblp_key}.bib?param={bib_format}'


class BibFormat(Enum):

    condensed = 'condensed'
    standard = 'standard'
    crossref = 'crossref'
    condensed_doi = 'condensed_doi'

    @staticmethod
    def get_bib_url(convert):
        if convert == "condensed":
            return "0"
        elif convert == "standard":
            return "1"
        elif convert == "crossref":
            return "2"
        elif convert == "condensed_doi":
            return "0"
        else:
            assert False
    
    def bib_url(self):
        if self is BibFormat.condensed:
            return "0"
        elif self is BibFormat.standard:
            return "1"
        elif self is BibFormat.crossref:
            return "2"
        elif self is BibFormat.condensed_doi:
            return "0"
        else:
            assert False

    def __str__(self):
        return self.value

            
def find_dblp_key(title, full_bib_entry, output_filename, bib_format):
    post = requests.post(DBLP_PUBLICATION_SEARCH_URL.format(title=title))
    match = re.match(r".*DBLP:(.*),", post.text)
    if (match):
        post = requests.post(DBLP_PUBLICATION_BIBTEX.format(dblp_key=match.group(1), bib_format=BibFormat.get_bib_url(bib_format)))
        with open(output_filename, "a") as f:
            f.writelines(post.text)
        console.print(post.text)
    else:
        error_console.print("No match found for title: " + title)
        with open(output_filename, "a") as f:
            f.writelines(full_bib_entry)
        console.print(full_bib_entry)

def open_file(input_filename, output_filename, bib_format):
    with open(input_filename, "r") as f:
        current_entry = ""
        title = ""
        for line in f.readlines():
            if line.startswith("@"):
                if title != "":
                    find_dblp_key(title, current_entry, output_filename, bib_format)
                current_entry = line
            else: current_entry += line
            match = re.match(r"\s*title\s*=\s*(.*)", line)
            if (match):
                title = match.group(1).replace("{", "").replace("}", "")


def main(input_filename: str=None, output_filename: str=None, bib_format: str="condensed"):
    if output_filename is None:
        output_filename = "output_" + bib_format + ".bib"
    if input_filename is None:
        file_list = glob.glob("*.bib")
        for bib in file_list:
            open_file(bib,output_filename, bib_format)
    else:
        open_file(input_filename,output_filename, bib_format)

if __name__ == "__main__":
    typer.run(main)