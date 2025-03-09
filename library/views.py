from django.shortcuts import render, get_object_or_404
from . import forms,models
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import News
from .forms import NewsForm
from django.urls import reverse
from .models import Book


# Create your views here.
# views.py
from django.shortcuts import render
from .models import Blog, Book, News, LibraryDetails

def home_view(request):
    # Fetching blogs, books, news, and library details
    blogs = Blog.objects.filter(is_approved=True)  # Only fetch blogs that are approved
    print(blogs)  # Fetch all blogs (but now filtered to approved ones)
    
    books = Book.objects.all()  # If you're displaying books, fetch them as well
    news_items = News.objects.all().order_by('-created_at')[:4]  # Latest 4 news items
    details = LibraryDetails.objects.latest('id')  # Latest library details

    return render(request, 'index.html', {
        'blogs': blogs,
        'books': books,
        'news_items': news_items,
        'details': details
    })





    
from django.shortcuts import render, redirect
from .models import Blog

def afterlogin_view(request):
    # Fetching all the pending blogs (where is_approved is False)
    pending_blogs = Blog.objects.filter(is_approved=False)

    return render(request, 'adminafterlogin.html', {'pending_blogs': pending_blogs})


def book_view(request):
    return render(request,'book.html')

def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST, request.FILES)  # Include request.FILES to handle image upload
        if form.is_valid():
            book = form.save()  # Save the book and capture the instance
            messages.success(request, 'Book added successfully!')  # Add success message
            return redirect('/viewbook')  # Redirect to the viewbook page
    return render(request, 'addbook.html', {'form': form})

def viewbook_view(request):
    books=models.Book.objects.all()
    print(books)
    return render(request,'viewbook.html',{'books':books})


def update_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = forms.BookForm(instance=book)
    if request.method == 'POST':
        form = forms.BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect(reverse('viewbook'))
    return render(request, 'updatebook.html', {'form': form, 'book': book})

def delete_book_view(request,pk):
    services = models.Book.objects.get(id=pk)
    services.delete()
    return redirect('viewbook')

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_news')
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form})

def view_news(request):
    news_items = News.objects.all().order_by('-created_at')
    return render(request, 'view_news.html', {'news_items': news_items})

def news_view(request):
    return render(request,'news.html')


def update_news(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('view_news')
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'add_news.html', {'form': form})

# Delete a news item
def delete_news(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news_item.delete()
        return redirect('view_news')
    return render(request, 'delete_news.html', {'news_item': news_item})


from .models import LibraryDetails
from .forms import LibraryDetailsForm

def library_details(request):
    return render(request,'librarydetails.html')


def add_library_details(request):
    if request.method == 'POST':
        form = LibraryDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_library_details')
    else:
        form = LibraryDetailsForm()
    return render(request, 'add_library_details.html', {'form': form})

def view_library_details(request):
    details = LibraryDetails.objects.latest('id')  # Fetch the latest entry
    return render(request, 'view_library_details.html', {'details': details})




from .forms import UserForm

def user_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userlogin')
        else:
            print(form.errors)  # This will print the errors in the terminal/console
    else:
        form = UserForm()

    return render(request, 'user.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import userdetails

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = userdetails.objects.get(username=username)

            if user.password == password:  # In a real-world scenario, use password hashing!
                request.session['user_id'] = user.id  # Store user ID in the session
                messages.success(request, f"Welcome, {username}!")
                return redirect('userdashboard')  
            else:
                messages.error(request, "Incorrect password.")
        except userdetails.DoesNotExist:
            messages.error(request, "Username does not exist.")
    
    # Pass user_id from session to the template
    user_id = request.session.get('user_id', None)
    return render(request, 'userlogin.html', {'user_id': user_id})



def userdashboard(request):
    return render(request, 'userdashboard.html')


from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm

def blog_create(request):
    if request.method == 'POST':  # If the form has been submitted
        form = BlogForm(request.POST, request.FILES)  # Include request.FILES to handle image uploads
        if form.is_valid():
            blog = form.save(commit=False)  # Save the form data but don't commit yet
            blog.is_approved = False  # Set blog approval status to False (not approved)
            blog.save()  # Save the new blog post to the database
            return redirect('userdashboard')  # Redirect to the user dashboard after saving the blog
    else:
        form = BlogForm()  # Display the empty form when the page is first loaded

    return render(request, 'blog_form.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog

from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog

def approve_blog(request, blog_id):
    if request.user.is_superuser:  # Check if the user is an admin
        blog = get_object_or_404(Blog, id=blog_id)  # Fetch the blog by ID
        blog.is_approved = True  # Set the blog as approved
        blog.save()  # Save the blog with the updated approval status
        
        pending_blogs = Blog.objects.filter(is_approved=False)
        
        return render(request, 'adminafterlogin.html', {'pending_blogs': pending_blogs})
    else:
        return redirect('userlogin')  # Redirect to login if the user is not an admin

def viewblog_view(request):
    # Filter only approved blogs
    blogs = Blog.objects.filter(is_approved=True)
    return render(request, 'index.html', {'blogs': blogs})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import userdetails
from django.contrib.auth.hashers import make_password
def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            # Get user by username
            user = userdetails.objects.get(username=username)
            # Pass user_id in the redirect instead of username
            return redirect('reset_password', user_id=user.id)
        except userdetails.DoesNotExist:
            return HttpResponse("User not found.")

    return render(request, 'forgot_password.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import userdetails

def reset_password(request, user_id):
    try:
        user = userdetails.objects.get(id=user_id)  # Fetch user by ID

        if request.method == 'POST':
            new_password = request.POST['new_password']
            user.password = new_password  # Directly setting the new password
            user.save()  # Save the user object with the new password

            messages.success(request, "Your password has been successfully updated.")
            return redirect('userlogin')  # Redirect to login page after successful reset

        return render(request, 'reset_password.html', {'user': user})

    except userdetails.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('userlogin')  # Redirect if the user does not exist

