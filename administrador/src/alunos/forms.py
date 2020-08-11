from django import forms
from cids.models import Cid
import hashlib

# Create your form here.
class AlunoForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=100)
	data_nasc	=	forms.DateField(label='Data de nascimento')
	email		=	forms.EmailField(label='Email', max_length=45)
	senha		=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput)
	cpf			=	forms.CharField(label='CPF', max_length=14)
	cep			=	forms.CharField(label='CEP', max_length=10)
	numero		=	forms.CharField(label='Número', max_length=5)
	celular     =	forms.CharField(label='Celular', max_length=15)
	cid 		=	forms.ModelMultipleChoiceField(label='CIDs', widget=forms.SelectMultiple, queryset=Cid.objects.all(), required=False)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	leitor_tela	=	forms.CharField(label='Leitor de tela', max_length=3)
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
		ajuda		=	self.cleaned_data.get('ajuda_voz')
		leitor 		=	self.cleaned_data.get('leitor_tela')
		info		=	self.cleaned_data.get('outra_info')

		if ajuda == 'sim':
			ajuda_voz = True
		else:
			ajuda_voz = False

		if leitor == 'sim':
			leitor_tela = True
		else:
			leitor_tela = False

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
			'ajuda_voz': ajuda_voz, 
			'leitor_tela': leitor_tela, 
			'outra_info': info 
		}

class AlunoEditForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=100)
	data_nasc	=	forms.DateField(label='Data de nascimento')
	email		=	forms.EmailField(label='Email', max_length=45)
	senha		=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput, required=False)
	cpf			=	forms.CharField(label='CPF', max_length=14)
	cep			=	forms.CharField(label='CEP', max_length=10)
	numero		=	forms.CharField(label='Número', max_length=5)
	celular     =	forms.CharField(label='Celular', max_length=15)
	cid 		=	forms.ModelMultipleChoiceField(label='CIDs', widget=forms.SelectMultiple, queryset=Cid.objects.all(), required=False)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	leitor_tela	=	forms.CharField(label='Leitor de tela', max_length=3)
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
		ajuda		=	self.cleaned_data.get('ajuda_voz')
		leitor 		=	self.cleaned_data.get('leitor_tela')
		info		=	self.cleaned_data.get('outra_info')

		if ajuda == 'sim':
			ajuda_voz = True
		else:
			ajuda_voz = False

		if leitor == 'sim':
			leitor_tela = True
		else:
			leitor_tela = False

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
			'ajuda_voz': ajuda_voz, 
			'leitor_tela': leitor_tela, 
			'outra_info': info 
		}