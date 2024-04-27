from Instrucao import Instrucao
from Pipeline import Pipeline

def ler_linhas_programa():
    with open('programa2.txt', 'r') as file:
        return file.readlines()

def main():
    programa = ler_linhas_programa()
    registradores = [0] * 32
    pipeline = Pipeline(programa, registradores)
    pipeline.run()

if __name__ == "__main__":
    main()

