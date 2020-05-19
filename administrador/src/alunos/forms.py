from django import forms
import hashlib

# Create your form here.
class AlunoForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=100)
	data_nasc	=	forms.DateField(label='Data de nascimento')
	email		=	forms.EmailField(label='Email')
	senha		=	forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)
	cpf			=	forms.CharField(label='CPF', max_length=14)
	cep			=	forms.CharField(label='CEP', max_length=10)
	numero		=	forms.CharField(label='Número', max_length=5)
	celular     =	forms.CharField(label='Celular', max_length=15)
	cid 		=	forms.CharField(label='CIDs', widget=forms.Textarea, required=True)
	comando_voz =	forms.CharField(label='Comando por voz', max_length=3)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	nvda 		=	forms.CharField(label='NVDA', max_length=3)
	outra_info	=	forms.CharField(label='Outras Informações', widget=forms.Textarea, required=False, max_length=100)
	foto		=	forms.ImageField(label='Foto')

	def clean_form(self):
		foto_perfil	=	self.cleaned_data.get('foto')
		nome 		= 	self.cleaned_data.get('nome')
		data 		=	self.cleaned_data.get('data_nasc')
		email		=	self.cleaned_data.get('email')
		senha		=	self.cleaned_data.get('senha')
		cpf 		=	self.cleaned_data.get('cpf')
		celular 	=	self.cleaned_data.get('celular')
		cep			=	self.cleaned_data.get('cep')
		numero		=	self.cleaned_data.get('numero')	
		cid 		=	self.cleaned_data.get('cid')
		comando		=	self.cleaned_data.get('comando_voz')
		ajuda		=	self.cleaned_data.get('ajuda_voz')
		nvda		=	self.cleaned_data.get('nvda')
		info		=	self.cleaned_data.get('outra_info')

		hash_bytes = hashlib.sha256(senha.encode())
		senha_hash = hash_bytes.hexdigest()

		return { 
			'foto': foto_perfil,
			'nome': nome, 
			'data_nasc': data, 
			'email': email, 
			'senha': senha_hash,
			'cpf': cpf,
			'celular': celular, 
			'cep': cep, 
			'numero': numero, 
			'cid': cid,
			'comando_voz': comando, 
			'ajuda_voz': ajuda, 
			'nvda': nvda, 
			'outra_info': info 
		}

class AlunoEditForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=100)
	data_nasc	=	forms.DateField(label='Data de nascimento')
	email		=	forms.EmailField(label='Email')
	senha		=	forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)
	cpf			=	forms.CharField(label='CPF', max_length=14)
	cep			=	forms.CharField(label='CEP', max_length=10)
	numero		=	forms.CharField(label='Número', max_length=5)
	celular     =	forms.CharField(label='Celular', max_length=15)
	cid 		=	forms.CharField(label='CIDs', widget=forms.Textarea, required=True)
	comando_voz =	forms.CharField(label='Comando por voz', max_length=3)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	nvda 		=	forms.CharField(label='NVDA', max_length=3)
	outra_info	=	forms.CharField(label='Outras Informações', widget=forms.Textarea, required=False, max_length=100)
	foto		=	forms.ImageField(label='Foto', required=False)

	def clean_form(self):
		foto_perfil	=	self.cleaned_data.get('foto')
		nome 		= 	self.cleaned_data.get('nome')
		data 		=	self.cleaned_data.get('data_nasc')
		email		=	self.cleaned_data.get('email')
		senha		=	self.cleaned_data.get('senha')
		cpf 		=	self.cleaned_data.get('cpf')
		celular 	=	self.cleaned_data.get('celular')
		cep			=	self.cleaned_data.get('cep')
		numero		=	self.cleaned_data.get('numero')	
		cid 		=	self.cleaned_data.get('cid')
		comando		=	self.cleaned_data.get('comando_voz')
		ajuda		=	self.cleaned_data.get('ajuda_voz')
		nvda		=	self.cleaned_data.get('nvda')
		info		=	self.cleaned_data.get('outra_info')

		hash_bytes = hashlib.sha256(senha.encode())
		senha_hash = hash_bytes.hexdigest()

		return { 
			'foto': foto_perfil,
			'nome': nome, 
			'data_nasc': data, 
			'email': email, 
			'senha': senha_hash,
			'cpf': cpf,
			'celular': celular, 
			'cep': cep, 
			'numero': numero, 
			'cid': cid,
			'comando_voz': comando, 
			'ajuda_voz': ajuda, 
			'nvda': nvda, 
			'outra_info': info 
		}