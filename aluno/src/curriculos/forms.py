from django import forms
import hashlib

# Create your form here.
class CurriculoForm(forms.Form):
	intituicao_ensino 	= 	forms.CharField(label='Instituições de ensino', widget=forms.Textarea, max_length=100)
	curso_extra 		=	forms.CharField(label='Cursos extras', widget=forms.Textarea, max_length=100)
	empresa 			=	forms.CharField(label='Empresas', widget=forms.Textarea, max_length=100)
	cargo				=	forms.CharField(label='Cargos ocupados', widget=forms.Textarea, max_length=100)

	def clean_form(self):
		instituicao	=	self.cleaned_data.get('intituicao_ensino')
		curso 		=	self.cleaned_data.get('curso_extra')
		empresa		=	self.cleaned_data.get('empresa')
		cargo		=	self.cleaned_data.get('cargo')

		return { 'intituicao_ensino': instituicao, 'curso_extra': curso, 'empresa': empresa, 'cargo': cargo }