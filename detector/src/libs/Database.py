import mysql.connector as mysql

class Database:
	def __init__(self):
		self.connection = mysql.connect(host='localhost', user='ciapd_recognition', password='ciapd$recognition', database='ciapd', auth_plugin='mysql_native_password')
		self.cursor = self.connection.cursor()
		self.__createTable()

	def __createTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `treinado` (`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, `foto` VARCHAR(100), `grupo` VARCHAR(13)) ENGINE=InnoDB")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `treinamento` (`id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT, `arquivo` LONGBLOB) ENGINE=InnoDB")

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
		self.cursor.execute("INSERT INTO `treinado`(`foto`, `grupo`) VALUES (%s, %s)", [filename, group])
		self.connection.commit()
		return self.cursor.lastrowid

	def deleteFace(self, id):
		try:
			self.cursor.execute("DELETE FROM `treinado` WHERE `id`=%s", [id])
			self.connection.commit()
			return True
		except:
			return False

	def getTrain(self, filename):
		self.cursor.execute("SELECT * FROM `treinamento` WHERE id=%s", [1])
		result = self.cursor.fetchone()

		if result != None:
			blob = result[1]

			with open(filename, 'wb') as file:
				file.write(blob)

			return True
		else:
			return False

	def saveTrain(self, filename, new):
		with open(filename, 'rb') as file:
			train = file.read()

		if new:
			self.cursor.execute("INSERT INTO `treinamento`(`arquivo`) VALUES (%s)", [train])
		else:
			self.cursor.execute("UPDATE `treinamento` SET `arquivo`=%s WHERE `id`=%s", [train, 1])

		self.connection.commit()