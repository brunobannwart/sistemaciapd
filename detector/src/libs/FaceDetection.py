import cv2, os
import numpy as np
from PIL import Image
from .Database import Database
from .models.FaceBundle import FaceBundle

class FaceDetection:
	def __init__(self, resources_dir):
		self.resources_dir = resources_dir
		self.known = []
		self.db = Database()
		
		self.classifier = cv2.CascadeClassifier(os.path.join(resources_dir, 'haarcascade_frontalface_alt2.xml'))
		self.facerecognizer = cv2.face.LBPHFaceRecognizer_create()

		if (os.path.exists(os.path.join(resources_dir, 'train.yml'))):
			self.facerecognizer.read(os.path.join(resources_dir, 'train.yml'))

		else:
			train_from_db = self.db.getTrain(os.path.join(resources_dir, 'train.yml'))
			
			if train_from_db:
				self.facerecognizer.read(os.path.join(resources_dir, 'train.yml'))

		self.__loadFaces()

	def __loadFaces(self):
		faces = self.db.getFaces()

		for face in faces:
			bundle = FaceBundle.parseJSON(self, face)
			self.known.append(bundle)

	def __newFace(self, bundle):
		face = bundle.parseData()
		filename = face['filename']
		group = face['group']

		return self.db.saveFace(filename, group)

	def __parseFaces(self, filepath):
		train = []
		labels = []

		if len(self.known):
			last_known = self.known[-1]
			id_ = last_known.getFaceID() + 1
		else:
			id_ = 1

		img = cv2.imread(filepath)
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray_img = cv2.equalizeHist(gray_img)
		facelist = self.classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)

		for (x, y, w, h) in facelist:
			roi = gray_img[y: y+h, x: x+w]
			train.append(roi)
			labels.append(id_)

		return train, labels

	def addKnownFace(self, filepath, facegroup):
		faces, labels = self.__parseFaces(filepath)

		if len(labels):
			bundle = FaceBundle(os.path.basename(filepath))
			bundle.setGroup(facegroup)
			faceID = self.__newFace(bundle)
			bundle.setFaceID(faceID)

			self.known.append(bundle)
			
			if (os.path.exists(os.path.join(self.resources_dir, 'train.yml'))):
				self.facerecognizer.update(faces, np.array(labels))
				new = False

			else:
				self.facerecognizer.train(faces, np.array(labels))
				train_file = open(os.path.join(self.resources_dir, 'train.yml'), 'w+')
				new = True

			self.facerecognizer.write(os.path.join(self.resources_dir, 'train.yml'))
			self.db.saveTrain(os.path.join(self.resources_dir, 'train.yml'), new)
			return bundle
		else:
			return None

	def removeKnownFace(self, faceID):
		count = 0;
	
		for knownFace in self.known:
			if knownFace.getFaceID() == int(faceID):
				if self.db.deleteFace(faceID):
					self.known.pop(count)
					return True
				else:
					return False
			else:
				count += 1
		return False

	def findMatches(self, filepath, filegroup):
		matches = []

		img = cv2.imread(filepath)
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray_img = cv2.equalizeHist(gray_img)
		facelist = self.classifier.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)

		for (x, y, w, h) in facelist:
			roi = gray_img[y: y+h, x: x+w]
			
			id, conf = self.facerecognizer.predict(roi)

			print('ID treino: ', id)
			print('Confiabilidade: ', conf)

			if conf >= 45 and conf <= 85:
				for known in self.known:
					if known.getFaceID() == id:
						print('Grupo: ', known.getGroup())

						if known.getGroup() == filegroup:
							matches.append(known.parseData())

		return matches