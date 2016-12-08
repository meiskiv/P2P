import json


class Quadro(object):
    def __init__(self,tipo, dados):
        self.tipo = tipo
        self.dados = dados

    def jsondumps(self):
        jd = json.dumps(self.__dict__)
        return jd

