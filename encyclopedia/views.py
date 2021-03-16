from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

#adding to create a form in search to manipulate
class SearchForm(forms.Form):
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder':'Search Wiki'}))

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
        form = SearchForm(request.POST)
        if form.is_valid():
            #getting the Data entered in the search bar
            dataentred = form.cleaned_data["query"]
            entries = util.list_entries()
            for entry in entries:
                if dataentred.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

            if ispresent:
                markdowner = Markdown()
                return render(request, "encyclopedia/entry.html",{
                    'content': markdowner.convert(content),
                    "form": form,
                    'entryTitle': data
                })

    return render(request, "encyclopedia/index.html",{
        "form": SearchForm()
    })       
