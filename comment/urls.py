from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
 path('', views.home, name="home"),
 path('motech/', views.motech, name="motech"),
 path('songs/', views.song, name="song"),
 path('index/', views.index, name="index"),
 path('youtube/', views.youtube, name='youtube'),
 path('youtube/demoses/', views.demoses, name='demoses'),
 path('pelcon/', views.pelcon, name='pelcon'),
 path('myajax/', views.myajax, name='myajax'),
 path('pelcon/yourajax/', views.yourajax, name='yourajax'),
 path('form/', views.uploadForm, name='form'),
 path('upload/', views.uploadFile, name='upload'),
 path('files/', views.FileView.as_view(), name='files'),
 path('pelcono/', views.PelconView.as_view(), name='pelcon'),
 path('myupload/', views.myUpload, name='myupload'),
 path('pelconUpload/', views.pelconUpload, name='pelconUpload'),
 path('crud/', views.IndexView.as_view(), name='crud'),
 path('student/', views.Student, name='save'),
 path('editdata/', views.editdata, name='edit'),
 path('update/', views.updatedata, name='update'),

 # Appointment Reminder
 path('new/', views.AppointmentCreateView.as_view(), name='new_appointment'),
 path('list/', views.ListStudent.as_view(), name='list'),
 path('add/', views.CreateStudent.as_view(), name='add'),
 path('alist/', views.AppointmentListView.as_view(), name='alist'),
 path('ulist/<int:pk>', views.AppointmentUpdateView.as_view(), name='ulist'),
 path('dlist/<int:pk>', views.AppointmentDeleteView.as_view(), name='dlist'),
 path('vlist/<int:pk>', views.AppointmentDetailView.as_view(), name='vlist'),



# ALL BookApp URLS's 
path('BookApp/', views.login, name='login'),
path('uadd_book/', views.uadd_book, name='uadd_book'),
path('add_book/', views.add_book, name='add_book'),
path('listbook/', views.BookListView.as_view(), name='blist'),
path('upload-book/', views.upload_book, name='ubook'),
path('login/', views.loginView, name='login_form'),
path('register/', views.register, name='register'),
path('registeruser/', views.registerUser, name='registeruser'),
path('logout/', views.logout_view, name='logout'),
path('albook/', views.ABookListView.as_view(), name='albook'),
path('mbook/', views.ManageBook.as_view(), name='mbook'),


# Publisher URL's
path('delete_request/', views.delete_request, name='delete_request'),
path('dbr/', views.delete_book_request, name='dbr'),
path('send_feedback/', views.send_feedback, name='send_feedback'),
path('send_feedback_user/', views.send_feedback_user, name='feedback'),
path('about/', views.about, name='about'),
path('psearch/',views.psearch,name='psearch'),





# Librarian URL's
path('librarian/', views.librarian, name='librarian'),
path('ladd_book/', views.ladd_book, name='ladd_book'),
path('lupload_book/', views.lupload_book, name='lupload_book'),
path('llbook/', views.LListBook.as_view(), name='llbook'),
path('lvbook/<int:pk>', views.LViewBook.as_view(), name='lvbook'),
path('lmbook/', views.LManageBook.as_view(), name='lmbook'),
path('lebook/<int:pk>', views.LEditBook.as_view(), name='lebook'),
path('ldbook/<int:pk>', views.LDBook.as_view(), name='ldbook'),
path('lchat/', views.LChatList.as_view(), name='lall_chat'),
path('lnew_chat/', views.LChatCreate.as_view(), name='lnew_chat'),
path('ldelete_request/', views.LDeleteRequest.as_view(), name='ldelete_request'),
path('lsearch/',views.lsearch,name='lsearch'),
path('lib_del/<int:pk>', views.LibDelete.as_view(), name='lib_del'),



# Admin URL's
path('avbook/<int:pk>', views.ALViewBook.as_view(), name='avbook'),
path('aebook/<int:pk>', views.AEditBook.as_view(), name='aebook'),
path('adbook/<int:pk>', views.ADBook.as_view(), name='adbook'),
path('adelete_request/', views.ADeleteRequest.as_view(), name='adelete_request'),
path('achat/', views.AChatList.as_view(), name='aall_chat'),
path('anew_chat/', views.AChatCreate.as_view(), name='anew_chat'),
path('dashboard/', views.dashboard, name='dashboard'),
path('create_user/', views.create_user_form, name='create_user'),
path('create/', views.create, name='create'),
path('users/', views.UserView.as_view(), name='users'),
path('aduser/<int:pk>', views.ADUser.as_view(), name='aduser'),
path('avuser/<int:pk>', views.ALViewUser.as_view(), name='avuser'),
path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
path('asearch/',views.asearch,name='asearch'),
path('admin_del/<int:pk>', views.AdminDelete.as_view(), name='admin_del'),
path('aupload_book/', views.aupload_book, name='aupload_book'),


# Career Day
path('ma/', views.CDListFile.as_view(), name='ma'),
path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
path('process_pdf/', views.process_pdf, name='process_pdf'),

# Chat
path('chat/', views.ChatListView.as_view(), name='all_chat'),
path('new_chat/', views.ChatCreateView.as_view(), name='new_chat'),


path('edit_file/<int:pk>', views.UpdateFile.as_view(), name='edit_file'),
path('update_file/<int:pk>', views.update_file, name='update_file'),



path('cb/', views.create_book_normal, name='cb'),
path('addbird/', views.BirdAddView.as_view(), name="add_bird"),
path('listbird/', views.BirdListView.as_view(), name="bird_list"),





path('music/', views.make_prediction, name='music'),























]
