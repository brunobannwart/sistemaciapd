from django.shortcuts import render, redirect
import os, requests, json
from .models import Administrador
from .forms import AdministradorForm, AdministradorEditForm

# Create your views here.
def admin_list_view(request):
	admin_list = Administrador.objects.all() 
	context = {
		'admin_list': admin_list
	}
	return render(request, 'administrator/list.html', context)

def admin_form_view(request, id=0):
	os.environ['NO_PROXY'] = '127.0.0.1'
	
	if request.method == 'POST':

		if id == 0:
			form = AdministradorForm(request.POST, request.FILES)
			edit = False
		else:
			form = AdministradorEditForm(request.POST, request.FILES or None)
			edit = True

		if form.is_valid():
			data = form.clean_form()

			if id == 0:
				if Administrador.objects.filter(email=data['email']) | Administrador.objects.filter(rf=data['rf']):
					if Administrador.objects.filter(email=data['email']):
						administrator = request.POST
						error = 'Já existe administrador com esse e-mail cadastrado'
					else:
						administrator = request.POST
						error = 'Já existe administrador com esse RF'
				else:
					try:
						response = requests.post('http://127.0.0.1:5000/api/train', data={'group': 'administrador'}, files={ 'file': data['foto'] })

						if response.status_code == 200:	
							responseJSON = response.json()			
							
							create_admin = 	Administrador.objects.create(foto=data['foto'], nome=data['nome'], rf=data['rf'], 
												email=data['email'], senha_hash=data['senha'], cod_treino=responseJSON['treino'],
												comando_voz=data['comando_voz'], ajuda_voz=data['ajuda_voz'], nvda=data['nvda'])	
							create_admin.save()
							
							form = AdministradorForm()
							error = None
							return redirect('/administradores/')

						else:
							administrator = request.POST
							error = 'Foto inválida'

					except:	
						form = AdministradorForm()
						error = None
						return redirect('/administradores/')
			else:
				try:
					update_admin = Administrador.objects.get(id=id)

					if request.FILES.get('foto', False):
						update_admin.foto = data['foto']

					if request.POST.get('senha') != '':
						update_admin.senha_hash = data['senha']
					
					update_admin.nome = data['nome']
					update_admin.comando_voz = data['comando_voz']
					update_admin.ajuda_voz = data['ajuda_voz']
					update_admin.nvda = data['nvda']
					update_admin.save()


				finally:
					form = AdministradorForm()
					error = None
					return redirect('/administradores/')	
		else:
			administrator = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'

	else:
		form = AdministradorForm()
		error = None

		if id == 0:
			administrator = {
				'foto': None,
				'nome': '',
				'rf': '',
				'email': '',
				'senha': '',
				'comando_voz': 'nao',
				'ajuda_voz': 'nao',
				'nvda': 'nao',
			}

			edit = False
		else:
			try:
				administrator = Administrador.objects.get(id=id)
				edit = True
			except:
				return redirect('/administradores/')
			
	context = {
		'administrator': administrator,
		'error': error,
		'edit': edit
	}

	return render(request, 'administrator/form.html', context)

def admin_delete_view(request, id=0):
	try:
		administrator = Administrador.objects.get(id=id)
		#train = administrator.cod_treino
		#response = requests.post('http://127.0.0.1:5000/api/delete', data={'faceID': train})
		#if response.status_code == 200:
		administrator.delete()
	finally:
		return redirect('/administradores/')