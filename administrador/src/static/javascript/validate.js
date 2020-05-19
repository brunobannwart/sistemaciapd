async function validarCEP(cep_entrada) {
	let cep;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco_cep = document.getElementById('container');
	const titulo = document.getElementById('title');
	const logradouro = document.getElementById('address');
	const bairro	=	document.getElementById('district');
	const localidade = document.getElementById('city');
	const uf = document.getElementById('uf');
	const erro = document.getElementById('error');

	bloco_cep.style.display = 'none';
	titulo.style.display = 'none';
	logradouro.style.display = 'none';
	bairro.style.display = 'none';
	localidade.style.display = 'none';
	uf.style.display = 'none';
	erro.style.display = 'none';

	const opcoes = {
		method: 'GET',
		mode: 'cors',
		cache: 'default'
	}

	cep = cep_entrada.value.replace(exp, '');

	if (cep.length == 8) {
		await fetch(`https://viacep.com.br/ws/${cep}/json/`, opcoes)
			.then(response => {
			 	response.json().then(data => {
			 		if (data.erro != true) {
			  			bloco_cep.style.display = 'block';
			  			titulo.style.display = 'block';
			  			logradouro.style.display = 'block';
						bairro.style.display = 'block';
						localidade.style.display = 'block';
						uf.style.display = 'block';
			  			titulo.innerHTML = 'CEP';
			  			logradouro.innerHTML = data.logradouro;
			  			bairro.innerHTML = data.bairro;
			  			localidade.innerHTML = data.localidade;
			  			uf.innerHTML = data.uf;
					} else {
						bloco_cep.style.display = 'block';
				  		titulo.style.display = 'block';
				  		erro.style.display = 'block';
				  		titulo.innerHTML = 'Aviso';
				  		erro.innerHTML = 'Informe um CEP válido';
					}
				});
			})
			.catch(error => {
				bloco_cep.style.display = 'block';
				titulo.style.display = 'block';
				erro.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				erro.innerHTML = 'Informe um CEP válido';
			});
	}
}

function validarCPF(cpf_entrada) {
	let cpf, numeros, digitos, soma, i, resultado, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco = document.getElementById('container_document');
	const titulo = document.getElementById('title_document');
	const mensagem = document.getElementById('message_document');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	cpf = cpf_entrada.value.replace(exp, '');

	if (cpf.length == 11) {
		controle = 0;
		iguais = 1;

		for (i = 0; i < cpf.length - 1; i++) {
			if (cpf.charAt(i) != cpf.charAt(i + 1)) {
				iguais = 0;
				break;
			}
		}

		if (!iguais) {
			numeros = cpf.substring(0, 9);
			digitos = cpf.substring(9);
			soma = 0;

			for (i = 10; i > 1; i--) {
				soma += numeros.charAt(10 - i) * i;
			}

			resultado = (soma * 10) % 11;
			//resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;

			if (resultado != digitos.charAt(0)) {
				controle = 0;

			} else {
				numeros = cpf.substring(0, 10);
				soma = 0;

				for (i = 11; i > 1; i--) {
					soma += numeros.charAt(11 - i) * i;
				}

				//resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
				resultado = (soma * 10) % 11;

				if (resultado != digitos.charAt(1)) {
					controle = 0;
				} else {
					controle = 1;
				}
			}
		} else {
			controle = 0;
		}

		if (!controle) {
			bloco.style.display = 'block';
			titulo.style.display = 'block';
			mensagem.style.display = 'block';
			titulo.innerHTML = 'Aviso';
			mensagem.innerHTML = 'Informe um CPF válido'
		}
	}
}

function validarCNPJ(cnpj_entrada) {
	let cnpj, posicao, tamanho, numeros, digitos, soma, resultado, i, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco = document.getElementById('container_document');
	const titulo = document.getElementById('title_document');
	const mensagem = document.getElementById('message_document');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	cnpj = cnpj_entrada.value.replace(exp, '');

	if (cnpj.length == 14) {
		controle = 0;
		iguais = 1;

		for (i = 0; i < cnpj.length - 1; i++) {
			if (cnpj.charAt(i) != cnpj.charAt(i + 1)) {
				iguais = 0;
				break;
			}
		}

		if (!iguais) {
			tamanho = cnpj.length - 2;
			numeros = cnpj.substring(0, tamanho);
			digitos = cnpj.substring(tamanho);
			soma = 0;
			posicao = tamanho - 7;

			for (i = tamanho; i >= 1; i--) {
				soma += numeros.charAt(tamanho - i) * posicao--;
				if (posicao < 2) {
					posicao = 9;
				}
			}

			resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;

			if (resultado != digitos.charAt(0)) {
				controle = 0;

			} else {
				tamanho += 1;
				numeros = cnpj.substring(0, tamanho);
				soma = 0;
				posicao = tamanho - 7;

				for (i = tamanho; i >= 1; i--) {
					soma += numeros.charAt(tamanho - i) * posicao--;
					if (posicao < 2) {
						posicao = 9;
					}
				}

				resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;

				if (resultado != digitos.charAt(1)) {
          			controle = 0;

				} else {
					controle = 1;
				}
			}

		} else {
			controle = 0;
		}

		if (!controle) {
			bloco.style.display = 'block';
			titulo.style.display = 'block';
			mensagem.style.display = 'block';
			titulo.innerHTML = 'Aviso';
			mensagem.innerHTML = 'Informe um CNPJ válido'
		}
	}
}