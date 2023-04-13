from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from markdown2 import markdown
from django.contrib import messages

from . import util

import random


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'})
    )

class EntryForm(forms.Form):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter title'})
    )
    contents = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"placeholder": "Enter contents", "style": "resize:none;height:400px;"})
    )

def index(request):
    """ Shows list of all entries. Clicking on an entry redirects to that entry's page"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def entry(request, entry):
    """
    Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, s
    hould render a page that displays the contents of that encyclopedia entry.
    """
    # The view should get the content of the encyclopedia entry by calling the appropriate util function.
    content = util.get_entry(entry)

    # If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
    if content == None:
        return render(request, "encyclopedia/entry_error.html", {
            "entry": entry,
            "search_form": SearchForm()
        })

    # If the entry does exist, the user should be presented with a page that displays the content of the entry.
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "content": markdown(content),
            "search_form": SearchForm()
        })


def search(request):
    """
    Allow the user to type a query into the search box 
    in the sidebar to search for an encyclopedia entry.
    """

    if request.method == "POST":
        form = SearchForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the query from the 'cleaned' version of form data
            query = form.cleaned_data["query"].lower()

            # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
            if util.get_entry(query) != None:
                return redirect("encyclopedia:entry", entry=query)

            # If the query does not match the name of an encyclopedia entry,
            # the user should instead be taken to a search results page that displays a list of all encyclopedia entries
            # that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
            # Clicking on any of the entry names on the search results page should take the user to that entry’s page.
            else:

                search_results = [
                    entry for entry in util.list_entries() if query in entry.lower()]

                return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "search_results": search_results,
                    "search_form": SearchForm()
                })

        return redirect("encyclopedia:index")

    else:
        return redirect("encyclopedia:index")

def random_page(request):
    """Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry."""
    return redirect("encyclopedia:entry", entry=random.choice(util.list_entries()))


def new_page(request):
    """Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry."""
    if request.method == "POST":
        form = EntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the title and contents from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            contents = form.cleaned_data["contents"]

            # If an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
            if util.get_entry(title) != None:
                messages.error(request, "An entry with this title already exists")
                return redirect("encyclopedia:new_page")


            # Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
            else:
               with open(f"entries/{title}.md", "a") as file:
                file.write(f"#{title}\n")
                file.write(contents)
                return redirect("encyclopedia:entry", entry=title)



    else:
        return render(request, "encyclopedia/new_page.html", {
            "entry_form": EntryForm(),
            "search_form": SearchForm()})
