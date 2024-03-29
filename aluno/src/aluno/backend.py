from django.contrib.auth.backends import BaseBackend
from django.db import connection
from core_aluno.models import LoginAluno

class LoginBackend(BaseBackend):
	def authenticate(request, student_email=None, student_senha=None):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, nome, email, senha_hash, ajuda_voz, leitor_tela  FROM aluno WHERE email=%s", [student_email])
			result = cursor.fetchone()

			if result != None:
				data = {
					'id': result[0],
					'nome': result[1],
					'email': result[2],
					'senha_hash': result[3],
					'ajuda_voz': result[4],
					'leitor_tela': result[5],
				}

				try:
					if student_senha == data['senha_hash']:
						if LoginAluno.objects.filter(id=data['id']):
							student_session = LoginAluno.objects.get(id=data['id'])
							student_session.delete()

						student = 	LoginAluno.objects.create(id=data['id'], nome=data['nome'], email=data['email'], senha_hash=data['senha_hash'], 
										ajuda_voz=data['ajuda_voz'], leitor_tela=data['leitor_tela'])
						
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