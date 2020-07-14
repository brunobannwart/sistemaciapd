class FaceBundle:
	faceID = 0
	filename = ''
	group = ''

	def __init__(self, filename):
		self.filename = filename

	# Metodos set das propriedades
	def setFaceID(self, faceID):
		self.faceID = faceID

	def setGroup(self, group):
		self.group = group

	# Metodos get das propriedades
	def getFaceID(self):
		return self.faceID

	def getGroup(self):
		return self.group

	# Metodos parse de dados

	def parseData(self):
		data = {
			'faceID': self.faceID,
			'filename':	self.filename,
			'group': self.group,
		}

		return data

	def parseJSON(self, faceJSON):
		bundle = FaceBundle(faceJSON['filename'])
		bundle.setFaceID(faceJSON['faceID'])
		bundle.setGroup(faceJSON['group'])
		return bundle