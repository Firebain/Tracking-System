from os import path


class Resources(object):
    __resources_dir = path.join(
        path.dirname(path.realpath(__file__)), 
        '..', 
        'resources'
    )

    @staticmethod
    def wsdl_dir():
        return path.join(Resources.__resources_dir, 'wsdl')

    @staticmethod
    def haarcascade(filename):
        return path.join(Resources.__resources_dir, 'haarcascades', filename)
