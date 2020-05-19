from django.shortcuts import render, redirect
import os, requests, json
from .models import Empresa
from .forms import EmpresaForm, EmpresaEditForm

# Create your views here.
def company_list_view(request):
	company_list = Empresa.objects.all()
	context = {
		'company_list': company_list
	}
	return render(request, 'company/list.html', context)

def company_form_view(request, id=0):
	os.environ['NO_PROXY'] = '127.0.0.1'

	if request.method == 'POST':
		if id == 0:
			form = EmpresaForm(request.POST, request.FILES)
			read = False
		else:
			form = EmpresaEditForm(request.POST, request.FILES or None)
			read = True

		if form.is_valid():
			data = form.clean_form()
			logo = request.FILES['logo']
			
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
						#response = requests.post('http://127.0.0.1:5000/api/train', data={'group': 'empresa'}, files={ 'file': data['foto'] })

						create_company = Empresa.objects.create(foto=data['foto'], logo=data['logo'], 
											razao_social=data['razao_social'], cnpj=data['cnpj'], 
											nome_contato=data['nome_contato'], email=data['email'], 
											senha=data['senha'], telefone=data['telefone'], 
											cep=data['cep'], numero=data['numero'], 
											comando_voz=data['comando_voz'], ajuda_voz=data['ajuda_voz'], nvda=data['nvda'])		
						create_company.save()

					finally:
						form = EmpresaForm()
						error = None
						return redirect('/empresas/')			
			else:
				try:
					update_company = Empresa.objects.get(id=id)
				
					if request.FILES.get('foto', False):
						update_company.foto = data['foto']
				
					if request.FILES.get('logo', False):
						update_company.logo = data['logo']
				
					update_company.razao_social = data['razao_social']
					update_company.nome_contato = data['nome_contato']
					update_company.telefone = data['telefone']
					update_company.cep = data['cep']
					update_company.numero = data['numero']
					update_company.comando_voz = data['comando_voz']
					update_company.ajuda_voz = data['ajuda_voz']
					update_company.nvda = data['nvda']
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
				'comando_voz': '',
				'ajuda_voz': '',
				'nvda': '',
			}
			read = False
		else:
			try:
				company = Empresa.objects.get(id=id)
				read = True
			except:
				return redirect('/empresas/')	

	context = {
		'company': company,
		'error': error,
		'read': read
	}

	return render(request, 'company/form.html', context)

def company_delete_view(request, id=0):
	try:
		company = Empresa.objects.get(id=id)
		company.delete()
	finally:
		return redirect('/empresas/')