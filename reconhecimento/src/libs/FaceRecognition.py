import cv2, face_recognition, os, pickle
import mysql.connector
import numpy as np
from .models.FaceBundle import FaceBundle

class FaceRecognition:
	def __init__(self, tolerance=0.6):
		self.tolerance = tolerance
		self.known = []	
		#self.db = mysql.connector.connect(host='localhost', user='ciapd_recognition', passwd='ciapd$recognition', database='ciapd')
		#self.cursor = self.db.cursor()
		#self.__getFacesDatabase()

	# Metodos privados	

	#def __createFaceTable(self):
	#	self.cursor.execute(
	#		'CREATE TABLE IF NOT EXISTS face (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, filename VARCHAR(100), encodings'
	#	)

	#def __getFacesSaved(self):
	#	self.cursor.execute('SELECT * FROM face')
	#	results = self.cursor.fetchall()
	#
	#	for row in results:
	#		face = {
	#			'id': row[0],
	#			'filename': row[1],
	#		}
	#
	#		face_bundle = parseJSON(face)
	#		self.known.append(face_bundle)
	
	#def __saveFace(self, bundle):
	#	face = bundle.parseData()
	#	self.cursor.execute('INSERT INTO face(filename, encodings, group) VALUES (%s, %s, %s)', ())
	#	self.db.commit()
	#	return self.cursor.lastrowid 

	#def __deleteFace(self, id):
	#	self.cursor.execute('DELETE FROM face WHERE id=%s', (id))
	#	self.db.commit()

	def __parseFaces(self, filePath) -> list:
		faces: list = []

		img = face_recognition.load_image_file(filePath)
		filename = os.path.basename(filePath)
		
		face_locations  = face_recognition.face_locations(img)
		face_encodings = face_recognition.face_encodings(img, face_locations)
		face_landmarks = face_recognition.face_landmarks(img)

		for location, encodings, landmarks in zip(face_locations, face_encodings, face_landmarks):
			bundle = FaceBundle(filename)
			bundle.setLocation(location)
			bundle.setEncodings(encodings)
			bundle.setLandMarks(landmarks)
			faces.append(bundle)
		
		return faces

	def __hasMatch(self, knownEncodings, faceBundle):
		matches = []
		matches = face_recognition.compare_faces(knownEncodings, faceBundle.getEncodings(), tolerance=self.tolerance)
		return matches

	# Metodos publicos

	def addKnownFace(self, filePath, faceGroup) -> FaceBundle:
		bundles = self.__parseFaces(filePath)
		
		if len(bundles):
			bundles[0].setGroup(faceGroup)
			#faceID = self.__saveFace(bundles[0])
			#bundles[0].setFaceID(faceID)
			self.known.append(bundles[0])
				
		return bundles[0]

	#def removeKnownFace(self, faceID):
	#	count = 0;
	#
	#	for knownFace in self.known:
	#		if knownFace.getFaceID() == faceID:
	#			break
	#		count += 1
	#
	#	self.known.pop(count)
	# 	self.__deleteFace(faceID)

	def findMatches(self, filePath) -> list: # add fileGroup
		faces: list = []
		knownEncodings = []
		bundles = self.__parseFaces(filePath)

		for knownFace in self.known:
			#if knownFace.getGroup() == fileGroup:
			knownEncodings.append(knownFace.getEncodings())

		for bundle in bundles:
			matches = self.__hasMatch(knownEncodings, bundle)
			if True in matches:
				bundle.setKnownFace(True)
			faces.append(bundle.parseData())

		return faces