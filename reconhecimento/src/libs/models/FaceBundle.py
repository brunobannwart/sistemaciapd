import numpy as np

class FaceBundle:
	faceID = 0
	filename = ''
	location = []
	encodings = []
	landmarks = []
	group = ''

	def __init__(self, filename):
		self.filename = filename

	# Metodos set das propriedades
	def setFaceID(self, faceID):
		self.faceID = faceID

	def setLocation(self, location):
		self.location = location

	def setEncodings(self, encodings):
		self.encodings = encodings

	def setLandMarks(self, landmarks):
		self.landmarks = landmarks

	def setGroup(self, group):
		self.group = group

	# Metodos get das propriedades
	def getFaceID(self):
		return self.faceID

	def getLocation(self):
		return self.location

	def getEncodings(self):
		return self.encodings

	def getLandMarks(self):
		return self.landmarks

	def getGroup(self):
		return self.group

	# Metodos parse de dados

	def parseData(self):
		data = {
			'faceID': self.faceID,
			'filename':	self.filename,
			'location': self.location,
			'encoding': self.encodings.tolist(),
			'landmark':	self.landmarks,
			'group': self.group,
		}

		return data

	def parseJSON(self, faceJSON):
		bundle = FaceBundle(faceJSON['filename'])
		bundle.setFaceID(faceJSON['faceID'])
		bundle.setLocation(faceJSON['location'])
		bundle.setEncodings(np.array(faceJSON['encoding']))
		bundle.setLandMarks(faceJSON['landmark'])
		bundle.setGroup(faceJSON['group'])
		return bundle