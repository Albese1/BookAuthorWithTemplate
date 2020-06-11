from django.shortcuts import render, HttpResponse, redirect
from App_One.models import *
# Create your views here.

def viewbook(request, bookid):
    if request.method == "POST":
        theBook = Book.objects.get(id=bookid)
        theAuthorThatWeWantToAddHere = Author.objects.get(id=int(request.POST["author"]))
        theBook.authors.add(theAuthorThatWeWantToAddHere)
        return redirect('/books/' + str(bookid))
    try:
        theBook = Book.objects.get(id=bookid)
    except:
        return HttpResponse("There is no such book with that id " + str(bookid))
    context = {
        "id": theBook.id,
        "title": theBook.title,
        "desc": theBook.desc,
        "authors": theBook.authors.all(),
        "otherAuthors": Author.objects.all().exclude(id__in=Book.objects.get(id=bookid).authors.all())
    }
    return render(request, "books/view.html", context)

def books(request):
    if request.method == "POST":
        if not request.POST["title"]:
            return HttpResponse("Title field should be filled")
        elif len(request.POST["title"]) > 255:
            return HttpResponse("Title should not be longer than 255 characters")
        elif not request.POST["desc"]:
            return HttpResponse("Desc field should be filled")
        Book.objects.create(title=request.POST["title"], desc=request.POST["desc"])
        return redirect('/')
    context = {
        'books': Book.objects.all()
    }
    return render(request, "books/index.html", context)

def viewauthor(request, authorid):
    if request.method == "POST":
        theAuthor = Author.objects.get(id=authorid)
        TheBookWeWantToAddToThisAuthor = Book.objects.get(id=int(request.POST["book"]))
        theAuthor.books.add(TheBookWeWantToAddToThisAuthor)
        return redirect('/authors/' + str(authorid))
    try:
        theAuthor = Author.objects.get(id=authorid)
    except:
        return HttpResponse("There is no such author with that id " + str(authorid))
    context = {
        "id": theAuthor.id,
        "first_name": theAuthor.first_name,
        "last_name": theAuthor.last_name,
        "notes": theAuthor.notes,
        "books": theAuthor.books.all(),
        "otherBooks": Book.objects.all().exclude(id__in=Author.objects.get(id=authorid).books.all())
    }
    return render(request, "authors/view.html", context)

def authors(request):
    if request.method == "POST":
        if not request.POST["first_name"]:
            return HttpResponse("First name field should be filled")
        if not request.POST["last_name"]:
            return HttpResponse("First name field should be filled")
        elif len(request.POST["first_name"]) > 45:
            return HttpResponse("First name should not be longer than 255 characters")
        elif len(request.POST["last_name"]) > 45:
            return HttpResponse("Last name should not be longer than 255 characters")
        elif not request.POST["notes"]:
            return HttpResponse("Notes field should be filled")
        Author.objects.create(first_name = request.POST["first_name"], last_name=request.POST["last_name"], notes=request.POST["notes"])
        return redirect('/')
    context = {
        'authors': Author.objects.all()
    }
    return render(request, "authors/index.html", context)