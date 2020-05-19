from django import forms
import hashlib

class LoginForm(forms.Form):
	email = forms.EmailField(label='Email')
	senha = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)

	def clean_form(self):
		email =	self.cleaned_data.get('email')
		senha =	self.cleaned_data.get('senha')

		hash_bytes = hashlib.sha256(senha.encode())
		senha_hash = hash_bytes.hexdigest()

		return { 'email': email, 'senha': senha_hash }