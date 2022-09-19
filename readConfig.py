import configparser


def prop_read():
    config = configparser.ConfigParser()
    config.read('prop.ini')
    return config