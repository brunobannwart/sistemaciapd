import cv2, face_recognition, os, pickle
import mysql.connector as mysql
import numpy as np
from .models.FaceBundle import FaceBundle

class FaceRecognition:
	def __init__(self, tolerance=0.6):
		self.tolerance = tolerance
		self.known = []

		self.db = mysql.connect(host='localhost', user='ciapd_recognition', password='ciapd$recognition', 
					database='ciapd', auth_plugin='mysql_native_password')

		self.cursor = self.db.cursor()
		self.__getFacesSaved()

	# Metodos privados	
	def __createFaceTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `face` (`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, `filename` VARCHAR(100), "
			+ "`encodings` TEXT, `group` VARCHAR(13)) ENGINE=InnoDB"
		)

	def __getFacesSaved(self):
		self.__createFaceTable()
		self.cursor.execute("SELECT * FROM `face`")
		results = self.cursor.fetchall()
	
		for row in results:
			encodings = []
			face_id = row[0]
			filename = row[1]
			encoding_list_str = row[2].split(",")
			group = row[3]

			for encoding_str in encoding_list_str:
				encoding = float(encoding_str)
				encodings.append(encoding)
	
			face = {
				'faceID': face_id,
				'filename': filename,
				'encoding': encodings,
				'group': group
			}
	
			face_bundle = FaceBundle.parseJSON(self, face)
			self.known.append(face_bundle)
	
	def __saveFace(self, bundle):
		bundleJSON = bundle.parseData()
		filename = bundleJSON['filename']
		encoding = bundleJSON['encoding']
		group = bundleJSON['group']
		encoding_str = ",".join([str(encode) for encode in encoding])
	
		self.cursor.execute("INSERT INTO `face`(`filename`, `encodings`, `group`) VALUES (%s, %s, %s)", [filename, encoding_str, group])
		self.db.commit()
		return self.cursor.lastrowid 

	def __deleteFace(self, id):
		try:
			self.cursor.execute("DELETE FROM `face` WHERE `id`=%s", [id])
			self.db.commit()
			return True
		except:
			return False

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

	# Metodos publicos
	def addKnownFace(self, filePath, faceGroup) -> FaceBundle:
		bundles = self.__parseFaces(filePath)
		
		if len(bundles):
			bundles[0].setGroup(faceGroup)
			faceID = self.__saveFace(bundles[0])
			bundles[0].setFaceID(faceID)
			self.known.append(bundles[0])
			return bundles[0]
		else:
			return None

	def removeKnownFace(self, faceID):
		count = 0;
	
		for knownFace in self.known:
			if knownFace.getFaceID() == parseInt(faceID):
				self.known.pop(count)
				if self.__deleteFace(faceID):
					return True
				else:
					return False
			else:
				count += 1

		return False

	def findMatches(self, filePath, faceGroup) -> list:
		faces: list = []
		knownEncodings = []
		bundles = self.__parseFaces(filePath)

		for knownFace in self.known:
			if knownFace.getGroup() == faceGroup:
				knownEncodings.append(knownFace.getEncodings())

		for bundle in bundles:
			matches = self.__hasMatch(knownEncodings, bundle)
			if True in matches:
				faces.append(bundle.parseData())

		return faces