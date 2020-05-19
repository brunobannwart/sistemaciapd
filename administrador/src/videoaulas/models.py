from django.db import models

# Create your models here.
class Videoaula(models.Model):
	arquivo 	=	models.ImageField(verbose_name='Arquivo', upload_to='logo/videoaula', null=False, blank=False)
	titulo 		= 	models.CharField(verbose_name='Titulo', max_length=45)
	url			=	models.URLField(verbose_name='URL', max_length=100)
	descricao	=	models.TextField(verbose_name='Descrição', blank=False, null=False, max_length=100)
	created_at	=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at	=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.titulo

	class Meta:
		db_table = 'videoaula'
		verbose_name = 'Video-aula'
		verbose_name_plural = 'Video-aulas'
		ordering = ['titulo']