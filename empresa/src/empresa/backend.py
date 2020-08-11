from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.db import connection
from core_empresa.models import LoginEmpresa

class LoginBackend(BaseBackend):
	def authenticate(request, company_email=None, company_senha=None):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, logo, razao_social, email, senha_hash, ajuda_voz, leitor_tela  FROM empresa WHERE email=%s", [company_email])
			result = cursor.fetchone()

			if result != None:
				data = {
					'id': result[0],
					'logo': settings.MEDIA_URL + result[1],
					'razao_social': result[2],
					'email': result[3],
					'senha_hash': result[4],
					'ajuda_voz': result[5],
					'leitor_tela': result[6],
				}

				try:
					if company_senha == data['senha_hash']:
						if LoginEmpresa.objects.filter(id=data['id']):
							company_session = LoginEmpresa.objects.get(id=data['id'])
							company_session.delete()

						company = 	LoginEmpresa.objects.create(id=data['id'], logo=data['logo'], razao_social=data['razao_social'], email=data['email'], senha_hash=data['senha_hash'], 
										ajuda_voz=data['ajuda_voz'], leitor_tela=data['leitor_tela'])

						return company
					else:
						return False
				except:
					return None
			else:
				return None

	def get_user(self, company_id):
		try:
			return LoginEmpresa.objects.get(id=company_id)
		except:
			return None