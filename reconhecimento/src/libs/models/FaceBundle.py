import numpy as np

class FaceBundle:
	faceID = ''
	filename = ''
	location = []
	encodings = []
	landmarks = []
	known = False
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

	def setKnownFace(self, value):
		self.known = value

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

	def getKnownFace(self):
		return self.known

	def getLandMarks(self):
		return self.landmarks

	def getGroup(self):
		return self.group

	# Metodos parse de dados

	def parseData(self):
		data = {
			'faceID': self.faceID,
			'filename':	self.filename,
			'known': self.known,
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