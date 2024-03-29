from django import forms
import hashlib

# Create your form here.
class EmpresaForm(forms.Form):
	razao_social	= 	forms.CharField(label='Razão Social', max_length=45)
	cnpj 			=	forms.CharField(label='CNPJ', max_length=18)
	nome_contato	=	forms.CharField(label='Nome do contato', max_length=45)
	email 			=	forms.EmailField(label='E-mail', max_length=45)
	senha 			=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput)
	telefone 		=	forms.CharField(label='Telefone', max_length=14)
	cep				=	forms.CharField(label='CEP', max_length=10)
	numero			=	forms.CharField(label='Número', max_length=5)
	ajuda_voz		=	forms.CharField(label='Ajuda por voz', max_length=3)
	leitor_tela		=	forms.CharField(label='Leitor de tela', max_length=3)
	foto 			=	forms.ImageField(label='Foto')
	logo			=	forms.ImageField(label='Logo')

	def clean_form(self):
		logo_empresa 	= 	self.cleaned_data.get('logo')
		foto_perfil		=	self.cleaned_data.get('foto')
		razao			= 	self.cleaned_data.get('razao_social')
		cnpj			=	self.cleaned_data.get('cnpj')
		nome			=	self.cleaned_data.get('nome_contato')
		email			=	self.cleaned_data.get('email')
		senha			=	self.cleaned_data.get('senha')
		telefone		=	self.cleaned_data.get('telefone')
		cep 			=	self.cleaned_data.get('cep')
		numero			=	self.cleaned_data.get('numero')
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
			'logo': logo_empresa,
			'foto': foto_perfil,
			'razao_social': razao, 
			'cnpj': cnpj, 
			'nome_contato': nome, 
			'email': email, 
			'senha': senha_hash, 
			'telefone': telefone,
			'cep': cep,  
			'numero': numero,
			'ajuda_voz': ajuda_voz,
			'leitor_tela': leitor_tela
		}

class EmpresaEditForm(forms.Form):
	razao_social	= 	forms.CharField(label='Razão Social', max_length=45)
	cnpj 			=	forms.CharField(label='CNPJ', max_length=18)
	nome_contato	=	forms.CharField(label='Nome do contato', max_length=45)
	email 			=	forms.EmailField(label='E-mail', max_length=45)
	senha 			=	forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput, required=False)
	telefone 		=	forms.CharField(label='Telefone', max_length=14)
	cep				=	forms.CharField(label='CEP', max_length=10)
	numero			=	forms.CharField(label='Número', max_length=5)
	ajuda_voz		=	forms.CharField(label='Ajuda por voz', max_length=3)
	leitor_tela		=	forms.CharField(label='Leitor de tela', max_length=3)
	foto 			=	forms.ImageField(label='Foto', required=False)
	logo			=	forms.ImageField(label='Logo', required=False)

	def clean_form(self):
		logo_empresa 	= 	self.cleaned_data.get('logo')
		foto_perfil		=	self.cleaned_data.get('foto')
		razao			= 	self.cleaned_data.get('razao_social')
		cnpj			=	self.cleaned_data.get('cnpj')
		nome			=	self.cleaned_data.get('nome_contato')
		email			=	self.cleaned_data.get('email')
		senha			=	self.cleaned_data.get('senha')
		telefone		=	self.cleaned_data.get('telefone')
		cep 			=	self.cleaned_data.get('cep')
		numero			=	self.cleaned_data.get('numero')
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
			'logo': logo_empresa,
			'foto': foto_perfil,
			'razao_social': razao, 
			'cnpj': cnpj, 
			'nome_contato': nome, 
			'email': email, 
			'senha': senha_hash, 
			'telefone': telefone,
			'cep': cep,  
			'numero': numero,
			'ajuda_voz': ajuda_voz,
			'leitor_tela': leitor_tela
		}