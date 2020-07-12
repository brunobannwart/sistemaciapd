import mysql.connector as mysql

class Database:
	def __init__(self):
		self.connection = mysql.connect(host='localhost', user='ciapd_recognition', password='ciapd$recognition', database='ciapd', auth_plugin='mysql_native_password')
		self.cursor = self.connection.cursor()
		self.__createTable()

	def __createTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `face` (`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, `arquivo` VARCHAR(100), "
			+ "`codificações` TEXT, `grupo` VARCHAR(13)) ENGINE=InnoDB")

	def getFaces(self):
		faces = []

		self.cursor.execute("SELECT * FROM `face`")
		results = self.cursor.fetchall()

		for row in results:
			faceID = row[0]
			filename = row[1]
			encodings = row[2].split(",")
			group = row[3]

			face = {
				'faceID': faceID,
				'filename': filename,
				'encoding': encodings,
				'group': group
			}

			faces.append(face)

		return faces

	def saveFace(self, filename, encodings, group):
		self.cursor.execute("INSERT INTO `face`(`arquivo`, `codificações`, `grupo`) VALUES (%s, %s, %s)", [filename, encodings, group])
		self.connection.commit()
		return self.cursor.lastrowid

	def deleteFace(self, id):
		try:
			self.cursor.execute("DELETE FROM `face` WHERE `id`=%s", [id])
			self.connection.commit()
			return True
		except:
			return False