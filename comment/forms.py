from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import ModelForm
from comment.models import Appointment, Student, Book, Chat, Files, Bird
from django import forms
from django.forms import modelformset_factory


from django.forms import formset_factory


BirdFormSet = modelformset_factory(
    Bird, fields=("common_name", "scientific_name"), extra=1
)



class BukForm(forms.Form):
    name = forms.CharField(
        label='Book Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    )
BookFormset = formset_factory(BukForm, extra=1)





class FileForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf')



class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']



class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['phone_number'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['time'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['time_zone'].widget.attrs = {
            'class': 'form-control col-md-6'
        }

    class Meta:
        model = Appointment
        fields = ['name', 'phone_number', 'time', 'time_zone']





class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['lastname'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['coursename'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        self.fields['yos'].widget.attrs = {
            'class': 'form-control col-md-6'
        }

    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'coursename', 'yos']


# BookApp Form

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'year', 'uploaded_by', 'desc')


class ChatForm(forms.ModelForm):

    class Meta:
        model = Chat
        fields = ('message', )


class BookUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')