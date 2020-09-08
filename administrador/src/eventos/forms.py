from django import forms

# Create your form here.
class EventoForm(forms.Form):
	titulo 			= 	forms.CharField(label='Titulo', max_length=50)
	data_exp 		=	forms.DateField(label='Data de expiração')
	descricao		=	forms.CharField(label='Descrição', widget=forms.Textarea, max_length=150)
	arquivo			=	forms.ImageField(label='Arquivo')

	def clean_form(self):
		arquivo 	=	self.cleaned_data.get('arquivo')
		titulo		= 	self.cleaned_data.get('titulo')
		data_exp	=	self.cleaned_data.get('data_exp')
		descricao	=	self.cleaned_data.get('descricao')

		return { 'arquivo': arquivo, 'titulo': titulo, 'data_exp': data_exp, 'descricao': descricao }

class EventoEditForm(forms.Form):
	titulo 			= 	forms.CharField(label='Titulo', max_length=50)
	data_exp 		=	forms.DateField(label='Data de expiração')
	descricao		=	forms.CharField(label='Descrição', widget=forms.Textarea, max_length=150)
	arquivo			=	forms.ImageField(label='Arquivo', required=False)

	def clean_form(self):
		arquivo 	=	self.cleaned_data.get('arquivo')
		titulo		= 	self.cleaned_data.get('titulo')
		data_exp	=	self.cleaned_data.get('data_exp')
		descricao	=	self.cleaned_data.get('descricao')

		return { 'arquivo': arquivo, 'titulo': titulo, 'data_exp': data_exp, 'descricao': descricao }