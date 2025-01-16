from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html') # This is the view that will be rendered when the user visits the home page.

def contact(request):
    return render(request, 'contact.html') # This is the view that will be rendered when the user visits the contact page.

def about(request):
    return render(request, 'about.html') # This is the view that will be rendered when the user visits the about page.