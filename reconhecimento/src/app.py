from flask import Flask, json, Response, request
from werkzeug.utils import secure_filename
from libs.FaceRecognition import FaceRecognition
from libs.models.FaceBundle import FaceBundle
from os import path, remove

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config.from_object("config.Config")
app.face = FaceRecognition()

def handle_sucess(output, status=200, mimetype='application/json'):
	return Response(output, status=status, mimetype=mimetype)

def handle_error(output, status=500, mimetype='application/json'):
	return Response(json.dumps({ 'error': output }), status=status, mimetype=mimetype)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Treinamento de Face
@app.route('/api/train', methods=['POST'])
def train_face():
	output = json.dumps({ 'sucess': True })
	face_group = request.form['group']

	if 'file' not in request.files:
		return handle_error('Requer imagem')

	else:
		file = request.files['file']

		if not allowed_file(file.filename):
			return handle_error('Imagens suportadas: *.png , *.jpg')
		else:
			filename = secure_filename(file.filename)
			base_dir = path.abspath(path.dirname(__file__))
			train_storage = path.join(base_dir, 'assets/train')
			file_path = path.join(train_storage, filename)
			file.save(file_path)
			
			bundle = app.face.addKnownFace(file_path, face_group)
			remove(file_path)

			if bundle != None:
				#output = json.dumps({ 'treino': bundle.getFaceID() })
				return handle_sucess(output)
			else:
				return handle_error('Nenhuma face encontrada na imagem')

# Reconhecimento de Face
@app.route('/api/recognize', methods=['POST'])
def recognize_face():
	output = json.dumps({ 'sucess': True })
	face_group = request.form['group']

	if 'file' not in request.files:
		return handle_error('Requer imagem')

	else:
		file = request.files['file']

		if not allowed_file(file.filename):
			return handle_error('Extensão não suportada')
		else:
			filename = secure_filename(file.filename)
			base_dir = path.abspath(path.dirname(__file__))
			train_storage = path.join(base_dir, 'assets/recognize')
			file_path = path.join(train_storage, filename)
			file.save(file_path)

			matches = app.face.findMatches(file_path, face_group)
			remove(file_path)

			if len(matches):
				faceMatched = matches[0]
				#output = json.dumps({ 'reconhecimento': faceMatched['faceID'] })

				return handle_sucess(output)
			else:
				return handle_error('Face não reconhecida na imagem.')

# Excluir face armazenada
@app.route('/api/delete', methods=['POST'])
def delete_face():
	output = json.dumps({ 'success': True })

	faceid = request.form['faceID']
	app.face.removeKnownFace(faceid)
	return handle_sucess(output)

app.run(host=app.config['FLASK_RUN_HOST'], port=app.config['FLASK_RUN_PORT'])