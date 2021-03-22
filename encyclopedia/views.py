from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

#adding a class to create a form text input instead of manually setting input field
class SearchForm(forms.Form):
    #adding an input field that will be called in every function for search
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder':'Search Wiki'}))

#adding a class for the create page option to help us input new title and content
class AddNewPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    content = forms.CharField(label= "", widget=forms.Textarea(attrs={'size': 50, 'placeholder': 'Enter your content', 'id': 'new-entry-content', 'style': 'display:flex; width:80%; height:40%; margin-top:15px;' }))

class EditPageFields(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'id': 'edit-entry-title'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'id': 'edit-entry-content','style':'display:flex; width:80%; height:40%; margin-top:15px;'}))
#function for the index page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

#view to show a specific page the user search in url
def entry(request, entry):
    markdowner=Markdown()
    #get the data the user typed in the url
    entrypage= util.get_entry(entry)
    #if it is non existent redirect to error page html
    if entrypage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "title": entry,
            "form":SearchForm()
        })
        # if it is existent redirect the user to the  entry page
    else:
        return render(request,"encyclopedia/entry.html", {
            "entry": markdowner.convert(entrypage),
            "title":entry,
            "form": SearchForm()
        })

# fuction for the search bar
def search(request):
    if request.method == 'POST':
        entries_found= []
        #Get the data entered in the field
        form = SearchForm(request.POST)
        if form.is_valid():
            #getting the Data entered in the search bar
            dataentred = form.cleaned_data["query"]
            #all entries
            entries = util.list_entries()
            for entry in entries:
                #if the data was found
                if dataentred.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    #redirect the user to the entry page
                    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
                #if the letters entered are part of the letters in the entry add it to the empty list we created above
                if dataentred.lower() in entry.lower():
                    entries_found.append(entry)
                
               #default
            return render(request, "encyclopedia/index.html", {
            "entries2": entries_found,
            "search":True,
            "value":dataentred,
            "form": SearchForm()
            
        })

#function for creating entry        
def create(request):
    if request.method == 'POST':
        #get the data from AddNewPage entered and store it in variable
        newentry = AddNewPage(request.POST)

        if newentry.is_valid():
            #extracting the title and content separately and storing them in variables
            title = newentry.cleaned_data['title']
            content = newentry.cleaned_data['content']
            # list of available entries
            available_entries = util.list_entries()
            for entry in available_entries:
                # if the user tries to create an already existing entry display an error message
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/createnew.html",{
                        "form": SearchForm(),
                        "addNewPage": AddNewPage(),
                        "errormessage": "The wiki page you are trying to create already exists..."
                    })
            #adding mark down to entered data the "n" part is to break the title from the body in different lines
            newentrytitle = '#' + title
            newentrybody = "\n" + content

            all_entered_content = newentrytitle + newentrybody
            #saving the entered data in the entries file and by calling save_entry from util
            util.save_entry(title, all_entered_content)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html",{
                "entryTitle" : newentrytitle,
                "entry": newentrybody,
                "form":SearchForm()
            })
    #default
    return render(request, "encyclopedia/createnew.html", {
        "form": SearchForm(),
        "addNewPage": AddNewPage()
    } )

def edit(request, entry):
    
    if request.method == "POST":
        # Get data for the entry so it can be edited
        entrypage = util.get_entry(entry)

        editpage = EditPageFields(initial={'title': entry, 'content': entrypage})

        return render(request, "encyclopedia/edit.html", {
            "form": SearchForm(),
            "editEntry": editpage,
            "entry": entrypage,
            "title": entry
        })
    
def submitEntry(request, entry):
    if request.method == 'POST':
        markdowner=Markdown()
        #get the edited entered data
        edited_post = EditPageFields(request.POST)
        if edited_post.is_valid():
            #get the newely edited valueds both the title and content
            edited_title = edited_post.cleaned_data['title']
            edited_content = edited_post.cleaned_data['content']
            

            if edited_title != entry:
                #using f string to find the entry and if found store it in a variable
                filename = f"entries/{entry}.md"
                if default_storage.exist(filename):
                    default_storage.delete(filename)


            util.save_entry(edited_title, edited_content)
            edited_entry = util.get_entry(edited_title)        
        return render(request, "encyclopedia/entry.html",{
                "title":edited_title,
                "entry": markdowner.convert(edited_entry),
                "form":SearchForm(),            
                "msg_success": "Wiki Page was Successfully updated"
                })           
    
            
            

        