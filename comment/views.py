from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .forms import CustomUserCreationForm
from .models import Bird,Buk, Song, YouTube, Files, Pelcon,Student, Appointment, Book, User, Feedback, Chat, Ma, Motechapp
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import BirdFormSet, CustomerForm, StudentForm, BookForm, ChatForm, BookUserForm, FileForm, BookFormset
from . import models
import operator
from django.views.generic import ListView, TemplateView
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import PyPDF2
import nltk
import spacy
from spacy.matcher import PhraseMatcher
from django.core.files.storage import FileSystemStorage
import os
import sklearn
import numpy as np
import pandas as pd
import joblib as joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from pandas import read_csv
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import joblib as joblib
from joblib import dump, load
import argparse
import os



def home_music(request):
    return render(request, 'comment/home_music.html')


def make_prediction(request):
    if request.method == 'POST':
        age = request.POST['age']
        gender = request.POST['gender']

        gender = gender.lower()
        age = int(age)

        if gender == 'male':
            gender = 1
        else:
            gender = 0


        model = os.path.join('F:/PYCHARM/DJANGO/ml/model', 'tree.pkl')
        model = joblib.load(model)
        data = [age,gender]
        x = np.array(data).reshape(1,-1)
        x = np.array(x, dtype=np.int64)

        results = model.predict(x)
        print(results[0])
        results = results[0]
        context = {'results':results}
        return render(request, 'comment/home_music.html', context)
    else:
        return render(request, 'comment/home_music.html')




            





class BirdListView(ListView):
    model = Bird
    template_name = "comment/bird_list.html"

class BirdAddView(TemplateView):
    template_name = "comment/add_bird.html"

    def get(self, *args, **kwargs):
        formset = BirdFormSet(queryset=Bird.objects.none())
        return self.render_to_response({'bird_formset': formset})

    # Define method to handle POST request
    def post(self, *args, **kwargs):

        formset = BirdFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("bird_list"))

        return self.render_to_response({'bird_formset': formset})



def create_book_normal(request):
    template_name = 'comment/create_normal.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    Buk(name=name).save()
            # once all books are saved, redirect to book list view
            return redirect('/')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })



def song(request):
    song_list = Song.objects.all().order_by('-id')
    song_list = {'song_list':song_list}
    return render(request, 'comment/song.html', song_list)

def index(request):
   return render(request, 'index.html')









def update_file(request, pk):
    if request.method == 'POST':
        pdf = request.FILES['pdf']
        file_name = request.FILES['pdf'].name

        fs = FileSystemStorage()
        file = fs.save(pdf.name, pdf)
        fileurl = fs.url(file)
        report = file_name


        Book.objects.filter(id = pk).update(pdf = pdf)
        messages.success(request, 'FIle was uploaded successfully!')
        return redirect('blist')
    else:
        return render(request, 'bookapp/update_file.html')




class UpdateFile(SuccessMessageMixin, UpdateView): 
    model = Book
    form_class = FileForm
    template_name = 'bookapp/edit_file.html'
    success_url = reverse_lazy('blist')
    success_message = "Data successfully updated"






# Career Day Views
class CDListFile(generic.ListView):
    model = Files
    template_name = 'comment/list_file.html'
    context_object_name = 'files'
    paginate_by = 6

    def get_queryset(self):
        return Files.objects.order_by('-id')


def upload_pdf(request):
    return render(request, 'comment/upload_pdf.html')


def process_pdf(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        title = request.POST['title']
        pdf = request.FILES['pdf']


        nlp = spacy.load("en_core_web_sm")
        phrase_matcher = PhraseMatcher(nlp.vocab)

        fname = pdf
        pdfFileObj = open(fname, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        # print(pageObj.extractText())
        final_data = pageObj.extractText()
        #print(final_data)


        # Defining Phrase to match
        month = [nlp.make_doc(text) for text in ['March', 'April', 'June', 'September','4']]
        days = [nlp.make_doc(text) for text in ['3', '4', 'June', '2021']]

        phrase_matcher.add("MONTH", None, *month)
        phrase_matcher.add("DAYS", None, *days)

        # Creating a file for writing matched words
        demose = open("media/alpine/test.txt", "w+")

        # Print matching Phrase
        doc = nlp(final_data)
        word_found = ''
        matches = phrase_matcher(doc)
        for match_id, start, end in matches:
            word_found = doc[start:end].text
            with open("test.txt", "a") as myFile:
                myFile.write(str(word_found + "\n"))

        print("Below Is The Month Found :")
        lines = []
        with open('test.txt') as f:
            lines = [line.rstrip() for line in f]
            print(lines)

        print("Print Month ")
        print(lines[0])
        print("")
        month_list = ['January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September','October', 'November', 'December']

        check_month = any(item in lines for item in month_list)

        # print(check)
        month = ''
        if (check_month == True):
            month_found = "Month Is Found"
            print(month_found)
            print(lines[0])
            month = lines[0]
        else:
            month_not_found = "Month Is Not Found"
            print(month_not_found)        

        a = Ma(fullname=fullname, title=title, pdf=pdf, month=month)
        a.save()
        messages.success(request, 'Files Submitted successfully!')
        return redirect('ma')
    else:
        messages.error(request, 'Files was not Submitted successfully!')
        return redirect('upload_pdf')    








account_sid = 'AC46c019ea77dacf86ecea2d4bb44a3ca0'
auth_token = 'eaa7077fa70d51c8397dbb2ee7123ed6'




def home(request):
	like = ['1', '0', '0']
	satisfied = ["Django", "Machine Learning", "Robotics", "None"]
	total_viewer = YouTube.objects.aggregate(Sum("v_watched"))
	print(total_viewer)
	total_viewer = total_viewer.get("v_watched__sum")
	print(total_viewer)


	context = {"like":like, "satisfied":satisfied, "total_viewer":total_viewer}
	return render(request, 'comment/mo.html', context)


"""
def youtube(request):
	if request.method == "POST":
		full_names = request.POST['full_names']
		comment = request.POST['comment']
		v_watched = request.POST['v_watched']
		satisfied = request.POST['satisfied']
		viewer_like = request.POST['viewer_like']
		print("satisfied ? :", satisfied)
		print("Viewer Like : ", viewer_like)

		a = YouTube(full_names=full_names, comment=comment, v_watched=v_watched, satisfied=satisfied, viewer_like=viewer_like)
		a.save()
		messages.success(request, 'Feedback was Submitted successfully!')
		return redirect('home')
	else:
		messages.error(request, 'Failed To Submit Feedback, retry')
		return redirect('home')
"""


def demoses(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        a = Motechapp(firstname=firstname, lastname=lastname)
        a.save()
        return HttpResponse('Ok')


def yourajax(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        a = Motechapp(firstname=firstname, lastname=lastname)
        a.save()
        #return redirect('myajax')
        return HttpResponse('Ok') 


def motech(request):
	names = ["Pelcon", "Crow", "Alpine", "Eagle" ]
	context = {"names":names}
	return render(request, 'comment/motech.html', context)

def pelcon(request):
    return render(request, 'bookapp/home.html')

def youtube(request):
    return render(request, 'bookapp/youtube.html')


def myajax(request):
    return render(request, 'comment/ajax.html')

class FileView(generic.ListView):
    model = Files
    template_name = 'comment/file.html'
    context_object_name = 'files'
    paginate_by = 6

    def get_queryset(self):
    	return Files.objects.order_by('-id')



def uploadForm(request):
	return render(request, 'comment/upload.html')


def uploadFile(request):
    if request.method == 'POST':
        filename = request.POST['filename']
        owner = request.POST['owner']
        pdf = request.FILES['pdf']
        cover = request.FILES['cover']

        a = Files(filename=filename, owner=owner, pdf=pdf, cover=cover)
        a.save()
        messages.success(request, 'Files Submitted successfully!')
        return redirect('files')
    else:
    	messages.error(request, 'Files was not Submitted successfully!')
    	return redirect('form')



class PelconView(generic.ListView):
	model = Pelcon
	template_name = 'comment/pelcon.html'
	context_object_name = 'files'
	paginate_by = 4


	def get_queryset(self):
		return Pelcon.objects.order_by('-id')


def myUpload(request):
	return render(request, 'comment/myUpload.html')



def pelconUpload(request):
	if request.method == 'POST':
		name = request.POST['name']
		owner = request.POST['owner']
		pdf = request.FILES['pdf']
		cover = request.FILES['cover']

		a = Pelcon(name=name, owner=owner, pdf=pdf, cover=cover)
		a.save()
		messages.success(request, 'Files was Submitted successfully')
		return redirect('pelcon')
	else:
		messages.error(request, 'Files was not Submitted successfully')
		return redirect('myupload')



class IndexView(generic.ListView):
	model = Pelcon
	template_name = 'comment/home.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Pelcon.objects.order_by('-id')



def myStudent(request):
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		coursename = request.POST['coursename']
		yos = request.POST['yos']


		a = Student(firstname=firstname, lastname=lastname, coursename=coursename, yos=yos)
		a.save()
		messages.success(request, 'Data Was Submitted Successfully')
		return redirect('crud')
	else:
		messages.error(request, 'Data Was Not Submitted Successfully')
		return redirect('crud')


def editdata(request, pk):
	data = get_object_or_404(Student, id=pk)
	alldata = Student.objects.order_by('-id')

	context = {'data': data, 'qid' : pk, 'getdata' : alldata}
	return render(request, 'comment/home.html', context)


def updatedata(request):
		ed = Student.objects.get(id=request.POST['qid'])

		ed.name=request.POST['name']
		ed.question_text=request.POST['questiontext']
		ed.save()



class AppointmentCreateView(SuccessMessageMixin, CreateView):
    model = Appointment
    form_class = CustomerForm
    success_url = reverse_lazy('alist')
    template_name = 'comment/appointment_form.html'
    success_message = 'Appointment successfully created!.'



class CreateStudent(SuccessMessageMixin, CreateView):
    model = Appointment
    form_class = StudentForm
    template_name = 'comment/add_student.html'
    success_url = reverse_lazy('list')
    success_message = 'Student Was Successfully Added!.'


class ListStudent(generic.ListView):
	model = Student
	template_name = 'comment/crud.html'
	context_object_name = 'students'
	paginate_by = 4

	def get_queryset(self):
		return Student.objects.order_by('-id')



# Appointment Reminder

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'comment/appointment_list.html'
    context_object_name = 'apps'
    paginate_by = 4


    def get_queryset(self):
    	return Appointment.objects.order_by('-id')


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'comment/appointment_detail.html'


class AppointmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Appointment
    form_class = CustomerForm
    success_message = 'Appointment successfully updated.'


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'comment/confirm_delete.html'
    success_url = reverse_lazy('alist')


class AppointmentUpdateView(UpdateView):
    model = Appointment
    template_name = 'comment/appointment_update.html'
    form_class = CustomerForm
    success_message = 'Success: Data was updated.'
    success_url = reverse_lazy('alist')







# BookApp Views
def login(request):
    return render(request, 'comment/login.html')

def register(request):
    return render(request, 'comment/register.html')


def add_book(request):
    return render(request, 'bookapp/add_book.html')

def uadd_book(request):
    return render(request, 'bookapp/add_file.html')    


class UserListView(ListView):
    model = User
    template_name = 'bookapp/me.html'
    context_object_name = 'users'
    paginate_by = 4


    def get_queryset(self):
        return User.objects.order_by('-id')



class BookListView(ListView):
    model = Book
    template_name = 'bookapp/book_list.html'
    context_object_name = 'books'
    paginate_by = 4


    def get_queryset(self):
    	return Book.objects.order_by('-id')


def upload_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username



        a = Book(title=title, author=author, year=year, publisher=publisher,
        	desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success = (request, 'Book Uploaded Successfully')
        return redirect('blist')
    else:
        return redirect('add_book')


def psearch(request):
    query = request.GET['query']
    print(type(query))




    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashboard')
    else:
                a = data

                # Searching for Books
                qs1 =models.Book.objects.filter(id__iexact=a).distinct()
                qs2 =models.Book.objects.filter(id__exact=a).distinct()
                qs3 =models.Book.objects.filter(id__iexact=a).distinct()
                qs4 =models.Book.objects.filter(id__exact=a).distinct()
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()




                files = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res




                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)
   


                if files:
                    return render(request,'bookapp/result.html',{'files':files,'word':word})
                return render(request,'bookapp/result.html',{'files':files,'word':word})



def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else:    
                return redirect('blist')                 
        else:
            messages.info(request,"Invalid username or password")
            return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')






class ManageBook(ListView):
    model = Book
    template_name = 'dashboard/manage_books.html'
    context_object_name = 'books'
    paginate_by = 4


    def get_queryset(self):
        return Book.objects.order_by('-id')


def registerUser(request):
    if request.method == 'POST':
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            
            a = User(username=username, email=email, password=password, is_publisher=True)
            a.save()
            messages.success(request, 'Account was created successfully!')
            return redirect('login')
    else:
        messages.error(request, 'Registration Fail, Try Again Later')
        return redirect('register')

# Publisher Views
def delete_request(request):
    return render(request, 'bookapp/delete_request.html')

def send_feedback(request):
    return render(request, 'bookapp/send_feedback.html')

def about(request):
    return render(request, 'bookapp/about.html')


def delete_book_request(request):
    if request.method == 'POST':
        book_id = request.POST['delete_request']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        user_request = "User" + " " + username + " " + "want to delete book with id " + book_id


        a = Feedback(delete_request=user_request)
        a.save()
        messages.success = (request, 'Request Was Sent Successfully')
        return redirect('delete_request')
    else:
        messages.error(request, 'Request Was Not Sent Successfully')
        return redirect('delete_request')



def send_feedback_user(request):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        user_feedback = "User" + " " + username + " " + "says " + feedback


        a = Feedback(feedback=user_feedback)
        a.save()
        messages.success = (request, 'Request Was Sent Successfully')
        return redirect('send_feedback')
    else:
        messages.error(request, 'Request Was Not Sent Successfully')
        return redirect('send_feedback')







# Librarian Views
def librarian(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()


    context = {'book':book, 'user':user}
    return render(request, 'librarian/home.html', context)

def ladd_book(request):
    return render(request, 'librarian/add_book.html')


def lupload_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username


        a = Book(title=title, author=author, year=year, publisher=publisher,
            desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success = (request, 'Book Uploaded Successfully')
        return redirect('llbook')
    else:
        messages.error(request, 'Book Was Not Uploaded Successfully')
        return redirect('ladd_book')




class LListBook(ListView):
    model = Book
    template_name = 'librarian/book_list.html'
    context_object_name = 'books'
    paginate_by = 5


    def get_queryset(self):
        return Book.objects.order_by('-id')


class LViewBook(DetailView):
    model = Book
    template_name='librarian/book_detail.html'


class LManageBook(ListView):
    model = Book
    template_name = 'librarian/manage_books.html'
    context_object_name = 'books'
    paginate_by = 5


    def get_queryset(self):
        return Book.objects.order_by('-id')

class LEditBook(SuccessMessageMixin, UpdateView): 
    model = Book
    form_class = BookForm
    template_name = 'librarian/edit_book.html'
    success_url = reverse_lazy('lmbook')
    success_message = "Data successfully updated"


class LDBook(SuccessMessageMixin, DeleteView):
    model = Book
    template_name='librarian/confirm_delete.html'
    success_url = reverse_lazy('lmbook')
    success_message = "Data successfully deleted"


class LibDelete(SuccessMessageMixin, DeleteView):
    model = Book
    template_name='librarian/confirm_delete2.html'
    success_url = reverse_lazy('librarian')
    success_message = "Data successfully deleted"



class LChatList(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'librarian/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('posted_at')


class LChatCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = ChatForm
    model = Chat
    template_name = 'librarian/chat_form.html'
    success_url = reverse_lazy('lall_chat')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LDeleteRequest(ListView):
    model = Feedback
    template_name = 'librarian/delete_request.html'
    context_object_name = 'feedbacks'
    paginate_by = 4


    def get_queryset(self):
        return Feedback.objects.order_by('-id')


def lsearch(request):
    query = request.GET['query']
    print(type(query))




    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('librarian')
    else:
                a = data

                # Searching for It
                qs1 =models.Book.objects.filter(id__iexact=a).distinct()
                qs2 =models.Book.objects.filter(id__exact=a).distinct()
                qs3 =models.Book.objects.filter(id__iexact=a).distinct()
                qs4 =models.Book.objects.filter(id__exact=a).distinct()
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()




                files = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res




                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)
   


                if files:
                    return render(request,'librarian/result.html',{'files':files,'word':word})
                return render(request,'librarian/result.html',{'files':files,'word':word})




# Group chat view
class ChatCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = ChatForm
    model = Chat
    template_name = 'bookapp/chat_form.html'
    success_url = reverse_lazy('all_chat')



    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'bookapp/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('posted_at')



# Admin views
class ALViewBook(DetailView):
    model = Book
    template_name='dashboard/book_detail.html'


class AEditBook(SuccessMessageMixin, UpdateView): 
    model = Book
    form_class = BookForm
    template_name = 'dashboard/edit_book.html'
    success_url = reverse_lazy('mbook')
    success_message = "Data successfully updated"


class AEditUser(SuccessMessageMixin, UpdateView): 
    model = User
    form_class = BookUserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('users')
    success_message = "Data successfully updated"


class ADBook(SuccessMessageMixin, DeleteView):
    model = Book
    template_name='dashboard/confirm_delete.html'
    success_url = reverse_lazy('mbook')
    success_message = "Data successfully deleted"


class ADUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete2.html'
    success_url = reverse_lazy('users')
    success_message = "Data successfully deleted"



class ADeleteRequest(ListView):
    model = Feedback
    template_name = 'dashboard/delete_request.html'
    context_object_name = 'feedbacks'
    paginate_by = 4


    def get_queryset(self):
        return Feedback.objects.order_by('-id')

class AChatList(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'dashboard/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('posted_at')


class AChatCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = ChatForm
    model = Chat
    template_name = 'dashboard/chat_form.html'
    success_url = reverse_lazy('aall_chat')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'

def create_user_form(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}

    return render(request, 'dashboard/add_user.html', choice)



@login_required
def dashboard(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()


    context = {'book':book, 'user':user}
    return render(request, 'dashboard/home.html', context)





class ABookListView(ListView):
    model = Book
    template_name = 'dashboard/book_list.html'
    context_object_name = 'books'
    paginate_by = 4


    def get_queryset(self):
        return Book.objects.order_by('-id')


def create(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("User Type")
            print(userType)
            if userType == "Publisher":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_publisher=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            elif userType == "Librarian":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_librarian=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')    
            else:
                messages.success(request, 'Member was not created')
                return redirect('users')
    else:
        return redirect('create_user')


class AdminDelete(SuccessMessageMixin, DeleteView):
    model = Book
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Data successfully deleted"



class UserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')


def asearch(request):
    query = request.GET['query']
    print(type(query))




    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashboard')
    else:
                a = data

                # Searching for Books
                qs1 =models.Book.objects.filter(id__iexact=a).distinct()
                qs2 =models.Book.objects.filter(id__exact=a).distinct()
                qs3 =models.Book.objects.filter(id__iexact=a).distinct()
                qs4 =models.Book.objects.filter(id__exact=a).distinct()
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()




                files = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res




                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)
   


                if files:
                    return render(request,'dashboard/result.html',{'files':files,'word':word})
                return render(request,'dashboard/result.html',{'files':files,'word':word})


def aupload_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username


        a = Book(title=title, author=author, year=year, publisher=publisher,
            desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success = (request, 'Book Uploaded Successfully')
        return redirect('albook')
    else:
        messages.error(request, 'Book Was Not Uploaded Successfully')
        return redirect('add_book')