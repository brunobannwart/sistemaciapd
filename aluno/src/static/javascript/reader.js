'use strict';

let lista_elementos = [];
let index_atual = 0;

const mapeamentos = {
	a: 'link', 
	button: 'button',
	h1: 'heading',
	h2: 'heading',
	h3: 'heading', 
	h4: 'heading', 
	h5: 'heading', 
	h6: 'heading', 
	strong: 'heading',
	p: 'paragraph',
	small: 'paragraph',
	html: 'page',
	img: 'image',
	nav: 'nav',
	ul: 'ul',
	label: 'label',
	input: 'input',
	textarea: 'textarea',
};

const narradores = {
	page(elemento) {
		const titulo = elemento.querySelector('title').textContent;
		audio(`Página ${titulo}`);
	},

	link(elemento) {
		audio(`Link, ${acessibilidade(elemento)}. Para acessar o link, pressione ENTER`);
	},

	button(elemento) {
		audio(`Botão, ${acessibilidade(elemento)}. Para clicar no botão, pressione ENTER`);
	},

	heading(elemento) {
		audio(`${acessibilidade(elemento)}`);
	},

	paragraph(elemento) {
		audio(elemento.textContent);
	},

	image(elemento) {
		audio(`Imagem, ${acessibilidade(elemento)}`);
	},

	nav(elemento) {
		audio(`Barra de navegação`);
	},

	ul(elemento) {
		const quantidade = $(elemento).children('li').length;
		let texto_lista;

		if (quantidade > 1) {
			texto_lista = 'itens';
		} else {
			texto_lista = 'item;'
		}

		audio(`Lista com ${quantidade} ${texto_lista}`);
	},

	label(elemento) {
		const texto_label = acessibilidade(elemento);
		let texto_obrigatorio;

		if (texto_label.includes('*')) {
			texto_obrigatorio = 'Campo obrigatório';
		} else {
			texto_obrigatorio = '';
		}

		audio(`${acessibilidade(elemento)}. ${texto_obrigatorio}`);
	},

	input(elemento) {
		const texto_entrada = $(elemento)[0].value;
		const texto_formulario = $(elemento)[0].placeholder;

		if (texto_entrada !== '') {
			audio(`Texto de entrada, ${texto_entrada}`);
		} else {
			audio(`Texto de entrada, ${texto_formulario}`);
		}
	},

	textarea(elemento) {
		const texto_entrada = $(elemento)[0].value;
		const texto_formulario = $(elemento)[0].placeholder;

		if (texto_entrada !== '') {
			audio(`Caixa de texto, ${texto_entrada}`);
		} else {
			audio(`Caixa de texto, ${texto_formulario}`);
		}
	},

	default(elemento) {
		audio(`${elemento.tagName}, ${acessibilidade(elemento)}`);
	}
};

$(document).ready(function() {
	const todos = $("*");
	let atual;

	lista_elementos = [];
	index_atual = 0;

	for (let i = 0; i < todos.length; i += 1) {
		atual = todos[i];

		if (existeAudio(atual)) {
			lista_elementos.push(atual);
		}
	}

	for (let i = 0; i < lista_elementos.length; i += 1) {
		atual = lista_elementos[i];
		atual.setAttribute('tabindex', i);
		lista_elementos[i] = atual;
	}
});

function existeAudio(elemento) {
	const lista_tags = [
		'html', 
		'h1', 
		'h2', 
		'h3', 
		'h4', 
		'h5', 
		'h6', 
		'p', 
		'button',
		'img',
		'nav',
		'a',
		'ul',
		'strong',
		'small',
		'input',
		'textarea',
		'label',
	];

	for (let i = 0; i < lista_tags.length; i += 1) {
		if ($(elemento)[0].tagName.toLowerCase() === lista_tags[i]) {
			if ($(elemento)[0].ariaHidden !== 'true' && 
				$(elemento)[0].style.display !== 'none' && $(elemento)[0].type !== 'hidden') {
					return true;
			}
		}
	}

	return false;
}

function moverFoco(offset) {
	const ultimo = document.querySelector('.leitor-selecionar');

	if (ultimo) {
		ultimo.classList.remove('leitor-selecionar');
	}

	if (offset instanceof HTMLElement) {
		index_atual = lista_elementos.findIndex(function(elemento) {
			return elemento === offset;
		});

		return focarElemento(offset);
	}

	index_atual = index_atual + offset;

	if (index_atual < 0) {
		index_atual = lista_elementos.length - 1;

	} else {
		if (index_atual > lista_elementos.length - 1) {
			index_atual = 0;
		}
	}

	focarElemento(lista_elementos[index_atual]);
}

function focarElemento(elemento) {
	if (elemento === document.body) {
		elemento = document.documentElement;
	}

	elemento.classList.add('leitor-selecionar');
	elemento.focus();

	anunciarElemento(elemento);
}

function obterElementoAtivo() {
	if (document.activeElement && document.activeElement !== document.body) {
		return document.activeElement;
	}

	return lista_elementos[0];
}

function anunciarElemento(elemento) {
	const funcionalidade = verificaFuncionalidade(elemento);

	if (narradores[funcionalidade]) {
		narradores[funcionalidade](elemento);
	} else {
		narradores.default(elemento);
	}
}

function verificaFuncionalidade(elemento) {
	const nome = elemento.tagName.toLowerCase();

	if (elemento.getAttribute('role')) {
		return elemento.getAttribute('role');
	}

	return mapeamentos[nome] || 'default';
}

function acessibilidade(elemento) {
	const conteudo = elemento.textContent.trim();

	if (elemento.getAttribute('aria-label')) {
		return elemento.getAttribute('aria-label');
	} else {
		if (elemento.getAttribute('alt')) {
			return elemento.getAttribute('alt');
		}
	}

	return conteudo;
}

function audio(texto, funcao_retorno=null) {
	const sintetizador = new SpeechSynthesisUtterance(texto);	
	sintetizador.lang = 'pt-BR';

	if (funcao_retorno) {
		sintetizador.onend = funcao_retorno;
	}

	speechSynthesis.cancel();
	speechSynthesis.speak(sintetizador);
}

function tratarEventoLeitor(evt) {
	const controle_leitor = document.getElementById('controle_leitor');

	if (!controle_leitor || controle_leitor.checked) {
		if (evt.ctrlKey && evt.which === 39) {
			moverFoco(1);

		} else {
			if (evt.ctrlKey && evt.which === 37) {
				moverFoco(-1);

			} else {
				if (evt.which === 9) {
					moverFoco(obterElementoAtivo());
				}
			}
		}
	} else {
		const ultimo = document.querySelector('.leitor-selecionar');

		if (ultimo) {
			ultimo.classList.remove('leitor-selecionar');
		}

		index_atual = 0;
	}
}

document.addEventListener('keydown', tratarEventoLeitor);