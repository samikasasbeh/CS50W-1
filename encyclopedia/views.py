from django.shortcuts import render
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner=Markdown()
    entrypage= util.get_entry(entry)
    if entrypage is None:
        return render(request, "ecnyclopedia/nonExistingEntry.html", {
            "entryTitle": entry
        })
    else:
        return render(request,"encyclopedia/entry.html", {
            "entry": markdowner.convert(entrypage),
            "entryTitle":entry
        })
