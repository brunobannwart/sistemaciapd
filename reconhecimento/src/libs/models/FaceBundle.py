import numpy as np

class FaceBundle:
	faceID = 0
	filename = ''
	encodings = []
	group = ''

	def __init__(self, filename):
		self.filename = filename

	# Metodos set das propriedades
	def setFaceID(self, faceID):
		self.faceID = faceID

	def setEncodings(self, encodings):
		self.encodings = encodings

	def setGroup(self, group):
		self.group = group

	# Metodos get das propriedades
	def getFaceID(self):
		return self.faceID

	def getEncodings(self):
		return self.encodings

	def getGroup(self):
		return self.group

	# Metodos parse de dados

	def parseData(self):
		data = {
			'faceID': self.faceID,
			'filename':	self.filename,
			'encoding': self.encodings.tolist(),
			'group': self.group,
		}

		return data

	def parseJSON(self, faceJSON):
		bundle = FaceBundle(faceJSON['filename'])
		bundle.setFaceID(faceJSON['faceID'])
		bundle.setGroup(faceJSON['group'])
		enconding_list = np.array(faceJSON['encoding'])
		bundle.setEncodings(enconding_list.astype(np.float))
		return bundle