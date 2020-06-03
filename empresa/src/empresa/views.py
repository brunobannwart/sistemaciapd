# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
import os, requests, io
from regex import subf
from pybase64 import urlsafe_b64decode
from PIL import Image
from .forms import LoginForm

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			data = form.clean_form()

			with connection.cursor() as cursor:
				cursor.execute("SELECT id, email, senha_hash FROM empresa WHERE email=%s", [data['email']])
				result = cursor.fetchone()

				if result != None:
					login_company = {
						'id': result[0],
						'email': result[1],
						'senha': result[2],
					}

					if login_company.senha_hash == data['senha']:
						#request.session['email'] = login_company.email
						form = LoginForm()
						return redirect('/vagas/')
					else:
						login = request.POST
						error = 'Senha não confere'
				else:
					login = request.POST
					error = 'Não existe empresa com esse e-mail'
		else:
			login = request.POST
			error = 'Preencher campos de login corretamente'
	else:
		form = LoginForm()
		error = None

		login = {
			'email': '',
			'senha': '',
		}

	context = {
		'login': login,
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
				cursor.execute("SELECT id, email FROM empresa WHERE cod_treino=%s", [company_codigo])
				result = cursor.fetchone()

				if result != None:
					login_company = {
						'id': result[0],
						'email': result[1],
					}
					#request.session['email'] = login_company.email
					return redirect('/vagas/')
				else:
					return redirect('login')

			return redirect('/vagas/')
		else:
			return redirect('login')
	
	return render(request, 'login/camera.html', {})

def readmore_view(request):
	return render(request, 'login/readmore.html', {})

def forgot_view(request):
	return render(request, 'login/forgot.html', {})

def logout_view (request):
	try:
		del request.session['email']
	finally:
		return redirect('login')
