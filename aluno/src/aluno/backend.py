from django.contrib.auth.backends import BaseBackend
from django.db import connection

class LoginBackend(BaseBackend):
	def authenticate(request, student_email=None, student_senha=None):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, nome, senha_hash, comando_voz, ajuda_voz, nvda, is_authenticated, last_login  FROM aluno WHERE email=%s", [student_email])
			result = cursor.fetchone()

			if result != None:
				data = {
					'id': result[0],
					'nome': result[1],
					'senha_hash': result[2],
					'comando_voz': result[3],
					'ajuda_voz': result[4],
					'nvda': result[5],
					'is_authenticated': result[6],
					'last_login': result[7]
				}

				if data['senha_hash'] == student_senha:
					cursor.execute("UPDATE aluno SET is_authenticated=%s", [1])
					data['is_authenticated'] = True
					return data
				else:
					return False
			else:
				return None

	def get_user(self, student_id):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id, nome, senha_hash, comando_voz, ajuda_voz, nvda, is_authenticated, last_login FROM aluno WHERE id=%s", [student_id])

			if result != None:
				data = {
					'id': result[0],
					'nome': result[1],
					'senha_hash': result[2],
					'comando_voz': result[3],
					'ajuda_voz': result[4],
					'nvda': result[5],
					'is_authenticated': result[6],
					'last_login': result[7]
				}

				return data
			else:
				return None