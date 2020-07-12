import cv2, face_recognition, os, pickle
import numpy as np
from .Database import Database
from .models.FaceBundle import FaceBundle

class FaceRecognition:
	def __init__(self, tolerance=0.6):
		self.tolerance = tolerance
		self.known = []
		self.db = Database()
		self.__loadFaces()

	def __loadFaces(self):
		faces = self.db.getFaces()

		for face in faces:
			bundle = FaceBundle.parseJSON(self, face)
			self.known.append(bundle)

	def __newFace(self, bundle):
		face = bundle.parseData()

		filename = face['filename']
		encoding = face['encoding']
		group = face['group']

		encodings = ",".join([str(encode) for encode in encoding])

		return self.db.saveFace(filename, encodings, group)

	def __parseFaces(self, filePath) -> list:
		faces: list = []

		img = face_recognition.load_image_file(filePath)
		filename = os.path.basename(filePath)
		
		face_locations  = face_recognition.face_locations(img)
		face_encodings = face_recognition.face_encodings(img, face_locations)

		for encodings in face_encodings:
			bundle = FaceBundle(filename)
			bundle.setEncodings(encodings)
			faces.append(bundle)
		
		return faces

	def __hasMatch(self, knownEncodings, faceBundle):
		matches = []
		matches = face_recognition.compare_faces(knownEncodings, faceBundle.getEncodings(), tolerance=self.tolerance)
		return matches

	def addKnownFace(self, filePath, faceGroup) -> FaceBundle:
		bundles = self.__parseFaces(filePath)
		
		if len(bundles):
			bundles[0].setGroup(faceGroup)
			faceID = self.__newFace(bundles[0])
			bundles[0].setFaceID(faceID)
			self.known.append(bundles[0])
			return bundles[0]
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

	def findMatches(self, filePath, faceGroup) -> list:
		faces: list = []
		knownGroup = []
		knownEncodings = []
		
		bundles = self.__parseFaces(filePath)

		for knownFace in self.known:
			if knownFace.getGroup() == faceGroup:
				knownGroup.append(knownFace)

		for knownFaceGroup in knownGroup:
			knownEncodings.append(knownFaceGroup.getEncodings())

		for bundle in bundles:
			matches = self.__hasMatch(knownEncodings, bundle)

			if len(matches) > 0 and True in matches:
				match_index = matches.index(True)
				bundle_matched = knownGroup[match_index]
				faces.append(bundle_matched.parseData())

		return faces