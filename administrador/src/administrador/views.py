from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
import os, requests, io
from regex import subf
from pybase64 import urlsafe_b64decode
from PIL import Image
from .forms import LoginForm
from administradores.models import Administrador
from .backend import LoginBackend

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			data = form.clean_form()
			login_admin = LoginBackend.authenticate(request, data['email'], data['senha'])

			if login_admin != None and login_admin != False:
				login_admin.is_authenticated = True
				login_admin.save()
				form = LoginForm()
				login(request, login_admin, backend='administrador.backend.LoginBackend')
				return redirect('/administradores/')
			else:
				if login_admin == False:
					login_form = request.POST
					error = 'Senha não confere'
				else:
					login_form = request.POST
					error = 'Não existe administrador com esse e-mail'
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
		url = request.POST['url']
		
		encode = subf('^data:image/png;base64,', '', url)
		decode = urlsafe_b64decode(encode)
		img = Image.open(io.BytesIO(decode))
		#img.show(title='Camera')
		photo = io.BytesIO()
		img.save(photo, 'png')
		photo.seek(0)

		response = requests.post('http://127.0.0.1:5000/api/recognize', data={'group': 'administrador'}, files={ 'file': ('photo.png', photo, 'image/png') })

		if response.status_code == 200:
			responseJSON = response.json()
			admin_codigo = responseJSON['reconhecimento']

			try:
				admin_train = Administrador.objects.get(cod_treino=admin_codigo)
				login_admin = LoginBackend.authenticate(request, admin_train.email, admin_train.senha_hash)

				if login_admin != None and login_admin != False:
					#request.session['email'] = login_admin.email
					login(request, login_admin)
					return redirect('/administradores/')
				else:
					return redirect('login')
			except:
				return redirect('login')
		else:
			return redirect('login')

	return render(request, 'login/camera.html', {})

def readmore_view(request):
	return render(request, 'login/readmore.html', {})

def forgot_view(request):
	return render(request, 'login/forgot.html', {})

def logout_view (request):
	logout(request)
	return redirect('login')