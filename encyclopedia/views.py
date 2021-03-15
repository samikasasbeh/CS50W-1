from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms

#adding to create a form in search to manipulate
class SearchForm(forms.Form):
    query = forms.CharField(label="Search here")

#Default landing page view
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#view to show a specific page the user search in url
def entry(request, entry):
    markdowner=Markdown()
    entrypage= util.get_entry(entry)
    if entrypage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": entry
        })
    else:
        return render(request,"encyclopedia/entry.html", {
            "entry": markdowner.convert(entrypage),
            "entryTitle":entry
        })

# to view the pages the user searched for 
def search(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            dataentry = form.cleaned_data["query"]
            for entry in util.list_entries():
                if dataentry == entry:
                    content = util.get_entry(dataentry)
                    ispresent = True

            if ispresent:
                markdowner = Markdown()
                return render(request, "encyclopedia/entry.html",{
                    'content': markdowner.convert(content),
                    "form": form,
                    'entryTitle': data
                })

    return render(request, "encyclopedia/entry.html",{
        "form": SearchForm()
    })       
