"""aluno URL Configuration

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

from aluno.views import login_view, camera_view, home_view, logout_view
from core_aluno.views import course_list_view, course_view

from core_aluno.views import event_list_view, event_view
from core_aluno.views import game_list_view, game_view 

from core_aluno.views import job_list_view, job_view
from core_aluno.views import videolesson_list_view, videolesson_view
from curriculos.views import curriculum_form_view

urlpatterns = [
	#path('admin/', admin.site.urls),

	#Path Login
	path('', login_view, name='login'),
	path('camera/', camera_view, name='camera'),
	path('sair/', logout_view, name='logout'),

	path('inicio/', home_view, name='home'),
	path('curriculo/formulario/', curriculum_form_view, name='curriculum-form'),

	#Paths de cursos
	path('cursos/', course_list_view, name='course-list'),
	path('cursos/<int:id>/', course_view, name='course'),

	#Paths de eventos
	path('eventos/', event_list_view, name='event-list'),
	path('eventos/<int:id>/', event_view, name='event'),

	#Paths de jogos
	path('jogos/', game_list_view, name='game-list'),
	path('jogos/<int:id>/', game_view, name='game'),

	#Paths de vagas
	path('vagas/', job_list_view, name='job-list'),
	path('vagas/<int:id>/', job_view, name='job'),

	#Paths de videoaulas
	path('videoaulas/', videolesson_list_view, name='videolesson-list'),
	path('videoaulas/<int:id>/', videolesson_view, name='videolesson'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 