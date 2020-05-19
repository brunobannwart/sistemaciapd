from django.db import models

# Create your models here.
class Curriculo(models.Model):
	email_aluno 		=	models.EmailField(verbose_name='Email')
	intituicao_ensino 	= 	models.TextField(verbose_name='Instituições de ensino', max_length=100)
	curso_extra 		=	models.TextField(verbose_name='Cursos extras', max_length=100)
	empresa 			=	models.TextField(verbose_name='Empresas', max_length=100)
	cargo				=	models.TextField(verbose_name='Cargos ocupados', max_length=100)
	liberado 			=	models.BooleanField(verbose_name='Curriculo liberado', default=False, null=False, blank=False)
	created_at			=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at			=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.email_aluno

	class Meta:
		db_table = 'curriculo'
		verbose_name = 'Curriculo'
		verbose_name_plural = 'Curriculo'
		ordering = ['email_aluno']