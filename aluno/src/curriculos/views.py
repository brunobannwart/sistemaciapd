from django.shortcuts import render, redirect
from .models import Curriculo
from .forms import CurriculoForm

# Create your views here.
def curriculum_form_view(request):
	if request.method == 'POST':
		form = CurriculoForm(request.POST)

		if form.is_valid():
			data = form.clean_form()
			try:
				#curriculum = Curriculo.objects.create(email_aluno=, intituicao_ensino=data['intituicao_ensino'], curso_extra=data['curso_extra'], 
				#				empresa=data['empresa'], cargo=data['cargo'])
				#curriculum.save()
				return redirect('/inicio/')
			except:
				curriculum = request.POST
				error = 'Não foi possível enviar currículo'
		else:
			curriculum = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = CurriculoForm()
		error = None
		
		curriculum = {
			'intituicao_ensino': '',
			'curso_extra': '', 
			'empresa': '',
			'cargo': '',
		}

	context = {
		'curriculum': curriculum,
		'error': error
	}

	return render(request, 'options/curriculum/form.html', context)