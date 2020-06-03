from django.db import models

# Create your models here.
class Empresa(models.Model):
	foto 				=	models.ImageField(verbose_name='Foto', upload_to='foto/empresa', null=False, blank=False)
	logo				=	models.ImageField(verbose_name='Logo', upload_to='logo/empresa', null=False, blank=False)
	razao_social		=	models.CharField(verbose_name='Razão social', max_length=45)
	cnpj				=	models.CharField(verbose_name='CNPJ', max_length=18, unique=True)
	
	nome_contato		=	models.CharField(verbose_name='Nome do contato', max_length=45)
	telefone			=	models.CharField(verbose_name='Telefone', max_length=14)

	email				=	models.EmailField(verbose_name='E-mail', unique=True, max_length=45)
	senha_hash			=	models.CharField(verbose_name='Senha', max_length=64)
	
	cep					=	models.CharField(verbose_name='CEP', max_length=10)
	numero				=	models.CharField(verbose_name='Número', max_length=5)
	
	comando_voz			=	models.CharField(verbose_name='Comando por voz', max_length=3)
	ajuda_voz			=	models.CharField(verbose_name='Ajuda por voz', max_length=3)
	nvda 				=	models.CharField(verbose_name='NVDA', max_length=3)
	
	cod_treino 			=	models.IntegerField(verbose_name='ID do treino facial', null=True)
	is_authenticated	=	models.BooleanField(verbose_name='Autenticado', default=False)
	last_login			=	models.DateTimeField(verbose_name='Último login', blank=True, null=True)
	created_at			=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at			=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.razao_social

	class Meta:
		db_table = 'empresa'
		verbose_name = 'Empresa'
		verbose_name_plural = 'Empresas'
		ordering = ['razao_social']
