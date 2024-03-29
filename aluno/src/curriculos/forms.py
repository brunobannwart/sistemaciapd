from django import forms
import hashlib

# Create your form here.
class CurriculoForm(forms.Form):
	instituicao_ensino 	= 	forms.CharField(label='Instituições de ensino', max_length=255, required=False)
	curso_extra 		=	forms.CharField(label='Cursos extras', max_length=255, required=False)
	empresa 			=	forms.CharField(label='Empresas', max_length=255, required=False)
	cargo				=	forms.CharField(label='Cargos ocupados', max_length=255, required=False)
	laudo_medico		=	forms.FileField(label='Laudo médico', required=False)

	def clean_form(self):
		instituicao	=	self.cleaned_data.get('instituicao_ensino')
		curso 		=	self.cleaned_data.get('curso_extra')
		empresa		=	self.cleaned_data.get('empresa')
		cargo		=	self.cleaned_data.get('cargo')
		laudo 		=	self.cleaned_data.get('laudo_medico')

		return { 'instituicao_ensino': instituicao, 'curso_extra': curso, 'empresa': empresa, 'cargo': cargo, 'laudo_medico': laudo }