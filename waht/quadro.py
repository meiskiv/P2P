import json


class Quadro(object):
    def __init__(self,tipo, dados):
        self.tipo = tipo
        self.dados = dados

    def tojson(self):
        return json.dump(Quadro.self.__dict__)
