from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Videoaula
from .forms import VideoaulaForm, VideoaulaEditForm

# Create your views here.
@login_required(login_url='login')
def videolesson_list_view(request):
	videolesson_list = Videoaula.objects.all()
	context = {
		'videolesson_list': videolesson_list
	}
	return render(request, "videolesson/list.html", context)

@login_required(login_url='login')
def videolesson_form_view(request, id=0): 
	if request.method == 'POST':
		if id == 0:
			form = VideoaulaForm(request.POST, request.FILES)
		else:
			form = VideoaulaEditForm(request.POST, request.FILES or None)

		if form.is_valid():
			data = form.clean_form()
			
			if id == 0:
				try:
					create_videolesson = Videoaula.objects.create(arquivo=data['arquivo'], titulo=data['titulo'], url=data['url'], descricao=data['descricao'])
					create_videolesson.save()

				finally:
					form = VideoaulaForm()
					error = None
					return redirect('/videoaulas/')
			else:
				try:
					update_videolesson = Videoaula.objects.get(id=id)

					if 'arquivo' in request.FILES:
						update_videolesson.removeFile()
						update_videolesson.arquivo = data['arquivo']
					
					update_videolesson.titulo = data['titulo']
					update_videolesson.url = data['url']
					update_videolesson.descricao = data['descricao']
					update_videolesson.save()

				finally:
					form = VideoaulaForm()
					error = None
					return redirect('/videoaulas/')
		else:
			videolesson = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = VideoaulaForm()
		error = None 

		if id == 0:
			videolesson = {
				'arquivo': None,
				'titulo': '',
				'url': '',
				'descricao': '',
			}
		else:
			try:
				videolesson = Videoaula.objects.get(id=id)
			except:
				return redirect('/videoaulas/')
	context = {
		'videolesson': videolesson,
		'error': error
	}

	return render(request, "videolesson/form.html", context)

@login_required(login_url='login')
def videolesson_delete_view(request, id=0):
	if request.method == 'POST':
		try:
			videolesson = Videoaula.objects.get(id=id)
			videolesson.delete()
		finally:
			return redirect('/videoaulas/')
	else:
		return redirect('/videoaulas/')