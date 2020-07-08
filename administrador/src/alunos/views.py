from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os, requests, json
from .models import Aluno
from .forms import AlunoForm, AlunoEditForm
from cids.models import Cid

# Create your views here.
@login_required(login_url='login')
def student_list_view(request):
	student_list = Aluno.objects.all()
	context = {
		'student_list': student_list
	}
	return render(request, 'student/list.html', context)

@login_required(login_url='login')
def student_form_view(request, id=0):
	os.environ['NO_PROXY'] = '127.0.0.1'

	if request.method == 'POST':
		if id == 0:
			form = AlunoForm(request.POST, request.FILES)
			edit = False
		else:
			form = AlunoEditForm(request.POST, request.FILES or None)
			edit = True
	
		if form.is_valid():
			data = form.clean_form()
			
			if id == 0:
				if Aluno.objects.filter(email=data['email']) | Aluno.objects.filter(cpf=data['cpf']):
					if Aluno.objects.filter(email=data['email']):
						student = request.POST
						error = 'Já existe estudante com esse e-mail cadastrado'
					else:
						student = request.POST
						error = 'Já existe estudante com esse CPF'
				else:
					try:
						response = requests.post('http://127.0.0.1:5000/api/train', data={'group': 'aluno'}, files={ 'file': data['foto'] })
	
						if response.status_code == 200:
							responseJSON = response.json()

							create_student = Aluno.objects.create(foto=data['foto'], nome=data['nome'], data_nasc=data['data_nasc'], email=data['email'], 
												senha_hash=data['senha'], cpf=data['cpf'], celular=data['celular'], cod_treino=responseJSON['treino'],
												cep=data['cep'], numero=data['numero'], comando_voz=data['comando_voz'],ajuda_voz=data['ajuda_voz'], 
												nvda=data['nvda'], outra_info=data['outra_info'])
							create_student.save()

							for cid in data['cid']:
								create_student.cid.add(Cid.objects.get(pk=cid.pk))

							form = AlunoForm()
							error = None
							return redirect('/alunos/')
						else:
							student = request.POST
							error = 'Foto inválida'

					except:
						form = AlunoForm()
						error = None
						return redirect('/alunos/')
			else:
				try:
					update_student = Aluno.objects.get(id=id)
					
					if request.FILES.get('foto', False):
						update_student.foto = data['foto']

					if request.POST.get('senha') != '':
						update_student.senha_hash = data['senha']

					if len(data['cid']):
						update_student.cid.clear()

						for cid in data['cid']:
							update_student.cid.add(Cid.objects.get(pk=cid.pk))
					
					update_student.nome = data['nome']
					update_student.data_nasc = data['data_nasc']
					update_student.cep = data['cep']
					update_student.celular = data['celular']
					update_student.numero = data['numero']
					update_student.comando_voz = data['comando_voz']
					update_student.ajuda_voz = data['ajuda_voz']
					update_student.nvda = data['nvda']
					update_student.outra_info = data['outra_info']
					update_student.save()

				finally:
					form = AlunoForm()
					error = None
					return redirect('/alunos/')
		else:
			student = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = AlunoForm()
		error = None

		if id == 0:
			student = {
				'foto': None,
				'nome': '',
				'data_nasc': '',
				'email': '',
				'senha': '',
				'cpf': '',
				'celular': '',
				'cep': '',
				'numero': '',
				'comando_voz': '',
				'ajuda_voz': '',
				'nvda': '',
				'outra_info': '',
			}

			edit = False
		else:
			try:
				student = Aluno.objects.get(id=id)
				edit = True
			except:
				return redirect('/alunos/')

	context = {
		'student': student,
		'error': error,
		'edit': edit,
		'cid_list': Cid.objects.all(),
	}

	return render(request, 'student/form.html', context)

@login_required(login_url='login')
def student_delete_view(request, id=0):
	try:
		student = Aluno.objects.get(id=id)
		treino = student.cod_treino
		response = requests.post('http://127.0.0.1:5000/api/delete', data={'faceID': treino})
		if response.status_code == 200:
			student.delete()
	finally:
		return redirect('/alunos/')