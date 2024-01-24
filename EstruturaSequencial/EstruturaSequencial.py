import random
import string
import time

class No:
    def __init__(self, chave, dado1, dado2):
        self.chave = chave
        self.dado1 = dado1
        self.dado2 = dado2
        self.proximo = None

class ArvoreSequencial:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, dado1, dado2):
        novo_no = No(chave, dado1, dado2)
        if not self.raiz:
            self.raiz = novo_no
        else:
            atual = self.raiz
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no

    def buscar(self, chave):
        atual = self.raiz
        tempo_inicial = time.time()
        interacoes = 0  # Inicializa o contador de interações
        while atual:
            interacoes += 1  # Incrementa o contador de interações a cada passo
            if atual.chave == chave:
                tempo_final = time.time()
                return atual, tempo_final - tempo_inicial, interacoes  # Retorna o resultado e o contador de interações
            atual = atual.proximo
        tempo_final = time.time()
        return None, tempo_final - tempo_inicial, interacoes  # Retorna None e o contador de interações

class BuscaNumerosQueExistemSequencial:
    def __init__(self, arvore, num_buscas, num_registros):
        self.arvore = arvore
        self.num_buscas = num_buscas
        self.num_registros = num_registros

    def buscar_numeros_que_existem(self):
        resultados = []
        total_interacoes = 0  # Inicializa o contador total de interações
        for _ in range(self.num_buscas):
            chave = random.choice(range(1, self.num_registros + 1))
            resultado, tempo, interacoes = self.arvore.buscar(chave)  # Recebe o contador de interações
            total_interacoes += interacoes  # Incrementa o contador total de interações
            resultados.append((chave, resultado, tempo, interacoes))  # Adiciona o contador de interações à lista
        return resultados, total_interacoes  # Retorna os resultados e o contador total de interações

class BuscaNumerosQueNaoExistemSequencial:
    def __init__(self, arvore, dados, num_buscas, num_registros):
        self.arvore = arvore
        self.dados = dados
        self.num_buscas = num_buscas
        self.num_registros = num_registros

    def buscar_numeros_que_nao_existem(self):
        numeros_unicos = set(entry[0] for entry in self.dados)
        numeros_nao_encontrados = []

        total_interacoes = 0  # Inicializa o contador total de interações

        while len(numeros_nao_encontrados) < self.num_buscas:
            num_aleatorio = random.randint(1, self.num_registros * 2)
            if num_aleatorio not in numeros_unicos:
                resultado, tempo, interacoes = self.arvore.buscar(num_aleatorio)
                total_interacoes += interacoes  # Incrementa o contador total de interações
                if not resultado:
                    numeros_nao_encontrados.append((num_aleatorio, tempo, interacoes))
        return numeros_nao_encontrados, total_interacoes  # Retorna os resultados e o contador total de interações

def gerar_dados_sequencial(num_registros, ordenados=False):
    dados = []
    for i in range(num_registros):
        chave = i + 1 if ordenados else random.randint(1, num_registros)
        dado1 = random.randint(1, 100)
        dado2 = ''.join(random.choice(string.ascii_letters) for _ in range(100))  # Usando 100 letras em vez de 10000
        dados.append((chave, dado1, dado2))
    return dados

def criar_arquivo_de_dados_sequencial(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for entrada in dados:
            arquivo.write(f"{entrada[0]} {entrada[1]} {entrada[2]}\n")

def main_sequencial():
    num_registros = int(input("Número de chaves no arquivo: "))
    num_buscas = int(input("Quantidade de chaves aleatórias a buscar: "))
    ordenados_opcao = input("Chaves ordenadas? (S/N): ").strip().lower()
    dados_ordenados = ordenados_opcao == 's'
    dados = gerar_dados_sequencial(num_registros, ordenados=dados_ordenados)
    criar_arquivo_de_dados_sequencial(dados, 'dados_sequencial.txt')

    arvore = ArvoreSequencial()
    for entrada in dados:
        arvore.inserir(*entrada)

    busca_existente = BuscaNumerosQueExistemSequencial(arvore, num_buscas, num_registros)
    resultados_existente, total_interacoes_existente = busca_existente.buscar_numeros_que_existem()

    print("Busca pelos números que existem:")
    for chave, resultado, tempo, interacoes in resultados_existente:
        if resultado:
            print(f"Chave: {chave}, encontrada, Tempo de pesquisa: {tempo:.6f} segundos, Interacoes: {interacoes}")

    input("Pressione Enter para continuar e buscar números que não existem...")
    print()

    busca_nao_existente = BuscaNumerosQueNaoExistemSequencial(arvore, dados, num_buscas, num_registros)
    resultados_nao_existente, total_interacoes_nao_existente = busca_nao_existente.buscar_numeros_que_nao_existem()

    print("\nBusca pelos números que não existem:")
    for chave, tempo, interacoes in resultados_nao_existente:
        print(f"Chave: {chave}, não encontrada, Tempo de pesquisa: {tempo:.6f} segundos, Interacoes: {interacoes}")

    tempo_total_existente = sum(tempo for _, _, tempo, _ in resultados_existente)
    tempo_total_nao_existente = sum(tempo for _, tempo, _ in resultados_nao_existente)

    print()
    print(f"Tempo total das buscas pelos números que existem: {tempo_total_existente:.6f} segundos")
    print(f"Tempo total das buscas pelos números que não existem: {tempo_total_nao_existente:.6f} segundos")
    print(f"Total de interações nas buscas pelos números que existem: {total_interacoes_existente}")
    print(f"Total de interações nas buscas pelos números que não existem: {total_interacoes_nao_existente}")

if __name__ == "__main__":
    main_sequencial()
