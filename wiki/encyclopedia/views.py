import markdown2
from random import choice

from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util


class PageForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title"}),
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Write page's content here"}),
    )


# Render homepage
def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


# Edit an entry
def edit(request, entry):
    if entry in util.list_entries():
        # Render the populated form
        return render(
            request,
            "encyclopedia/edit.html",
            {"title": entry, "content": util.get_entry(entry)},
        )
    else:
        return render_error(request, "Page does not exist.")


# Display an entry
def entry(request, entry):
    if entry not in util.list_entries():
        return render_error(request, "Page Not Found.")
    else:
        return render_entry(request, entry)


# Create a new page
def new(request):
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            # Get the title of the page from the form
            title = form.cleaned_data["title"]

            # If an entry with the provided title has not existed, save entry to disk
            if title not in util.list_entries():
                util.save_entry(title, form.cleaned_data["content"])
                return render_entry(request, title)

            # If there is already an entry with the provided title, show an error
            else:
                return render_error(request, "Page already exists!")

        # If the form is not valid, re-render the page with existing info
        else:
            return render(request, "encyclopedia/new.html", {"form": form})

    return render(request, "encyclopedia/new.html", {"form": PageForm()})


# Select a random entry
def random(request):
    entry = choice(util.list_entries())
    return render_entry(request, entry)


# Search entry
def search(request):
    # Get the query from form
    q = request.GET.get("q")

    # If the query matches the name of an encyclopedia entry
    if q.lower() in (entry.lower() for entry in util.list_entries()):
        return render_entry(request, q)

    # Search if the query is a substring of any entry
    matching_list = [e for e in util.list_entries() if q.lower() in e.lower()]
    return render(
        request, "encyclopedia/results.html", {"q": q, "entries": matching_list}
    )


# Update a page
def update(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title in util.list_entries():
            util.save_entry(title, content)
            return render_entry(request, title)
        else:
            render_error(request, "Page does not exist")

    return render(request, "encyclopedia/new.html", {"form": PageForm()})


# Return entry
def render_entry(request, entry):
    return render(
        request,
        "encyclopedia/entry.html",
        {"entry": entry, "content": markdown2.markdown(util.get_entry(entry))},
    )


# Render error page
def render_error(request, error):
    return render(request, "encyclopedia/error.html", {"error": error})
