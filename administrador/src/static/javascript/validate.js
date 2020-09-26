/*
	Funções para validar CEP 
*/
async function validarCEP(cep_entrada) {
	const container_leitor = document.getElementById('container_leitor');

	if (!container_leitor) {
		exibirResultadoCEP(cep_entrada);
	} else {
		informarResultadoCEP(cep_entrada);
	}
}

async function exibirResultadoCEP(cep_entrada) {
	let cep, cep_valido;
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
	cep_valido = document.getElementById('cep_valido');

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
			  			cep_valido.value = 'sim';

					} else {
						bloco_cep.style.display = 'block';
				  		titulo.style.display = 'block';
				  		erro.style.display = 'block';
				  		titulo.innerHTML = 'Aviso';
				  		erro.innerHTML = 'Informe um CEP válido';
				  		cep_valido.value = 'nao';
					}
				});
			})
			.catch(error => {
				bloco_cep.style.display = 'block';
				titulo.style.display = 'block';
				erro.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				erro.innerHTML = 'Informe um CEP válido';
				cep_valido.value = 'nao';
			});
	}
}

async function informarResultadoCEP(cep_entrada) {
	let cep, cep_valido;
	const exp = /\-|\.|\/|\(|\)| /g

	const opcoes = {
		method: 'GET',
		mode: 'cors',
		cache: 'default'
	}

	cep = cep_entrada.value.replace(exp, '');
	cep_valido = document.getElementById('cep_valido');

	if (cep.length == 8) {
		await fetch(`https://viacep.com.br/ws/${cep}/json/`, opcoes)
			.then(response => {
			 	response.json().then(data => {
			 		if (data.erro != true) {
			 			audio('CEP válido');

			  			cep_valido.value = 'sim';

					} else {
						audio('CEP inválido');
				  		cep_valido.value = 'nao';
					}
				});
			})
			.catch(error => {
				audio('CEP inválido');
				cep_valido.value = 'nao';
			});
	}
}

/*
	Funções para validar CPF 
*/
function validarCPF(cpf_entrada) {
	const container_leitor = document.getElementById('container_leitor');

	if (!container_leitor) {
		exibirResultadoCPF(cpf_entrada);
	} else {
		informarResultadoCPF(cpf_entrada);
	}
}

function exibirResultadoCPF(cpf_entrada) {
	let cpf, cpf_valido, numeros, digitos, soma, i, resultado, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco = document.getElementById('container_document');
	const titulo = document.getElementById('title_document');
	const mensagem = document.getElementById('message_document');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	cpf = cpf_entrada.value.replace(exp, '');
	cpf_valido = document.getElementById('cpf_valido');

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

			if (resultado != digitos.charAt(0)) {
				controle = 0;

			} else {
				numeros = cpf.substring(0, 10);
				soma = 0;

				for (i = 11; i > 1; i--) {
					soma += numeros.charAt(11 - i) * i;
				}

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
			mensagem.innerHTML = 'Informe um CPF válido';
			cpf_valido.value = 'nao';
		} else {
			cpf_valido.value = 'sim';
		}
	}
}

function informarResultadoCPF(cpf_entrada) {
	let cpf, cpf_valido, numeros, digitos, soma, i, resultado, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	cpf = cpf_entrada.value.replace(exp, '');
	cpf_valido = document.getElementById('cpf_valido');

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

			if (resultado != digitos.charAt(0)) {
				controle = 0;

			} else {
				numeros = cpf.substring(0, 10);
				soma = 0;

				for (i = 11; i > 1; i--) {
					soma += numeros.charAt(11 - i) * i;
				}

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
			audio('CPF inválido');
			cpf_valido.value = 'nao';

		} else {
			audio('CPF válido');
			cpf_valido.value = 'sim';
		}
	}
}


/*
	Funções para validar CNPJ 
*/
function validarCNPJ(cnpj_entrada) {
	const container_leitor = document.getElementById('container_leitor');

	if (!container_leitor) {
		exibirResultadoCNPJ(cnpj_entrada);
	} else {
		informarResultadoCNPJ(cnpj_entrada);
	}
}

function exibirResultadoCNPJ(cnpj_entrada) {
	let cnpj, cnpj_valido, posicao, tamanho, numeros, digitos, soma, resultado, i, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	const bloco = document.getElementById('container_document');
	const titulo = document.getElementById('title_document');
	const mensagem = document.getElementById('message_document');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	cnpj = cnpj_entrada.value.replace(exp, '');
	cnpj_valido = document.getElementById('cnpj_valido');

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
			mensagem.innerHTML = 'Informe um CNPJ válido';
			cnpj_valido.value = 'nao';
		} else {
			cnpj_valido.value = 'sim';
		}
	}
}

function informarResultadoCNPJ(cnpj_entrada) {
	let cnpj, cnpj_valido, posicao, tamanho, numeros, digitos, soma, resultado, i, iguais, controle;
	const exp = /\-|\.|\/|\(|\)| /g

	cnpj = cnpj_entrada.value.replace(exp, '');
	cnpj_valido = document.getElementById('cnpj_valido');

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
			audio('CNPJ inválido');
			cnpj_valido.value = 'nao';

		} else {
			audio('CNPJ válido');
			cnpj_valido.value = 'sim';
		}
	}
}

/*
	Funções para validar formulario de estudante
*/
function validarFormularioEstudante() {
	const container_leitor = document.getElementById('container_leitor');

	if (!container_leitor) {
		return exibirValidarFormularioEstudante();
	} else {
		return informarValidarFormularioEstudante();
	}
}

function exibirValidarFormularioEstudante() {
	const cpf = document.forms['formulario_estudante']['cpf_valido'].value;
	const cep = document.forms['formulario_estudante']['cep_valido'].value;
	const botao_submit = document.getElementById('botao_submit');

	const bloco = document.getElementById('container_document');
	const titulo = document.getElementById('title_document');
	const mensagem = document.getElementById('message_document');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	if (cpf == 'sim' && cep == 'sim') {
		botao_submit.disabled = true;
		return true;

	} else {
		if (cpf == 'sim') {
			bloco.style.display = 'block';
			titulo.style.display = 'block';
			mensagem.style.display = 'block';
			titulo.innerHTML = 'Aviso';
			mensagem.innerHTML = 'CEP continua inválido';

		} else {
			if (cep == 'sim') {
				bloco.style.display = 'block';
				titulo.style.display = 'block';
				mensagem.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				mensagem.innerHTML = 'CPF continua inválido';

			} else {
				bloco.style.display = 'block';
				titulo.style.display = 'block';
				mensagem.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				mensagem.innerHTML = 'CPF e CEP continuam inválidos';
			}
		}

		botao_submit.disabled = false;
		return false;
	}
}

function informarValidarFormularioEstudante() {
	const cpf = document.forms['formulario_estudante']['cpf_valido'].value;
	const cep = document.forms['formulario_estudante']['cep_valido'].value;
	const botao_submit = document.getElementById('botao_submit');

	if (cpf == 'sim' && cep == 'sim') {
		audio('Formulário validado');
		botao_submit.disabled = true;
		return true;

	} else {
		if (cpf == 'sim') {
			audio('CEP continua inválido');

		} else {
			if (cep == 'sim') {
				audio('CPF continua inválido');

			} else {
				audio('CPF e CEP continuam inválidos');
			}
		}

		botao_submit.disabled = false;
		return false;
	}
}

/*
	Funções para validar formulario de empresa
*/
function validarFormularioEmpresa() {
	const container_leitor = document.getElementById('container_leitor');

	if (!container_leitor) {
		return exibirValidarFormularioEmpresa();
	} else {
		return informarValidarFormularioEmpresa();
	}
}

function exibirValidarFormularioEmpresa() {
	const cnpj = document.forms['formulario_empresa']['cnpj_valido'].value;
	const cep = document.forms['formulario_empresa']['cep_valido'].value;
	const botao_submit = document.getElementById('botao_submit');

	const bloco = document.getElementById('container_document');
	const titulo = document.getElementById('title_document');
	const mensagem = document.getElementById('message_document');

	bloco.style.display = 'none';
	titulo.style.display = 'none';
	mensagem.style.display = 'none';

	if (cnpj == 'sim' && cep == 'sim') {
		botao_submit.disabled = true;
		return true;

	} else {
		if (cnpj == 'sim') {
			bloco.style.display = 'block';
			titulo.style.display = 'block';
			mensagem.style.display = 'block';
			titulo.innerHTML = 'Aviso';
			mensagem.innerHTML = 'CEP continua inválido';

		} else {
			if (cep == 'sim') {
				bloco.style.display = 'block';
				titulo.style.display = 'block';
				mensagem.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				mensagem.innerHTML = 'CNPJ continua inválido';

			} else {
				bloco.style.display = 'block';
				titulo.style.display = 'block';
				mensagem.style.display = 'block';
				titulo.innerHTML = 'Aviso';
				mensagem.innerHTML = 'CNPJ e CEP continuam inválidos';
			}
		}

		botao_submit.disabled = false;
		return false;
	}
}

function informarValidarFormularioEmpresa() {
	const cnpj = document.forms['formulario_empresa']['cnpj_valido'].value;
	const cep = document.forms['formulario_empresa']['cep_valido'].value;
	const botao_submit = document.getElementById('botao_submit');

	if (cnpj == 'sim' && cep == 'sim') {
		botao_submit.disabled = true;
		return true;

	} else {
		if (cnpj == 'sim') {
			audio('CEP continua inválido');

		} else {
			if (cep == 'sim') {
				audio('CNPJ continua inválido');

			} else {
				audio('CNPJ e CEP continuam inválidos');
			}
		}

		botao_submit.disabled = false;
		return false;
	}
}