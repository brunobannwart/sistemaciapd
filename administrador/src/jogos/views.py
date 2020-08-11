from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Jogo
from .forms import JogoForm, JogoEditForm

# Create your views here.
@login_required(login_url='login')
def game_list_view(request):
	game_list = Jogo.objects.all()
	context = {
		'game_list': game_list
	}
	return render(request, 'game/list.html', context)

@login_required(login_url='login')
def game_form_view(request, id=0): 
	if request.method == 'POST':
		if id == 0:
			form = JogoForm(request.POST, request.FILES)
		else:
			form = JogoEditForm(request.POST, request.FILES or None)

		if form.is_valid():
			data = form.clean_form()
						
			if id == 0:
				try:
					create_game = Jogo.objects.create(arquivo=data['arquivo'], titulo=data['titulo'], url=data['url'], descricao=data['descricao'])
					create_game.save()

				finally:
					form = JogoForm()
					error = None
					return redirect('/jogos/')
			else:
				try:
					update_game = Jogo.objects.get(id=id)

					if 'arquivo' in request.FILES:
						update_game.removeFile()
						update_game.arquivo = data['arquivo']

					update_game.titulo = data['titulo']
					update_game.url = data['url']
					update_game.descricao = data['descricao']
					update_game.save()

				finally:
					form = JogoForm()
					error = None
					return redirect('/jogos/')
		else:
			game = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = JogoForm() 
		error = None

		if id == 0:
			game = {
				'arquivo': None,
				'titulo': '',
				'url': '',
				'descricao': '',
			}
		else:
			try:
				game = Jogo.objects.get(id=id)
			except:
				return redirect('/jogos/')
	context = {
		'game': game,
		'error': error
	}

	return render(request, 'game/form.html', context)

@login_required(login_url='login')
def game_delete_view(request, id=0):
	if request.method == 'POST':
		try:
			game = Jogo.objects.get(id=id)
			game.delete()
		finally:
			return redirect('/jogos/')
	else:
		return redirect('/jogos/')