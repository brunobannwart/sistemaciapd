from django.contrib.auth.backends import BaseBackend
from django.db import connection
from core_aluno.models import LoginAluno

class LoginBackend(BaseBackend):
	def authenticate(request, student_email=None, student_senha=None):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, nome, email, senha_hash, comando_voz, ajuda_voz, nvda  FROM aluno WHERE email=%s", [student_email])
			result = cursor.fetchone()

			if result != None:
				data = {
					'id': result[0],
					'nome': result[1],
					'email': result[2],
					'senha_hash': result[3],
					'comando_voz': result[4],
					'ajuda_voz': result[5],
					'nvda': result[6],
				}

				try:
					if student_senha == data['senha_hash']:
						if LoginAluno.objects.filter(id=data['id']):
							student_session = LoginAluno.objects.get(id=data['id'])
							student_session.delete()

						student = 	LoginAluno.objects.create(id=data['id'], nome=data['nome'], email=data['email'], senha_hash=data['senha_hash'], 
										comando_voz=data['comando_voz'], ajuda_voz=data['ajuda_voz'], nvda=data['nvda'])
						
						return student
					else:
						return False
				except:
					return None
			else:
				return None

	def get_user(self, student_id):
		try:
			return LoginAluno.objects.get(id=student_id)
		except:
			return None