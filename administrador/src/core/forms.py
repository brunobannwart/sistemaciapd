from django import forms
import hashlib

# Create your form here.
class ChangePasswordForm(forms.Form):
	email			=	forms.EmailField(label='Email')
	senha 			=	forms.CharField(label='Senha', max_length=50, widget=forms.PasswordInput)
	confirma		=	forms.CharField(label='Confirma senha', max_length=50, widget=forms.PasswordInput)

	def clean_form(self):
		email 		=	self.cleaned_data.get('email')
		senha 		= 	self.cleaned_data.get('senha')

		hash_bytes = hashlib.sha256(senha.encode())
		senha_hash = hash_bytes.hexdigest()

		return { 'email': email, 'senha': senha_hash }