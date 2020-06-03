# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.db import connection
import os, requests, io
from regex import subf
from pybase64 import urlsafe_b64decode
from PIL import Image
from .forms import LoginForm
from .backend import LoginBackend
from core.models import LoginEmpresa

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			data = form.clean_form()
			login_company = LoginBackend.authenticate(request, data['email'], data['senha_hash'])

			if login_company != None and login_company != False:
				login_company.is_authenticated = True
				login_company.save()
				form = LoginForm()
				login(request, login_company, backend='empresa.backend.LoginBackend')
				return redirect('/vagas/')
			else:
				if login_company == False: 
					login_form = request.POST
					error = 'Senha não confere'
				else:
					login_form = request.POST
					error = 'Não existe empresa com esse e-mail'
		else:
			login_form = request.POST
			error = 'Preencher campos de login corretamente'
	else:
		form = LoginForm()
		error = None

		login_form = {
			'email': '',
			'senha': '',
		}

	context = {
		'login': login_form,
		'error': error,
	}
	return render(request, 'login/index.html', context)

def camera_view(request):
	os.environ['NO_PROXY'] = '127.0.0.1'

	if request.method == 'POST':
		url_img = request.POST['url']
		img_encode = subf('^data:image/png;base64,', '', url_img)
		img_decode = urlsafe_b64decode(img_encode)
		img = Image.open(io.BytesIO(img_decode))
		photo = io.BytesIO()
		img.save(photo, 'png')
		photo.seek(0)

		response = requests.post('http://127.0.0.1:5000/api/recognize', data={'group': 'empresa'}, files={ 'file': ('photo.png', photo, 'image/png') })

		if response.status_code == 200:
			responseJSON = response.json()
			company_codigo = responseJSON['reconhecimento']

			with connection.cursor() as cursor:
				cursor.execute("SELECT id, email, senha_hash FROM empresa WHERE cod_treino=%s", [company_codigo])
				result = cursor.fetchone()

				if result != None:
					data = { 'id': result[0], 'email': result[1], 'senha_hash': result[2] }
					login_company = LoginBackend.authenticate(request, data['email'], data['senha_hash'])

					if login_company != None and login_company != False:
						login_company.is_authenticated = True
						login_company.save()
						login(request, login_company, backend='empresa.backend.LoginBackend')
						return redirect('/vagas/')
					else:
						return redirect('login')
				else:
					return redirect('login')
		else:
			return redirect('login')
	
	return render(request, 'login/camera.html', {})

def readmore_view(request):
	return render(request, 'login/readmore.html', {})

def forgot_view(request):
	return render(request, 'login/forgot.html', {})

def logout_view (request):
	try:
		logout_email = request.user.email
		logout(request)
		company_session = LoginEmpresa.objects.get(email=logout_email)
		company_session.delete()
	finally:
		return redirect('login')
