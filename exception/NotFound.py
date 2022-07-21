class NotFound(Exception):
    def __init__(self, descricao, mensagem):
        self.code = 404
        self.description = descricao
        self.message = mensagem