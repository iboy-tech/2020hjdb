import ConfigParser
import os

config_full_path = os.path.expanduser("~/.config/send_email.conf")
config = ConfigParser.ConfigParser()
config.read(config_full_path)


for s in config.sections():
    print s, config.options(s)

    print config.get(s, 'smtp_host')