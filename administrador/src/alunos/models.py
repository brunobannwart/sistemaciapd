from django.db import models

# Create your models here.
class Aluno(models.Model):
	foto 				=	models.ImageField(verbose_name='Foto', upload_to='foto/aluno', null=False, blank=False)
	nome 				= 	models.CharField(verbose_name='Nome', max_length=45)
	data_nasc			=	models.DateField(verbose_name='Data de nascimento')
	
	email				=	models.EmailField(verbose_name='E-mail', unique=True)
	senha				=	models.CharField(verbose_name='Senha', max_length=64)
	
	cpf					=	models.CharField(verbose_name='CPF', max_length=14, unique=True)
	celular				=	models.CharField(verbose_name='Telefone', max_length=15)
	
	cep					=	models.CharField(verbose_name='CEP', max_length=10)
	numero				=	models.CharField(verbose_name='Número', max_length=5)
	cid 				=	models.TextField(verbose_name='CIDs', null=False, blank=False)
	
	comando_voz 		=	models.CharField(verbose_name='Comando por voz', max_length=3)
	ajuda_voz			=	models.CharField(verbose_name='Ajuda por voz', max_length=3)
	nvda 				=	models.CharField(verbose_name='NVDA', max_length=3)
	outra_info			=	models.TextField(verbose_name='Outras Informações', blank=True, null=False, max_length=100)
	
	intituicao_ensino 	= 	models.TextField(verbose_name='Instituições de ensino', max_length=100, blank=True, null=False)
	curso_extra 		=	models.TextField(verbose_name='Cursos extras', max_length=100, blank=True, null=False)
	empresa 			=	models.TextField(verbose_name='Empresas', max_length=100, blank=True, null=False)
	cargo				=	models.TextField(verbose_name='Cargos ocupados', max_length=100, blank=True, null=False)
	
	cod_treino 			=	models.IntegerField(verbose_name='ID do treino facial', null=True)
	created_at			=	models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
	updated_at			=	models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

	def __str__(self):
		return self.nome

	class Meta:
		db_table = 'aluno'
		verbose_name = 'Aluno'
		verbose_name_plural = 'Alunos'
		ordering = ['nome']