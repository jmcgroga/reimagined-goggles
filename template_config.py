class Config(object):
    DEBUG = False
    TESTING = False
# {{ "{{" }} blueprint_prefix {{ "}}" }}
    
class Production(Config):
    pass

class Development(Config):
    DEBUG = True

class Testing(Config):
    TESTING = True
