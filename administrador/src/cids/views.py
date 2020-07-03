from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cids.models import Cid
import os, requests, json

# Create your views here.
@login_required(login_url='login')
def cid_list_view(request):
	cid_count = Cid.objects.count()
	category = ['F', 'G', 'H', 'M', 'Q']

	if cid_count == 0:
		response = requests.get('https://cid10-api.herokuapp.com/cid10')
		list_cid = response.json()

		for cid in list_cid:
			cid_code = cid['codigo']
			cid_description = cid['nome']
			capital_letter = cid_code[0].upper()

			if capital_letter in category:
				create_cid = Cid.objects.create(codigo=cid_code, descricao=cid_description)
				create_cid.save()

	return redirect('/curriculos/')