from django.db import models

def file_folder_path(instance, filename):
	return 'curriculo/{0}/{1}'.format(instance.aluno_id, filename)

# Create your models here.
class Curriculo(models.Model):
	aluno_id			=	models.IntegerField(verbose_name='ID do aluno')
	instituicao_ensino 	= 	models.CharField(verbose_name='Instituições de ensino', max_length=255, blank=True, null=False)
	curso_extra 		=	models.CharField(verbose_name='Cursos extras', max_length=255, blank=True, null=False)
	empresa 			=	models.CharField(verbose_name='Empresas', max_length=255, blank=True, null=False)
	cargo				=	models.CharField(verbose_name='Cargos ocupados', max_length=255, blank=True, null=False)
	laudo_medico 		=	models.FileField(verbose_name='Laudo médico', upload_to=file_folder_path, blank=True, null=False)
	liberado 			=	models.BooleanField(verbose_name='Curriculo liberado', default=False, null=False, blank=False)
	created_at			=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at			=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.email_aluno

	class Meta:
		db_table = 'curriculo'
		verbose_name = 'Curriculo'
		verbose_name_plural = 'Curriculo'
		ordering = ['aluno_id']