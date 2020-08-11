from django import forms
import hashlib

# Create your form here.
class AdministradorForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=45)
	rf			=	forms.CharField(label='RF', max_length=8)
	email		=	forms.EmailField(label='Email', max_length=45)
	senha		=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	leitor_tela	=	forms.CharField(label='Leitor de tela', max_length=3)
	foto		=	forms.ImageField(label='Foto')

	def clean_form(self):
		foto_perfil		=	self.cleaned_data.get('foto')
		nome 			= 	self.cleaned_data.get('nome')
		rf 				=	self.cleaned_data.get('rf')
		email 			=	self.cleaned_data.get('email')
		senha			=	self.cleaned_data.get('senha')
		ajuda			=	self.cleaned_data.get('ajuda_voz')
		leitor			=	self.cleaned_data.get('leitor_tela')

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
			'rf': rf, 
			'email': email, 
			'senha': senha_hash,  
			'ajuda_voz': ajuda_voz, 
			'leitor_tela': leitor_tela 
		}

class AdministradorEditForm(forms.Form):
	nome 		= 	forms.CharField(label='Nome', max_length=45)
	rf			=	forms.CharField(label='RF', max_length=8)
	email		=	forms.EmailField(label='Email', max_length=45)
	senha		=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput, required=False)
	ajuda_voz	=	forms.CharField(label='Ajuda por voz', max_length=3)
	leitor_tela	=	forms.CharField(label='Leitor de tela', max_length=3)
	foto		=	forms.ImageField(label='Foto', required=False)

	def clean_form(self):
		foto_perfil		=	self.cleaned_data.get('foto')
		nome 			= 	self.cleaned_data.get('nome')
		rf 				=	self.cleaned_data.get('rf')
		email 			=	self.cleaned_data.get('email')
		senha			=	self.cleaned_data.get('senha')
		ajuda			=	self.cleaned_data.get('ajuda_voz')
		leitor 			=	self.cleaned_data.get('leitor_tela')

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
			'rf': rf, 
			'email': email, 
			'senha': senha_hash,
			'ajuda_voz': ajuda_voz, 
			'leitor_tela': leitor_tela 
		}
