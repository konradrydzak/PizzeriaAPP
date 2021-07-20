from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    """ Configure a database connection with parameters from database.ini file """
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)
    # If needed add a src/database.ini path to check
    if len(parser) != 2:
        parser.read('src/' + filename)

    # Get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
