from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entrypage= util.get_entry(entry)
    if entrypage is None:
        return render(request, "ecnyclopedia/nonExistingEntry.html", {
            "entryTitle": entry
        })
    else:
        return render(request,"encyclopedia/entry.html", {
            "entry": entrypage,
            "entryTitle":entry
        })
