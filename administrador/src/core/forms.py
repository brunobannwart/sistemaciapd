from django import forms
import hashlib

# Create your form here.
class CurriculumForm(forms.Form):
	aluno_id			=	forms.IntegerField(label='Id do Aluno')
	email 				=	forms.EmailField(label='Email do aluno')
	instituicao_ensino 	=	forms.CharField(label='Instituições de ensino', max_length=255, required=False)
	curso_extra 		=	forms.CharField(label='Cursos extras', max_length=255, required=False)
	empresa 			=	forms.CharField(label='Empresas', max_length=255, required=False)
	cargo 				=	forms.CharField(label='Cargos', max_length=255, required=False)
	liberado			=	forms.CharField(label='Liberado', max_length=3) 
	laudo_medico 		=	forms.CharField(label='Laudo médico', max_length=100, required=False)
	novo_laudo_medico	= 	forms.FileField(label='Novo laudo médico', required=False)

	def clean_form(self):
		aluno 			=	self.cleaned_data.get('aluno_id')
		email 			=	self.cleaned_data.get('email')
		instituicao 	= 	self.cleaned_data.get('instituicao_ensino')
		curso 			=	self.cleaned_data.get('curso_extra')
		empresas 		=	self.cleaned_data.get('empresa')
		cargos 			= 	self.cleaned_data.get('cargo')
		status 			= 	self.cleaned_data.get('liberado')
		laudo 			=	self.cleaned_data.get('laudo_medico')
		novo_laudo 		=	self.cleaned_data.get('novo_laudo_medico')

		return {
			'aluno_id': aluno,
			'email': email,
			'instituicao_ensino': instituicao,
			'curso_extra': curso,
			'empresa': empresas,
			'cargo': cargos,
			'liberado': status,
			'laudo_medico': laudo,
			'novo_laudo_medico': novo_laudo,
		}
