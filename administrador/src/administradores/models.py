from django.db import models

# Create your models here.
class Administrador(models.Model):
	foto 				=	models.ImageField(verbose_name='Foto', upload_to='foto/admin', null=False, blank=False)
	nome 				= 	models.CharField(verbose_name='Nome', max_length=45)
	rf	 				=	models.CharField(verbose_name='RF', max_length=8, unique=True)
	email				=	models.EmailField(verbose_name='Email', unique=True, max_length=45)
	senha_hash			=	models.CharField(verbose_name='Hash senha', max_length=64)
	
	comando_voz			=	models.BooleanField(verbose_name='Comando por voz', default=False)
	ajuda_voz 			=	models.BooleanField(verbose_name='Ajuda por voz', default=False)
	nvda 				=	models.BooleanField(verbose_name='NVDA', default=False)
	cod_treino  		=	models.IntegerField(verbose_name='ID do treino facial', null=True)

	is_authenticated	=	models.BooleanField(verbose_name='Autenticado', default=False)
	last_login			=	models.DateTimeField(verbose_name='Último login', blank=True, null=True)
	created_at			=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at			=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.nome

	def delete(self, *args, **kwargs):
		self.foto.delete()
		super().delete(*args, **kwargs)

	class Meta:
		db_table = 'administrador'
		verbose_name = 'Administrador'
		verbose_name_plural = 'Administradores'
		ordering = ['nome']
