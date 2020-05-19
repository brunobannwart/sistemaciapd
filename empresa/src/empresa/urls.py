"""empresa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from empresa.views import login_view, camera_view, readmore_view, forgot_view, logout_view
from core.views import changepassword_view, student_list_view, student_read_view
from vagas.views import job_list_view, job_form_view, job_delete_view

urlpatterns = [
	#path('admin/', admin.site.urls),
	
	#Paths de Login
	path('', login_view, name='login'),
	path('camera/', camera_view, name='camera'),
	path('saibamais/', readmore_view, name='readmore'),
	path('esquecidados/', forgot_view, name='forgot'),
	
	path('sair/', logout_view, name='logout'),
	path('trocarsenha/', changepassword_view, name='changepassword'),

	path('vagas/', job_list_view, name='job-list'),
	path('vagas/formulario/', job_form_view, name='job-form'),
	path('vagas/formulario/<int:id>/', job_form_view, name='job-edit'),
	path('vagas/excluir/<int:id>', job_delete_view, name='job-delete'),

	path('candidatos/', student_list_view, name='student-list'),
	path('candidatos/<int:id>/', student_read_view, name='student-read'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 