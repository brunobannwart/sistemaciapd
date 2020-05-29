from django import forms
import hashlib

# Create your form here.
class AdministradorForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=45)
	rf			=	forms.CharField(label='RF', max_length=8)
	email		=	forms.EmailField(label='Email', max_length=45)
	senha		=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput)
	comando_voz =	forms.CharField(label='Comando por voz', max_length=3)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	nvda 		=	forms.CharField(label='NVDA', max_length=3)
	foto		=	forms.ImageField(label='Foto')

	def clean_form(self):
		foto_perfil		=	self.cleaned_data.get('foto')
		nome 			= 	self.cleaned_data.get('nome')
		rf 				=	self.cleaned_data.get('rf')
		email 			=	self.cleaned_data.get('email')
		senha			=	self.cleaned_data.get('senha')
		comando			=	self.cleaned_data.get('comando_voz')
		ajuda			=	self.cleaned_data.get('ajuda_voz')
		nvda 			=	self.cleaned_data.get('nvda')

		hash_bytes = hashlib.sha256(senha.encode())
		senha_hash = hash_bytes.hexdigest()

		return { 
			'foto': foto_perfil,
			'nome': nome, 
			'rf': rf, 
			'email': email, 
			'senha': senha_hash,  
			'comando_voz': comando, 
			'ajuda_voz': ajuda, 
			'nvda': nvda 
		}

class AdministradorEditForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=45)
	rf			=	forms.CharField(label='RF', max_length=8)
	email		=	forms.EmailField(label='Email', max_length=45)
	senha		=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput, required=False)
	comando_voz =	forms.CharField(label='Comando por voz', max_length=3)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	nvda 		=	forms.CharField(label='NVDA', max_length=3)
	foto		=	forms.ImageField(label='Foto', required=False)

	def clean_form(self):
		foto_perfil		=	self.cleaned_data.get('foto')
		nome 			= 	self.cleaned_data.get('nome')
		rf 				=	self.cleaned_data.get('rf')
		email 			=	self.cleaned_data.get('email')
		senha			=	self.cleaned_data.get('senha')
		comando			=	self.cleaned_data.get('comando_voz')
		ajuda			=	self.cleaned_data.get('ajuda_voz')
		nvda 			=	self.cleaned_data.get('nvda')

		hash_bytes = hashlib.sha256(senha.encode())
		senha_hash = hash_bytes.hexdigest()

		return { 
			'foto': foto_perfil,
			'nome': nome, 
			'rf': rf, 
			'email': email, 
			'senha': senha_hash,  
			'comando_voz': comando, 
			'ajuda_voz': ajuda, 
			'nvda': nvda 
		}
