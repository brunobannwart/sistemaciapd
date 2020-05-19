from django.shortcuts import render, redirect
import os, requests, io
from regex import subf
from pybase64 import urlsafe_b64decode
from PIL import Image
from .forms import LoginForm
from administradores.models import Administrador

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			data = form.clean_form()

			try:
				login_admin = Administrador.objects.get(email=data['email'])

				if login_admin.senha == data['senha']:
					form = LoginForm()
					return redirect('/administradores/')
				else:
					login = request.POST
					error = 'Senha não confere'
			except:
				login = request.POST
				error = 'Não existe administrador com esse e-mail'
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
		url = request.POST['url']
		
		encode = subf('^data:image/png;base64,', '', url)
		decode = urlsafe_b64decode(encode)
		img = Image.open(io.BytesIO(decode))
		#img.show(title='Camera')
		
		photo = io.BytesIO()
		img.save(photo, 'png')
		photo.seek(0)

		#response = requests.post('http://127.0.0.1:5000/api/recognize', files={ 'file': ('photo.png', photo, 'image/png') })

		response = {
			'status_code': 200
		}

		if response.status_code == 200:
			return redirect('/administradores/')
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