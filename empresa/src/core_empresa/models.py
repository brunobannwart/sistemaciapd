from django.db import models

# Create your models here.
class LoginEmpresa(models.Model):
	id 					=	models.IntegerField(verbose_name='ID', primary_key=True)
	razao_social		=	models.CharField(verbose_name='Razão social', max_length=45)
	email				=	models.EmailField(verbose_name='E-mail', unique=True, max_length=45)
	senha_hash			=	models.CharField(verbose_name='Senha', max_length=64)
		
	comando_voz 		=	models.CharField(verbose_name='Comando por voz', max_length=3)
	ajuda_voz			=	models.CharField(verbose_name='Ajuda por voz', max_length=3)
	nvda 				=	models.CharField(verbose_name='NVDA', max_length=3)
	
	is_authenticated	=	models.BooleanField(verbose_name='Autenticado', default=False)
	last_login			=	models.DateTimeField(verbose_name='Último login', blank=True, null=True)
	created_at			=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at			=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.nome

	class Meta:
		db_table = 'login_empresa'
		verbose_name = 'Login de Empresa'
		verbose_name_plural = 'Login de Empresa'
		ordering = ['razao_social']
