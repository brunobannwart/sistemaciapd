from django.contrib.auth.backends import BaseBackend
from django.db import connection
from core.models import LoginEmpresa

class LoginBackend(BaseBackend):
	def authenticate(request, company_email=None, company_senha=None):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, razao_social, email, senha_hash, comando_voz, ajuda_voz, nvda  FROM empresa WHERE email=%s", [company_email])
			result = cursor.fetchone()

			if result != None:
				data = {
					'id': result[0],
					'razao_social': result[1],
					'email': result[2],
					'senha_hash': result[3],
					'comando_voz': result[4],
					'ajuda_voz': result[5],
					'nvda': result[6],
				}

				try:
					company = 	LoginEmpresa.objects.create(id=data['id'], razao_social=data['razao_social'], email=data['email'], senha_hash=data['senha_hash'], 
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