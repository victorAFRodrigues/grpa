class ApiKey:
    def __init__(self):
        import secrets
        self.secrets = secrets

    def generate(self):
        return self.secrets.token_urlsafe(32)