import os
from env import load_dotenv, find_dotenv

class DotEnv:
    def __init__(self):
        load_dotenv(find_dotenv())

    def get(self, key):

        value = os.getenv(key)

        if value is None:
            print(f'A variável de ambiente "{key}" não está cadastrada.')
            raise KeyError(f'A variável de ambiente "{key}" não está cadastrada.')

        return value

    def set(self, key, value):
        try:
            with open(find_dotenv(), "r") as f:
                rows = f.readlines()
                # print(rows)
        except FileNotFoundError:
            rows = []

        found = False
        with open(find_dotenv(), "w") as f:
            for row in rows:
                if row.startswith(f"{key}="):
                    f.write(f'{key}="{value}"\n')
                    found = True
                else:
                    f.write(row)
            if not found:
                f.write(f'{key}="{value}"\n')
