def parseDB(filename='db.config', section='postgresql'):
    """ Create a connection to a database

    Args:
        filename (string): The file containing the credentials
        section (string): The section in the file

    Returns:
        The arguments for initializing a pyscopg2 database
    """
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found')
    return db

def get_cursor():
    """ Gets all the seasons """
    conn = psycopg2.connect(**parseDB('../configs/db.config'))
    cur = conn.cursor()
    return cur
