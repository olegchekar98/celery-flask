import os


class DevelopmentConfig():
    TESTING = False
    WTF_CSRF_ENABLED = False
    UPLOAD_PATH = "project/file_storage"
