from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection
from .forms import ChangePasswordForm
from .utils import render_to_pdf

# Create your views here.
@login_required(login_url='login')
def changepassword_view(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)

		if form.is_valid():
			if form.cleaned_data.get('senha') == form.cleaned_data.get('confirma'):
				data = form.clean_form()

				with connection.cursor() as cursor:
					cursor.execute("SELECT id, email FROM empresa WHERE email=%s", [data['email']])
					result = cursor.fetchone()

					if result != None:
						company_email = data['email']
						company_senha_hash = data['senha_hash']

						cursor.execute("UPDATE empresa SET senha_hash=%s WHERE email=%s", [company_senha_hash, company_email])
						
						form = ChangePasswordForm()
						error = None
						return redirect('/vagas/')
					else:
						change = request.POST
						error = 'Não existe empresa com esse e-mail'
			else:
				change = request.POST
				error = 'Senhas não conferem'
		else:
			change = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = ChangePasswordForm()
		error = None

		change = {
			'email': '',
			'senha': '',
			'confirma': ''
		}

	context = {
		'change': change,
		'error': error
	}

	return render(request, 'core/company/password.html', context)

@login_required(login_url='login')
def student_list_view(request):
	student_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM aluno ORDER BY nome ASC")
		results = cursor.fetchall()

		for row in results:
			student = {
				'id': row[0],
				'foto': settings.MEDIA_URL + row[1],
				'nome': row[2],
				'data_nasc': row[3],
				'email': row[4],
				'cpf': row[6],
				'celular': row[7],
				'cep': row[8],
				'numero': row[9],
				'outra_info': row[12],
				'instituicao_ensino': row[13],
				'curso_extra': row[14],
				'empresa': row[15],
				'cargo': row[16],
				'laudo_medico': row[17],
			}
			student_list.append(student)
	
	context = {
		'student_list': student_list
	}

	return render(request, 'core/student/list.html', context)

@login_required(login_url='login')
def student_read_view(request, id=0):
	if id != 0:	
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM aluno WHERE id=%s", [id])
			result = cursor.fetchone()

			if result != None:
				cursor.execute("SELECT * FROM aluno_cid WHERE aluno_id=%s", [id])
				results_alunos_cids = cursor.fetchall()
				cids = []

				for result_aluno_cid in results_alunos_cids:
					cid_id = result_aluno_cid[2]

					cursor.execute("SELECT * FROM cid WHERE id=%s", [cid_id])
					result_cid = cursor.fetchone()

					if result_cid != None:
						cid = {
							'id': result_cid[0],
							'codigo': result_cid[1],
							'descricao': result_cid[2],
						}

						cids.append(cid)

				if result[17] != '':
					link_laudo = settings.MEDIA_URL + result[17]
				else:
					link_laudo = None

				student = {
					'id': result[0],
					'foto':	settings.MEDIA_URL + result[1],
					'nome': result[2],
					'data_nasc': result[3],
					'email': result[4],
					'cpf': result[6],
					'cep': result[8],
					'numero': result[9],
					'cid': cids,
					'outra_info': result[12],
					'instituicao_ensino': result[13],
					'curso_extra': result[14],
					'empresa': result[15],
					'cargo': result[16],
					'laudo_medico': link_laudo,
				}
		
				context = {
					'student': student
				}

				return render(request, 'core/student/read.html', context)
			else:
				return redirect('/candidatos/')
	else:
		return redirect('/candidatos/')

@login_required(login_url='login')
def student_pdf_view(request, id=0):		
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM aluno WHERE id=%s", [id])
			result = cursor.fetchone()

			if result != None:
				cursor.execute("SELECT * FROM aluno_cid WHERE aluno_id=%s", [id])
				results_alunos_cids = cursor.fetchall()
				cids = []

				for result_aluno_cid in results_alunos_cids:
					cid_id = result_aluno_cid[2]

					cursor.execute("SELECT * FROM cid WHERE id=%s", [cid_id])
					result_cid = cursor.fetchone()

					if result_cid != None:
						cid = {
							'id': result_cid[0],
							'codigo': result_cid[1],
							'descricao': result_cid[2],
						}

						cids.append(cid)

				student = {
					'id': result[0],
					'foto':	settings.MEDIA_ROOT + '/' + result[1],
					'nome': result[2],
					'data_nasc': result[3],
					'email': result[4],
					'cpf': result[6],
					'celular': result[7],
					'cep': result[8],
					'numero': result[9],
					'cid': cids,
					'outra_info': result[12],
					'instituicao_ensino': result[13],
					'curso_extra': result[14],
					'empresa': result[15],
					'cargo': result[16],
				}
		
				context = {
					'student': student
				}

				pdf = render_to_pdf('core/student/pdf.html', context)

				if pdf:
					response = HttpResponse(pdf, content_type='application/pdf')
					filename = result[2].replace(' ', '_').lower() + '.pdf'
					content = 'inline; filename=%s' % (filename)
					response['Content-Disposition'] = content
					return response
				else:
					return redirect('/candidatos/{0}'.format(id))

				return pdf
			else:
				return redirect('/candidatos/')
	else:
		return redirect('/candidatos/')
