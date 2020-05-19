from django.db import models

# Create your models here.
class Vaga(models.Model):
	arquivo 	=	models.ImageField(verbose_name='Arquivo', upload_to='logo/vaga', null=False, blank=False)
	titulo 		= 	models.CharField(verbose_name='Titulo', max_length=45)
	data_exp	=	models.DateField(verbose_name='Data de expiração')
	descricao	=	models.TextField(verbose_name='Descrição', blank=False, null=False, max_length=100)
	created_at	=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at	=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.titulo

	class Meta:
		db_table = 'vaga'
		verbose_name = 'Vaga'
		verbose_name_plural = 'Vagas'
		ordering = ['titulo']