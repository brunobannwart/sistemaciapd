import mysql.connector as mysql

class Database:
	def __init__(self):
		self.connection = mysql.connect(host='localhost', user='ciapd_recognition', password='ciapd$recognition', database='ciapd', auth_plugin='mysql_native_password')
		self.cursor = self.connection.cursor()
		self.__createTable()

	def __createTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `treinado` (`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, `arquivo` VARCHAR(100), `grupo` VARCHAR(13)) ENGINE=InnoDB")

	def getFaces(self):
		faces = []

		self.cursor.execute("SELECT * FROM `treinado`")
		results = self.cursor.fetchall()

		for row in results:
			faceID = row[0]
			filename = row[1]
			group = row[2]

			face = {
				'faceID': faceID,
				'filename': filename,
				'group': group
			}

			faces.append(face)

		return faces

	def saveFace(self, filename, group):
		self.cursor.execute("INSERT INTO `treinado`(`arquivo`, `grupo`) VALUES (%s, %s)", [filename, group])
		self.connection.commit()
		return self.cursor.lastrowid

	def deleteFace(self, id):
		try:
			self.cursor.execute("DELETE FROM `treinado` WHERE `id`=%s", [id])
			self.connection.commit()
			return True
		except:
			return False