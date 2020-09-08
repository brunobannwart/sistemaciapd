from django import forms

# Create your form here.
class VideoaulaForm(forms.Form):
	titulo 			= 	forms.CharField(label='Titulo', max_length=50)
	url				=	forms.URLField(label='URL', max_length=100)
	descricao		=	forms.CharField(label='Descrição', widget=forms.Textarea, max_length=150)
	arquivo 		=	forms.ImageField(label='Arquivo')

	def clean_form(self):
		arquivo 	=	self.cleaned_data.get('arquivo')
		titulo		= 	self.cleaned_data.get('titulo')
		url			=	self.cleaned_data.get('url')
		descricao	=	self.cleaned_data.get('descricao')

		return { 'arquivo': arquivo, 'titulo': titulo, 'url': url, 'descricao': descricao }

class VideoaulaEditForm(forms.Form):
	titulo 			= 	forms.CharField(label='Titulo', max_length=50)
	url				=	forms.URLField(label='URL', max_length=100)
	descricao		=	forms.CharField(label='Descrição', widget=forms.Textarea, max_length=150)
	arquivo 		=	forms.ImageField(label='Arquivo', required=False)

	def clean_form(self):
		arquivo 	=	self.cleaned_data.get('arquivo')
		titulo		= 	self.cleaned_data.get('titulo')
		url			=	self.cleaned_data.get('url')
		descricao	=	self.cleaned_data.get('descricao')

		return { 'arquivo': arquivo, 'titulo': titulo, 'url': url, 'descricao': descricao }