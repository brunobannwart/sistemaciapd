from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os, requests, json
from .models import Empresa
from .forms import EmpresaForm, EmpresaEditForm

# Create your views here.
@login_required(login_url='login')
def company_list_view(request):
	company_list = Empresa.objects.all()
	context = {
		'company_list': company_list
	}
	return render(request, 'company/list.html', context)

@login_required(login_url='login')
def company_form_view(request, id=0):
	os.environ['NO_PROXY'] = '127.0.0.1'

	if request.method == 'POST':
		if id == 0:
			form = EmpresaForm(request.POST, request.FILES)
			edit = False
		else:
			form = EmpresaEditForm(request.POST, request.FILES or None)
			edit = True

		if form.is_valid():
			data = form.clean_form()
			
			if id == 0:
				if Empresa.objects.filter(email=data['email']) | Empresa.objects.filter(cnpj=data['cnpj']):
					if Empresa.objects.filter(email=data['email']):
						company = request.POST
						error = 'Já existe empresa com esse e-mail cadastrado'
					else:
						company = request.POST
						error = 'Já existe empresa com esse CNPJ'
				else:
					try:
						response = requests.post('http://127.0.0.1:5000/api/train', data={'group': 'empresa'}, files={ 'file': data['foto'] })
						
						if response.status_code == 200:
							responseJSON = response.json()

							create_company = Empresa.objects.create(foto=data['foto'], logo=data['logo'], 
												razao_social=data['razao_social'], cnpj=data['cnpj'], 
												nome_contato=data['nome_contato'], email=data['email'], 
												senha_hash=data['senha'], telefone=data['telefone'], 
												cep=data['cep'], numero=data['numero'], cod_treino=responseJSON['treino'],
												ajuda_voz=data['ajuda_voz'], leitor_tela=data['leitor_tela'])		
							create_company.save()

							return redirect('/empresas/')
						else:
							company = request.POST
							error = 'Foto inválida'

					except:
						form = EmpresaForm()
						error = None
						return redirect('/empresas/')			
			else:
				try:
					update_company = Empresa.objects.get(id=id)

					if 'foto' in request.FILES and update_company.nome_contato != data['nome_contato']:
						try:
							response = requests.post('http://127.0.0.1:5000/api/train', data={'group': 'empresa'}, files={ 'file': data['foto'] })

							if response.status_code == 200:
								responseJSON = response.json()
								update_company.removePicture()
								update_company.foto = data['foto']
								update_company.cod_treino = responseJSON['treino']
								
						except Exception as e:
							print(e)
				
					if 'logo' in request.FILES:
						update_company.removeLogo()
						update_company.logo = data['logo']

					if request.POST.get('senha') != '':
						update_company.senha_hash = data['senha']
				
					update_company.razao_social = data['razao_social']
					update_company.nome_contato = data['nome_contato']
					update_company.telefone = data['telefone']
					update_company.cep = data['cep']
					update_company.numero = data['numero']
					update_company.ajuda_voz = data['ajuda_voz']
					update_company.leitor_tela = data['leitor_tela']
					update_company.save()

				finally:
					form = EmpresaForm()
					error = None
					return redirect('/empresas/')
		else:
			company = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = EmpresaForm()
		error = None 
		if id == 0:
			company = {
				'logo': None,
				'foto': None,
				'razao_social': '',
				'cnpj': '',
				'nome_contato': '',
				'email': '',
				'senha': '',
				'telefone': '',
				'cep': '',
				'numero': '',
				'ajuda_voz': 'nao',
				'leitor_tela': 'nao',
			}
			edit = False
		else:
			try:
				company = Empresa.objects.get(id=id)
				edit = True
			except:
				return redirect('/empresas/')	

	context = {
		'company': company,
		'error': error,
		'edit': edit
	}

	return render(request, 'company/form.html', context)

@login_required(login_url='login')
def company_delete_view(request, id=0):
	if request.method == 'POST':
		try:
			company = Empresa.objects.get(id=id)
			train = company.cod_treino
			response = requests.post('http://127.0.0.1:5000/api/delete', data={'faceID': train})
			if response.status_code == 200:
				company.delete()
		finally:
			return redirect('/empresas/')
	else:
		return redirect('/empresas/')