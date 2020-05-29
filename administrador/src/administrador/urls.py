"""administrador URL Configuration

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

	path('admin/', admin.site.urls),
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from administrador.views import login_view, camera_view, readmore_view, forgot_view, logout_view
from core.views import job_list_view, job_read_view, curriculum_list_view, curriculum_read_view

from administradores.views import admin_list_view, admin_form_view, admin_delete_view
from alunos.views import student_list_view, student_form_view, student_delete_view

from cursos.views import course_list_view, course_form_view, course_delete_view
from empresas.views import company_list_view, company_form_view, company_delete_view

from eventos.views import event_list_view, event_form_view, event_delete_view
from jogos.views import game_list_view, game_form_view, game_delete_view
from videoaulas.views import videolesson_list_view, videolesson_form_view, videolesson_delete_view

urlpatterns = [
	#path('admin/', admin.site.urls),

	path('', login_view, name='login'),
	path('camera/', camera_view, name='camera'),
	path('saibamais/', readmore_view, name='readmore'),
	path('esquecidados/', forgot_view, name='forgot'),
	path('sair/', logout_view, name='logout'),

	path('administradores/', admin_list_view, name='admin-list'),
	path('administradores/formulario/', admin_form_view, name='admin-form'),
	path('administradores/formulario/<int:id>/', admin_form_view, name='admin-edit'),
	path('administradores/excluir/<int:id>/', admin_delete_view, name='admin-delete'),

	path('alunos/', student_list_view, name='student-list'),
	path('alunos/formulario/', student_form_view, name='student-form'),
	path('alunos/formulario/<int:id>/', student_form_view, name='student-edit'),
	path('alunos/excluir/<int:id>/', student_delete_view, name='student-delete'),

	path('curriculos/', curriculum_list_view, name='curriculum-list'),
	path('curriculos/<int:id>/', curriculum_read_view, name='curriculum-read'),

	path('cursos/', course_list_view, name='course-list'),
	path('cursos/formulario/', course_form_view, name='course-form'),
	path('cursos/formulario/<int:id>/', course_form_view, name='course-edit'),
	path('cursos/excluir/<int:id>/', course_delete_view, name='course-delete'),

	path('empresas/', company_list_view, name='company-list'),
	path('empresas/formulario/', company_form_view, name='company-form'),
	path('empresas/formulario/<int:id>/', company_form_view, name='company-edit'),
	path('empresas/excluir/<int:id>/', company_delete_view, name='company-delete'),

	path('eventos/', event_list_view, name='event-list'),
	path('eventos/formulario/', event_form_view, name='event-form'),
	path('eventos/formulario/<int:id>/', event_form_view, name='event-edit'),
	path('eventos/excluir/<int:id>/', event_delete_view, name='event-delete'),

	path('jogos/', game_list_view, name='game-list'),
	path('jogos/formulario/', game_form_view, name='game-form'),
	path('jogos/formulario/<int:id>/', game_form_view, name='game-edit'),
	path('jogos/excluir/<int:id>/', game_delete_view, name='game-delete'),

	path('vagas/', job_list_view, name='job-list'),
	path('vagas/<int:id>/', job_read_view, name='job-read'),

	path('videoaulas/', videolesson_list_view, name='videolesson-list'),
	path('videoaulas/formulario/', videolesson_form_view, name='videolesson-form'),
	path('videoaulas/formulario/<int:id>/', videolesson_form_view, name='videolesson-edit'),
	path('videoaulas/excluir/<int:id>/', videolesson_delete_view, name='videolesson-delete'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 