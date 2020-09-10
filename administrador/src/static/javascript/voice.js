/* 	Language code: pt-BR
 	Voice name: pt-BR-Standard-A
 	SSML Gender: FEMALE

 	clientId: 426586612708-cedaaiu9nk1472hlfck6noqfi86s8n7s.apps.googleusercontent.com
 	apiKey: AIzaSyDEcVrhOsPCxa8Yc8Ze0ggux8YkdhghLoc
 	scope: https://www.googleapis.com/auth/cloud-platform
 	discovery: https://texttospeech.googleapis.com/$discovery/rest?version=v1
*/

let GoogleAuth, autenticado, ocupado;

function carregarCliente() {
	ocupado = false;
	gapi.load('client:auth2', iniciarCliente);
}

function iniciarCliente() {
	gapi.client.init({
		'apiKey': 'AIzaSyDEcVrhOsPCxa8Yc8Ze0ggux8YkdhghLoc',
		'clientId': '426586612708-cedaaiu9nk1472hlfck6noqfi86s8n7s.apps.googleusercontent.com',
		'scope': 'https://www.googleapis.com/auth/cloud-platform',
		'discoveryDocs': ['https://texttospeech.googleapis.com/$discovery/rest?version=v1'],
	})
	.then(function() {
		GoogleAuth = gapi.auth2.getAuthInstance();
		GoogleAuth.isSignedIn.listen(atualizarStatus);
		atualizarStatus(GoogleAuth.isSignedIn.get());
	});
}

function atualizarStatus(logado) {
	if (logado) {
		autenticado = true;
	} else {
		autenticado = false;
	}
}

function ajudaVoz(texto) {
	let bloco_audio = document.getElementById('ajuda_audio');

	if (!ocupado) {
		ocupado = true;
		
		gapi.client.texttospeech.text.synthesize({
		 	'resource': {
		 		'input': {
		 			'text': texto,
		 		},
		 		'voice': {
		 			'languageCode': 'pt-BR',
		 			'name': 'pt-BR-Standard-A',
		 			'ssmlGender': 'FEMALE',
		 		},
		 		'audioConfig': {
		 			'audioEncoding': 'MP3',
		 			'pitch': 0,
		 			'sampleRateHertz': 0,
		 			'speakingRate': 0,
		 			'volumeGainDb': 0,
		 		},
		 	},
		})
		.then(function(response) {	
		 	let som = new Audio('data:audio/mp3;base64,' + response.result.audioContent);
		
		 	bloco_audio.appendChild(som);

	 		som.addEventListener('ended', function() {
	 			ocupado = false;
		 		bloco_audio.removeChild(som);
		 	});

			som.play();
		})
		.catch(function(error) {
			ocupado = false;
		});
	}
}