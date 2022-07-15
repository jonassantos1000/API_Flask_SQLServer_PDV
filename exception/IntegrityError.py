class IntegrityError(Exception):
    def __init__(self, descricao, mensagem):
        self.code = 400
        self.description = descricao
        self.message = mensagem