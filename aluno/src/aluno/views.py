#from django.http import HttpResponse
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
				cursor.execute("SELECT id, email, senha FROM aluno WHERE email=%s", [data['email']])  
				result = cursor.fetchone()

				student = {
					'id': result[0],
					'email': result[1],
					'senha': result[2]
				}

				if student.senha == data['senha']:
					form = LoginForm()
					return redirect('/inicio/')
				else:
					login = request.POST
					error = 'Senha não confere'
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
		
		photo = io.BytesIO()
		img.save(photo, 'png')
		photo.seek(0)

		response = requests.post('http://127.0.0.1:5000/api/recognize', files={ 'file': ('photo.png', photo, 'image/png') })

		if response.status_code == 200:
			return redirect('/inicio/')
		else:
			return redirect('login')

	return render(request, 'login/camera.html', {})

def home_view(request):
	return render(request, 'options/index.html', {})

def logout_view (request):
	try:
		del request.session['email']
	finally:
		return redirect('login')