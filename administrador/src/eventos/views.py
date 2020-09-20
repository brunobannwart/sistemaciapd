from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import Evento
from .forms import EventoForm, EventoEditForm

# Create your views here.
@login_required(login_url='login')
def event_list_view(request):
	event_list = Evento.objects.all()
	context = {
		'event_list': event_list
	}
	return render(request, 'event/list.html', context)

@login_required(login_url='login')
@csrf_protect
def event_form_view(request, id=0): 
	if request.method == 'POST':
		if id == 0:
			form = EventoForm(request.POST, request.FILES)
		else:
			form = EventoEditForm(request.POST, request.FILES or None)

		if form.is_valid():
			data = form.clean_form()
			
			if id == 0:
				try:
					create_event = Evento.objects.create(arquivo=data['arquivo'], titulo=data['titulo'], data_exp=data['data_exp'], descricao=data['descricao'])
					create_event.save()

				finally:
					form = EventoForm()
					error = None
					return redirect('/eventos/')
			else:
				try:
					update_event = Evento.objects.get(id=id)

					if 'arquivo' in request.FILES:
						update_event.removeFile()
						update_event.arquivo = data['arquivo']
					
					update_event.titulo = data['titulo']
					update_event.data_exp = data['data_exp']
					update_event.descricao = data['descricao']
					update_event.save()

				finally:
					form = EventoForm()
					error = None
					return redirect('/eventos/')
		else:
			event = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = EventoForm()
		error = None

		if id == 0:
			event = {
				'arquivo': None,
				'titulo': '',
				'data_exp': '',
				'descricao': '',
			}
		else:
			try:
				event = Evento.objects.get(id=id)
			except:
				return redirect('/eventos/')
	context = {
		'event': event,
		'error': error
	} 

	context.update(csrf(request))
	return render(request, 'event/form.html', context)

@login_required(login_url='login')
@csrf_protect
def event_delete_view(request, id=0):
	if request.method == 'POST':
		try:
			event = Evento.objects.get(id=id)
			event.delete()
		finally:
			return redirect('/eventos/')
	else:
		return redirect('/eventos/')