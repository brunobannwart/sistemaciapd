/* 	Language code: pt-BR
 	Voice name: pt-BR-Standard-A
 	SSML Gender: FEMALE
*/

(function() {
	gapi.load('client:auth2', function() {
		gapi.auth2.init({
			client_id: 'YOUR_CLIENT_ID',
		});
	});
})();

function autenticarAjuda() {
	return gapi.auth2.getAuthInstance()
		.signIn({
			scope: 'https://www.googleapis.com/auth/cloud-platform',
		});
}

function clienteAjuda() {
	gapi.client.setApiKey('YOUR_API_KEY');

	return gapi.client.load('https://texttospeech.googleapis.com/$discovery/rest?version=v1')
}

function ajudaPorVoz(texto) {
	let bloco_audio = document.createDocumentFragment();

	autenticarAjuda().then(clienteAjuda);

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
		let som = new Audio('data:audio/mp3;base64,' + response.audioContent);
		bloco_audio.appendChild(som);

		som.addEventListener('ended', function() {
			bloco_audio.removeChild(som);
		});

		som.play();
	});

	bloco_audio = null;
}