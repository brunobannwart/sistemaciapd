class Config:
	DEBUG = False
	FLASK_RUN_HOST = 'localhost'
	FLASK_RUN_PORT = 5000
	SUPPORTED_IMAGES_EXT = ['image/png', 'image/jpeg, image/jpg']
	FILE_ALLOWED = SUPPORTED_IMAGES_EXT