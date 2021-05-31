from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from django.contrib.auth.models import User
from timezone_field import TimeZoneField
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.forms import modelformset_factory


class Bird(models.Model):
    common_name = models.CharField(max_length=250)
    scientific_name = models.CharField(max_length=250)
    
    def __str__(self):
      return self.common_name


# Accessing ForeignKey Inside HTML template
class Artist(models.Model):
   name = models.CharField(max_length=100, unique=True)
   slug = models.SlugField(max_length=100, unique=True,
            help_text='Uniq value for artist page URL, created from name')
   birth_name = models.CharField(max_length=100, blank=True)



class Song(models.Model):
   title = models.CharField(max_length=255)  
   slug = models.SlugField(max_length=255, unique=True,
            help_text='Unique value for product page URL, create from name.')
   youtube_link = models.URLField(blank=False)
   artists = models.ManyToManyField(Artist)


















# Career Day Model
class Ma(models.Model):
    fullname = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    pdf = models.FileField(upload_to='ma/')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)





#User = get_user_model()
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)


    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Files(models.Model):
    filename = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')
    cover = models.ImageField(upload_to='store/covers/', null=True, blank=True)

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)



class YouTube(models.Model):
    full_names = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)
    v_watched = models.IntegerField(null=True, blank=True)
    satisfied = models.BooleanField(default=False)
    viewer_like = models.CharField(blank=True, max_length=100)



class Pelcon(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')
    cover = models.ImageField(upload_to='store/covers/')


    def __str__(self):
        return self.name


class Motechapp(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)


    def __str__(self):
        return self.firstname        



class Student(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    coursename = models.CharField(max_length=100)
    yos = models.CharField(max_length=100)


    def __str__(self):
        return self.firstname


class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='UTC')

    # Additional fields not visible to users
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('alist', args=[str(self.id)])    


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)
    uploaded_by = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    pdf = models.FileField(upload_to='')
    cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)




class Buk(models.Model):

    name = models.CharField(max_length=255)
    isbn_number = models.CharField(max_length=13)

    class Meta:
        db_table = 'buk'

    def __str__(self):
        return self.name

class Feedback(models.Model):
    feedback = models.CharField(max_length=500, null=True, blank=True)
    delete_request = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.feedback


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return str(self.message)

