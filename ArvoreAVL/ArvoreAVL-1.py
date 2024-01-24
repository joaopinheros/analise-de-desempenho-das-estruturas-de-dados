import random
import string
import time

# Classe que define um nó da árvore AVL.
class NoAVL:
    def __init__(self, chave, dado1, dado2):
        self.chave = chave       # Chave do nó
        self.dado1 = dado1       # Primeiro dado (valor inteiro)
        self.dado2 = dado2       # Segundo dado (combinação de letras)
        self.esquerda = None     # Filho à esquerda
        self.direita = None      # Filho à direita
        self.altura = 1          # Altura do nó (inicializada como 1)

# Função auxiliar para obter a altura de um nó.
def obter_altura(no):
    if no is None:
        return 0
    return no.altura

# Função auxiliar para obter o fator de balanceamento de um nó.
def obter_fator_balanceamento(no):
    if no is None:
        return 0
    return obter_altura(no.esquerda) - obter_altura(no.direita)

# Função auxiliar para fazer a rotação simples à direita.
def rotacao_direita(y):
    if y is None or y.esquerda is None:
        return y

    x = y.esquerda
    T2 = x.direita

    x.direita = y
    y.esquerda = T2

    y.altura = 1 + max(obter_altura(y.esquerda), obter_altura(y.direita))
    x.altura = 1 + max(obter_altura(x.esquerda), obter_altura(x.direita))

    return x

# Função auxiliar para fazer a rotação simples à esquerda.
def rotacao_esquerda(x):
    if x is None or x.direita is None:
        return x

    y = x.direita
    T2 = y.esquerda

    y.esquerda = x
    x.direita = T2

    x.altura = 1 + max(obter_altura(x.esquerda), obter_altura(x.direita))
    y.altura = 1 + max(obter_altura(y.esquerda), obter_altura(y.direita))

    return y

# Função que insere um nó na árvore AVL.
def inserir(raiz, chave, dado1, dado2):
    if raiz is None:
        return NoAVL(chave, dado1, dado2)

    if chave < raiz.chave:
        raiz.esquerda = inserir(raiz.esquerda, chave, dado1, dado2)
    else:
        raiz.direita = inserir(raiz.direita, chave, dado1, dado2)

    raiz.altura = 1 + max(obter_altura(raiz.esquerda), obter_altura(raiz.direita))

    balanceamento = obter_fator_balanceamento(raiz)

    # Casos de desequilíbrio
    if balanceamento > 1:
        if chave < raiz.esquerda.chave:
            return rotacao_direita(raiz)
        else:
            raiz.esquerda = rotacao_esquerda(raiz.esquerda)
            return rotacao_direita(raiz)
    if balanceamento < -1:
        if chave > raiz.direita.chave:
            return rotacao_esquerda(raiz)
        else:
            raiz.direita = rotacao_direita(raiz.direita)
            return rotacao_esquerda(raiz)

    return raiz

# Classe que define a árvore AVL.
class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    # Insere um nó na árvore AVL.
    def inserir(self, chave, dado1, dado2):
        self.raiz = inserir(self.raiz, chave, dado1, dado2)

    # Realiza uma busca na árvore por uma chave e retorna o nó encontrado, o tempo gasto na busca e o número de interações.
    def buscar(self, chave):
        tempo_inicio = time.time()  # Registra o tempo de início da busca
        no, tempo_busca, interacoes = self._buscar(self.raiz, chave, 0)
        tempo_fim = time.time()
        return no, tempo_fim - tempo_inicio, interacoes

    def _buscar(self, no, chave, interacoes):
        if no is None:
            return None, 0, interacoes  # Retorna None quando a chave não é encontrada
        interacoes += 1
        if no.chave == chave:
            return no, 0, interacoes  # Retorna o nó e o número de interações quando a chave é encontrada
        elif chave < no.chave:
            return self._buscar(no.esquerda, chave, interacoes)
        else:
            return self._buscar(no.direita, chave, interacoes)

# Classe para buscar chaves que existem na árvore.
class BuscadorChavesExistentes:
    def buscar_chaves(self, arvore, chaves):
        resultados = []
        tempo_total = 0
        interacoes_total = 0

        for chave in chaves:
            resultado, tempo_busca, interacoes = arvore.buscar(chave)
            tempo_total += tempo_busca
            interacoes_total += interacoes
            if resultado:
                resultados.append(f"Chave: {chave}, encontrada, Tempo médio de pesquisa: {tempo_busca:.6f} segundos, Interacoes: {interacoes}")
            else:
                resultados.append(f"Chave: {chave}, não encontrada, Tempo médio de pesquisa: {tempo_busca:.6f} segundos, Interacoes: {interacoes}")

        return resultados, tempo_total, interacoes_total

# Classe para buscar chaves que não existem na árvore.
class BuscadorChavesNaoExistentes:
    def buscar_chaves(self, arvore, num_entradas, chaves):
        resultados = []
        tempo_total = 0
        interacoes_total = 0

        for chave in chaves:
            resultado, tempo_busca, interacoes = arvore.buscar(chave)
            tempo_total += tempo_busca
            interacoes_total += interacoes
            if resultado:
                resultados.append(f"Chave: {chave}, encontrada, Tempo médio de pesquisa: {tempo_busca:.6f} segundos, Interacoes: {interacoes}")
            else:
                resultados.append(f"Chave: {chave}, não encontrada, Tempo médio de pesquisa: {tempo_busca:.6f} segundos, Interacoes: {interacoes}")

        return resultados, tempo_total, interacoes_total

# Gera dados aleatórios com chaves, valores inteiros e combinações de letras.
def gerar_dados(num_entradas, ordenadas=False):
    dados = []
    for i in range(num_entradas):
        chave = i + 1 if ordenadas else random.randint(1, num_entradas)
        dado1 = random.randint(1, 100)
        dado2 = ''.join(random.choice(string.ascii_letters) for _ in range(100))
        dados.append((chave, dado1, dado2))
    return dados

# Função para criar um arquivo com os dados gerados.
def criar_arquivo_dados(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for entrada in dados:
            arquivo.write(f"{entrada[0]} {entrada[1]} {entrada[2]}\n")

# Função principal do programa.
def main():
    num_entradas = int(input("Número de chaves no arquivo: "))  # Solicita o número de chaves
    quant_buscas = int(input("Quantidade de chaves aleatórias a buscar: "))  # Solicita a quantidade de buscas
    opcao_ordenadas = input("Chaves ordenadas? (S/N): ").strip().lower()
    dados_ordenados = opcao_ordenadas == 's'
    
    # Iniciar a contagem do tempo de inserção
    tempo_inicio_insercao = time.time()
    dados = gerar_dados(num_entradas, ordenadas=dados_ordenados)
    tempo_fim_insercao = time.time()
    
    criar_arquivo_dados(dados, 'dados.txt')  # Cria um arquivo de texto com os dados

    arvore = ArvoreAVL()
    
    # Inserir os dados na árvore e calcular o tempo de inserção
    for entrada in dados:
        arvore.inserir(*entrada)

    chaves_busca = random.sample(range(1, num_entradas + 1), quant_buscas)
    tempo_total_busca_chaves_existentes = 0

    # Realiza buscas em chaves aleatórias que existem e registra o tempo de cada busca.
    buscador_chaves_existentes = BuscadorChavesExistentes()
    resultados_chaves_existentes, tempo_total_busca_chaves_existentes, interacoes_total_chaves_existentes = buscador_chaves_existentes.buscar_chaves(arvore, chaves_busca)

    print("\nBusca pelos números que existem:")
    for resultado in resultados_chaves_existentes:
        print(resultado)

    input("\nPressione Enter para continuar e buscar números que não existem...")

    chaves_nao_existem = random.sample(range(num_entradas + 1, num_entradas + 100), quant_buscas)
    tempo_total_busca_chaves_nao_existentes = 0

    # Realiza buscas em chaves aleatórias que não existem e registra o tempo de cada busca.
    buscador_chaves_nao_existentes = BuscadorChavesNaoExistentes()
    resultados_chaves_nao_existentes, tempo_total_busca_chaves_nao_existentes, interacoes_total_chaves_nao_existentes = buscador_chaves_nao_existentes.buscar_chaves(arvore, num_entradas, chaves_nao_existem)

    print("\nBusca pelos números que não existem:")
    for resultado in resultados_chaves_nao_existentes:
        print(resultado)

    tempo_total_todas_buscas = tempo_total_busca_chaves_existentes + tempo_total_busca_chaves_nao_existentes
    interacoes_total_todas_buscas = interacoes_total_chaves_existentes + interacoes_total_chaves_nao_existentes

    print(f"\nTempo total das buscas pelos números que existem: {tempo_total_busca_chaves_existentes:.6f} segundos")
    print(f"Tempo total das buscas pelos números que não existem: {tempo_total_busca_chaves_nao_existentes:.6f} segundos")
    print(f"Tempo total de todas as buscas: {tempo_total_todas_buscas:.6f} segundos")
    print(f"Número total de interações em todas as buscas: {interacoes_total_todas_buscas}")

if __name__ == "__main__":
    main()
