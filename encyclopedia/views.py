from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

#adding to create a form in search to manipulate
class SearchForm(forms.Form):
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder':'Search Wiki'}))

class AddNewPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    content = forms.CharField(label= "", widget=forms.Textarea(attrs={'size': 50, 'placeholder': 'Enter your content', 'id': 'new-entry-content', 'style': 'display:flex; width:80%; height:40%; margin-top:15px;' }))
#Default landing page view


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })
#view to show a specific page the user search in url
def entry(request, entry):
    markdowner=Markdown()
    entrypage= util.get_entry(entry)
    if entrypage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": entry,
            "form":SearchForm()
        })
    else:
        return render(request,"encyclopedia/entry.html", {
            "entry": markdowner.convert(entrypage),
            "entryTitle":entry,
            "form": SearchForm()
        })

# to view the pages the user searched for 
def search(request):
    if request.method == 'POST':
        entries_found= []
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
                
                if dataentred.lower() in entry.lower():
                    entries_found.append(entry)
                
                #if dataentred.lower() not in entry.lower():
                   # return render(request , "encyclopedia/nonExistingEntry.html", {
                        #"entryTitle": dataentred,
                        #"form": SearchForm
                    #})
            return render(request, "encyclopedia/index.html", {
            "entries2": entries_found,
            "search":True,
            "value":dataentred,
            "form": SearchForm()
            
        })

        
def create(request):
    if request.method == 'POST':
        newentry = AddNewPage(request.POST)

        if newentry.is_valid():
            title = newentry.cleaned_data['title']
            content = newentry.cleaned_data['content']
            # list of available entries
            available_entries = util.list_entries()
            for entry in available_entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/createnew.html",{
                        "form": SearchForm(),
                        "addNewPage": AddNewPage(),
                        "error_message": "The entry you are trying to create already exists"
                    })
            #adding mark down to entered data
            newentrytitle = '#' + title
            newentrybody = "\n" + content

            all_entered_content = newentrytitle + newentrybody
            util.save_entry(title, all_entered_content)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html",{
                "entryTitle" : title,
                "entry": entry,
                "form":SearchForm()
            })

    return render(request, "encyclopedia/createnew.html", {
        "form": SearchForm(),
        "addNewPage": AddNewPage()
    } )
        