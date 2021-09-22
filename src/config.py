from configparser import ConfigParser
from pathlib import Path


def config(filename='database.ini', section='postgresql'):
    """ Configure a database connection with parameters from database.ini file """
    parser = ConfigParser()
    parser.read(filename)
    # If parser cannot find and read a file it has length of 1, in that case add a src/database.ini path to check
    if len(parser) != 2:
        parser.read(Path("src", filename))

    # Get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
