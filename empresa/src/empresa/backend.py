from django.contrib.auth.backends import BaseBackend
from django.db import connection
from core_empresa.models import LoginEmpresa

class LoginBackend(BaseBackend):
	def authenticate(request, company_email=None, company_senha=None):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, foto, razao_social, email, senha_hash, comando_voz, ajuda_voz, nvda  FROM empresa WHERE email=%s", [company_email])
			result = cursor.fetchone()

			if result != None:
				data = {
					'id': result[0],
					'foto': result[1],
					'razao_social': result[2],
					'email': result[3],
					'senha_hash': result[4],
					'comando_voz': result[5],
					'ajuda_voz': result[6],
					'nvda': result[7],
				}

				try:
					company = 	LoginEmpresa.objects.create(id=data['id'], foto=data['foto'] razao_social=data['razao_social'], email=data['email'], senha_hash=data['senha_hash'], 
									comando_voz=data['comando_voz'], ajuda_voz=data['ajuda_voz'], nvda=data['nvda'])

					if company.senha_hash == company_senha:
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