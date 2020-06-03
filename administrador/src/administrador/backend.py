from django.contrib.auth.backends import BaseBackend
from administradores.models import Administrador

class LoginBackend(BaseBackend):
	def authenticate(request, admin_email=None, admin_senha=None):
		try:
			admin = Administrador.objects.get(email=admin_email)

			if admin.senha_hash == admin_senha:
				return admin
			else:
				return False
		except:
			return None

	def get_user(self, admin_id):
		try:
			return Administrador.objects.get(id=admin_id)
		except:
			return None