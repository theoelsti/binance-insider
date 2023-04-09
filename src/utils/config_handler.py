import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

telegram_config = config['telegram']
database_config = config['database']
settings_config = config['settings']