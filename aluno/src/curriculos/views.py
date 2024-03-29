from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import Curriculo
from .forms import CurriculoForm

# Create your views here.
@login_required(login_url='login')
@csrf_protect
def curriculum_form_view(request):
	if request.method == 'POST':
		form = CurriculoForm(request.POST, request.FILES or None)

		if form.is_valid():
			data = form.clean_form()
			try:
				if data['instituicao_ensino'] != '' or data['curso_extra'] != '' or data['empresa'] != '' or data['cargo'] != '' or data['laudo_medico']:
					curriculum = Curriculo.objects.create(aluno_id=request.user.id, instituicao_ensino=data['instituicao_ensino'], 
									curso_extra=data['curso_extra'], empresa=data['empresa'], 
									cargo=data['cargo'], laudo_medico=data['laudo_medico'])
					curriculum.save()

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
			'instituicao_ensino': '',
			'curso_extra': '', 
			'empresa': '',
			'cargo': '',
		}

	context = {
		'curriculum': curriculum,
		'error': error
	}

	context.update(csrf(request))
	return render(request, 'options/curriculum/form.html', context)