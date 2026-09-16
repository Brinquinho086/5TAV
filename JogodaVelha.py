import random
import time
import os
import json

# =======================================================
# SISTEMA DE MEMÓRIA E ARQUIVOS (AGENTE INTELIGENTE)
# =======================================================

ARQUIVO_MEMORIA = 'memoria_agente.txt'
ARQUIVO_MATRIZ = 'resultados_finais.txt'

def carregar_memoria():
    """Lê o banco de dados do Agente Inteligente."""
    if os.path.exists(ARQUIVO_MEMORIA):
        try:
            with open(ARQUIVO_MEMORIA, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_memoria(memoria):
    """Salva a experiência que o Agente adquiriu."""
    with open(ARQUIVO_MEMORIA, 'w') as f:
        json.dump(memoria, f)

def carregar_matriz():
    """Lê a matriz de resultados finais."""
    matriz = {}
    if os.path.exists(ARQUIVO_MATRIZ):
        try:
            with open(ARQUIVO_MATRIZ, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                for linha in linhas[2:]: # Pula as 2 linhas de cabeçalho
                    partes = linha.strip().split('|')
                    if len(partes) >= 5:
                        tab_str = partes[3].strip()
                        matriz[tab_str] = {
                            'X': int(partes[0].strip()),
                            'Empate': int(partes[1].strip()),
                            'O': int(partes[2].strip()),
                            'Freq': int(partes[4].strip())
                        }
        except:
            pass
    return matriz

def salvar_matriz(matriz):
    """Atualiza o arquivo txt visual com os resultados organizados."""
    with open(ARQUIVO_MATRIZ, 'w', encoding='utf-8') as f:
        f.write(" Vit. X | Empate | Vit. O | Tabuleiro Final                 | Frequência\n")
        f.write("-" * 80 + "\n")
        # Ordena para os mais frequentes ficarem no topo (opcional, mas fica legal)
        itens_ordenados = sorted(matriz.items(), key=lambda item: item[1]['Freq'], reverse=True)
        
        for tab_str, dados in itens_ordenados:
            f.write(f"   {dados['X']}    |   {dados['Empate']}    |   {dados['O']}    | {tab_str:<29} | {dados['Freq']}\n")

# =======================================================
# FUNÇÕES DO JOGO DA VELHA
# =======================================================

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_tabuleiro(tabuleiro):
    simbolos = {1: 'X', -1: 'O', 0: ' '}
    print("\n Posições do Tabuleiro:")
    print("  0 | 1 | 2 ")
    print(" ---+---+---")
    print("  3 | 4 | 5 ")
    print(" ---+---+---")
    print("  6 | 7 | 8 \n")
    print(" Jogo Atual:")
    print(f"  {simbolos[tabuleiro[0]]} | {simbolos[tabuleiro[1]]} | {simbolos[tabuleiro[2]]} ")
    print(" ---+---+---")
    print(f"  {simbolos[tabuleiro[3]]} | {simbolos[tabuleiro[4]]} | {simbolos[tabuleiro[5]]} ")
    print(" ---+---+---")
    print(f"  {simbolos[tabuleiro[6]]} | {simbolos[tabuleiro[7]]} | {simbolos[tabuleiro[8]]} \n")

# --- TIPOS DE JOGADORES ---

# 1. Humano
def jogada_humano(tabuleiro):
    while True:
        try:
            pos = int(input("Escolha uma posição (0 a 8): "))
            if pos < 0 or pos > 8:
                print("Posição inválida! Escolha um número entre 0 e 8.")
            elif tabuleiro[pos] != 0:
                print("Essa posição já está ocupada! Escolha outra.")
            else:
                return pos
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

# 2. Aleatório
def jogada_aleatoria(tabuleiro):
    posicoes_vazias = [i for i, valor in enumerate(tabuleiro) if valor == 0]
    return random.choice(posicoes_vazias)

# 3. Customizada (Sua IA original do código)
def jogada_customizada(tabuleiro, jogador_atual):
    posicoes_vazias = [i for i, valor in enumerate(tabuleiro) if valor == 0]
    oponente = jogador_atual * -1

    if tabuleiro == [0] * 9: return 4

    # Linhas, Colunas e Diagonais (Ataque)
    elif tabuleiro[0] == jogador_atual and tabuleiro[1] == jogador_atual and tabuleiro[2] == 0: return 2
    elif tabuleiro[0] == jogador_atual and tabuleiro[2] == jogador_atual and tabuleiro[1] == 0: return 1
    elif tabuleiro[1] == jogador_atual and tabuleiro[2] == jogador_atual and tabuleiro[0] == 0: return 0
    elif tabuleiro[3] == jogador_atual and tabuleiro[4] == jogador_atual and tabuleiro[5] == 0: return 5
    elif tabuleiro[3] == jogador_atual and tabuleiro[5] == jogador_atual and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == jogador_atual and tabuleiro[5] == jogador_atual and tabuleiro[3] == 0: return 3
    elif tabuleiro[6] == jogador_atual and tabuleiro[7] == jogador_atual and tabuleiro[8] == 0: return 8
    elif tabuleiro[6] == jogador_atual and tabuleiro[8] == jogador_atual and tabuleiro[7] == 0: return 7
    elif tabuleiro[7] == jogador_atual and tabuleiro[8] == jogador_atual and tabuleiro[6] == 0: return 6
    elif tabuleiro[0] == jogador_atual and tabuleiro[3] == jogador_atual and tabuleiro[6] == 0: return 6
    elif tabuleiro[0] == jogador_atual and tabuleiro[6] == jogador_atual and tabuleiro[3] == 0: return 3
    elif tabuleiro[3] == jogador_atual and tabuleiro[6] == jogador_atual and tabuleiro[0] == 0: return 0
    elif tabuleiro[1] == jogador_atual and tabuleiro[4] == jogador_atual and tabuleiro[7] == 0: return 7
    elif tabuleiro[1] == jogador_atual and tabuleiro[7] == jogador_atual and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == jogador_atual and tabuleiro[7] == jogador_atual and tabuleiro[1] == 0: return 1
    elif tabuleiro[2] == jogador_atual and tabuleiro[5] == jogador_atual and tabuleiro[8] == 0: return 8
    elif tabuleiro[2] == jogador_atual and tabuleiro[8] == jogador_atual and tabuleiro[5] == 0: return 5
    elif tabuleiro[5] == jogador_atual and tabuleiro[8] == jogador_atual and tabuleiro[2] == 0: return 2
    elif tabuleiro[0] == jogador_atual and tabuleiro[4] == jogador_atual and tabuleiro[8] == 0: return 8
    elif tabuleiro[0] == jogador_atual and tabuleiro[8] == jogador_atual and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == jogador_atual and tabuleiro[8] == jogador_atual and tabuleiro[0] == 0: return 0
    elif tabuleiro[2] == jogador_atual and tabuleiro[4] == jogador_atual and tabuleiro[6] == 0: return 6
    elif tabuleiro[2] == jogador_atual and tabuleiro[6] == jogador_atual and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == jogador_atual and tabuleiro[6] == jogador_atual and tabuleiro[2] == 0: return 2

    # Linhas, Colunas e Diagonais (Defesa)
    elif tabuleiro[0] == oponente and tabuleiro[1] == oponente and tabuleiro[2] == 0: return 2
    elif tabuleiro[0] == oponente and tabuleiro[2] == oponente and tabuleiro[1] == 0: return 1
    elif tabuleiro[1] == oponente and tabuleiro[2] == oponente and tabuleiro[0] == 0: return 0
    elif tabuleiro[3] == oponente and tabuleiro[4] == oponente and tabuleiro[5] == 0: return 5
    elif tabuleiro[3] == oponente and tabuleiro[5] == oponente and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == oponente and tabuleiro[5] == oponente and tabuleiro[3] == 0: return 3
    elif tabuleiro[6] == oponente and tabuleiro[7] == oponente and tabuleiro[8] == 0: return 8
    elif tabuleiro[6] == oponente and tabuleiro[8] == oponente and tabuleiro[7] == 0: return 7
    elif tabuleiro[7] == oponente and tabuleiro[8] == oponente and tabuleiro[6] == 0: return 6
    elif tabuleiro[0] == oponente and tabuleiro[3] == oponente and tabuleiro[6] == 0: return 6
    elif tabuleiro[0] == oponente and tabuleiro[6] == oponente and tabuleiro[3] == 0: return 3
    elif tabuleiro[3] == oponente and tabuleiro[6] == oponente and tabuleiro[0] == 0: return 0
    elif tabuleiro[1] == oponente and tabuleiro[4] == oponente and tabuleiro[7] == 0: return 7
    elif tabuleiro[1] == oponente and tabuleiro[7] == oponente and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == oponente and tabuleiro[7] == oponente and tabuleiro[1] == 0: return 1
    elif tabuleiro[2] == oponente and tabuleiro[5] == oponente and tabuleiro[8] == 0: return 8
    elif tabuleiro[2] == oponente and tabuleiro[8] == oponente and tabuleiro[5] == 0: return 5
    elif tabuleiro[5] == oponente and tabuleiro[8] == oponente and tabuleiro[2] == 0: return 2
    elif tabuleiro[0] == oponente and tabuleiro[4] == oponente and tabuleiro[8] == 0: return 8
    elif tabuleiro[0] == oponente and tabuleiro[8] == oponente and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == oponente and tabuleiro[8] == oponente and tabuleiro[0] == 0: return 0
    elif tabuleiro[2] == oponente and tabuleiro[4] == oponente and tabuleiro[6] == 0: return 6
    elif tabuleiro[2] == oponente and tabuleiro[6] == oponente and tabuleiro[4] == 0: return 4
    elif tabuleiro[4] == oponente and tabuleiro[6] == oponente and tabuleiro[2] == 0: return 2
 
    # Defesa Secundária
    elif tabuleiro[4] == jogador_atual and ((tabuleiro[0] == oponente and tabuleiro[8] == oponente) or (tabuleiro[2] == oponente and tabuleiro[6] == oponente)) and tabuleiro[1] == 0: return 1
    elif tabuleiro[4] == jogador_atual and ((tabuleiro[0] == oponente and tabuleiro[8] == oponente) or (tabuleiro[2] == oponente and tabuleiro[6] == oponente)) and tabuleiro[3] == 0: return 3
    elif tabuleiro[4] == jogador_atual and ((tabuleiro[0] == oponente and tabuleiro[8] == oponente) or (tabuleiro[2] == oponente and tabuleiro[6] == oponente)) and tabuleiro[5] == 0: return 5
    elif tabuleiro[4] == jogador_atual and ((tabuleiro[0] == oponente and tabuleiro[8] == oponente) or (tabuleiro[2] == oponente and tabuleiro[6] == oponente)) and tabuleiro[7] == 0: return 7
    
    # Estratégia de Posicionamento
    elif tabuleiro[4] == 0: return 4
    elif tabuleiro[0] == 0: return 0
    elif tabuleiro[2] == 0: return 2
    elif tabuleiro[6] == 0: return 6
    elif tabuleiro[8] == 0: return 8
    elif tabuleiro[1] == 0: return 1
    elif tabuleiro[3] == 0: return 3
    elif tabuleiro[5] == 0: return 5
    elif tabuleiro[7] == 0: return 7
    else: return posicoes_vazias[0]

# 4. Agente Inteligente
def jogada_agente(tabuleiro, memoria):
    estado = str(tabuleiro)
    posicoes_vazias = [i for i, valor in enumerate(tabuleiro) if valor == 0]
    
    if estado in memoria:
        melhor_jogada = None
        maior_pontuacao = -float('inf')
        
        for jogada_str, pontuacao in memoria[estado].items():
            jogada = int(jogada_str)
            if jogada in posicoes_vazias and pontuacao > maior_pontuacao:
                maior_pontuacao = pontuacao
                melhor_jogada = jogada
                
        if melhor_jogada is not None:
            return melhor_jogada
            
    return random.choice(posicoes_vazias)

# --- REGRAS E EXECUÇÃO ---

def verificar_fim_de_jogo(tabuleiro):
    linhas_vitoria = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
    ]
    for a, b, c in linhas_vitoria:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] and tabuleiro[a] != 0:
            return tabuleiro[a] 
    if 0 not in tabuleiro:
        return 0 
    return None

def escolher_tipo_jogador(nome_jogador):
    print(f"\nEscolha o controle para o jogador {nome_jogador}:")
    print("1 - Humano")
    print("2 - Máquina (Jogadas Aleatórias)")
    print("3 - Máquina (Sua IA)")
    print("4 - Agente Inteligente (Aprende com Experiência)")
    
    while True:
        escolha = input(f"Digite o número para o jogador {nome_jogador}: ")
        if escolha in ['1', '2', '3', '4']:
            return int(escolha)
        print("Opção inválida!")

def jogar_partida(tipo_X, tipo_O, memoria, visual=True, jogador_inicial=1):
    tabuleiro = [0] * 9
    jogador_atual = jogador_inicial
    nomes = {1: 'X', -1: 'O'}
    tipos = {1: tipo_X, -1: tipo_O}
    
    historico_X = []
    historico_O = []
    
    while True:
        if visual:
            limpar_tela()
            exibir_tabuleiro(tabuleiro)
            print(f"Vez do jogador {nomes[jogador_atual]}")
        
        tipo_atual = tipos[jogador_atual]
        estado_atual = str(tabuleiro)
        
        if tipo_atual == 1:
            jogada = jogada_humano(tabuleiro)
        elif tipo_atual == 2:
            if visual: time.sleep(1)
            jogada = jogada_aleatoria(tabuleiro)
        elif tipo_atual == 3:
            if visual: time.sleep(1)
            jogada = jogada_customizada(tabuleiro, jogador_atual)
        elif tipo_atual == 4:
            if visual: time.sleep(1)
            jogada = jogada_agente(tabuleiro, memoria)
            
        # Registra o histórico da jogada (para a memória do Agente)
        if jogador_atual == 1:
            historico_X.append((estado_atual, jogada))
        else:
            historico_O.append((estado_atual, jogada))
            
        tabuleiro[jogada] = jogador_atual
        
        resultado = verificar_fim_de_jogo(tabuleiro)
        if resultado is not None:
            if visual:
                limpar_tela()
                exibir_tabuleiro(tabuleiro)
                if resultado == 1: print("🎉 FIM DE JOGO! O jogador X venceu! 🎉")
                elif resultado == -1: print("🎉 FIM DE JOGO! O jogador O venceu! 🎉")
                else: print("🤝 FIM DE JOGO! Deu velha (Empate)! 🤝")
            
            # Retorna o resultado + o caminho que os jogadores fizeram + tabuleiro final
            return resultado, historico_X, historico_O, tabuleiro
            
        jogador_atual *= -1

# --- ATUALIZADORES (RODAM NO FINAL DAS PARTIDAS) ---

def processar_memoria(tipo_X, tipo_O, resultado, historico_X, historico_O, memoria):
    """Distribui as recompensas (+2, +1, -2) na memória baseada no resultado da partida."""
    if tipo_X == 4:
        pontos = 2 if resultado == 1 else (1 if resultado == 0 else -2)
        for estado, jogada in historico_X:
            jogada_str = str(jogada)
            if estado not in memoria: memoria[estado] = {}
            if jogada_str not in memoria[estado]: memoria[estado][jogada_str] = 0
            memoria[estado][jogada_str] += pontos
            
    if tipo_O == 4:
        pontos = 2 if resultado == -1 else (1 if resultado == 0 else -2)
        for estado, jogada in historico_O:
            jogada_str = str(jogada)
            if estado not in memoria: memoria[estado] = {}
            if jogada_str not in memoria[estado]: memoria[estado][jogada_str] = 0
            memoria[estado][jogada_str] += pontos

def processar_matriz_final(resultado, tabuleiro_final, matriz):
    """Registra o tabuleiro final na matriz de estatísticas."""
    tab_str = str(tabuleiro_final)
    
    vit_x = 1 if resultado == 1 else 0
    empate = 1 if resultado == 0 else 0
    vit_o = 1 if resultado == -1 else 0

    if tab_str not in matriz:
        matriz[tab_str] = {'X': vit_x, 'Empate': empate, 'O': vit_o, 'Freq': 1}
    else:
        matriz[tab_str]['Freq'] += 1

# --- MODOS DE JOGO ---

def modo_visual():
    limpar_tela()
    print("=== MODO VISUAL ===")
    tipo_X = escolher_tipo_jogador("X (1)")
    tipo_O = escolher_tipo_jogador("O (-1)")
    
    memoria = carregar_memoria()
    matriz = carregar_matriz()
    
    resultado, hist_X, hist_O, tab_final = jogar_partida(tipo_X, tipo_O, memoria, visual=True, jogador_inicial=1)
    
    # Atualiza as informações aprendidas/geradas e salva nos TXT
    processar_memoria(tipo_X, tipo_O, resultado, hist_X, hist_O, memoria)
    processar_matriz_final(resultado, tab_final, matriz)
    salvar_memoria(memoria)
    salvar_matriz(matriz)

def modo_teste():
    limpar_tela()
    print("=== MODO DE TESTE (EXECUÇÃO DE MÚLTIPLAS PARTIDAS) ===")
    tipo_X = escolher_tipo_jogador("X (1)")
    tipo_O = escolher_tipo_jogador("O (-1)")
    
    while True:
        try:
            qtd = int(input("\nQuantas partidas deseja simular? "))
            if qtd > 0:
                break
            print("Digite um número maior que zero.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")

    vitorias_X = 0
    vitorias_O = 0
    empates = 0

    # Carrega arquivos apenas uma vez para o teste ser extremamente rápido
    memoria = carregar_memoria()
    matriz = carregar_matriz()

    print("\nIniciando simulações...")
    tempo_inicio = time.time()

    # Define o passo de feedback (10% das partidas, mínimo de 1)
    passo_feedback = max(1, int(qtd * 0.10))

    for i in range(1, qtd + 1):
        resultado, hist_X, hist_O, tab_final = jogar_partida(tipo_X, tipo_O, memoria, visual=False, jogador_inicial=1)
        
        if resultado == 1: vitorias_X += 1
        elif resultado == -1: vitorias_O += 1
        else: empates += 1
        
        # Atualiza a memória e matriz mantidas na RAM (para ser rápido)
        processar_memoria(tipo_X, tipo_O, resultado, hist_X, hist_O, memoria)
        processar_matriz_final(resultado, tab_final, matriz)
            
        # O Feedback Dinâmico de 10%
        if i % passo_feedback == 0:
            print(f"[{i} / {qtd}] partidas processadas...")

    # Salva toda a experiência de uma só vez no final
    salvar_memoria(memoria)
    salvar_matriz(matriz)
    tempo_fim = time.time()

    print("\n" + "="*30)
    print("📊 RESULTADOS DA SIMULAÇÃO 📊")
    print("="*30)
    print(f"Total de partidas: {qtd}")
    print(f"Tempo de execução: {tempo_fim - tempo_inicio:.2f} segundos")
    print(f"Vitórias do X:     {vitorias_X} ({(vitorias_X/qtd)*100:.1f}%)")
    print(f"Vitórias do O:     {vitorias_O} ({(vitorias_O/qtd)*100:.1f}%)")
    print(f"Empates:           {empates} ({(empates/qtd)*100:.1f}%)")
    print("="*30)
    print("-> Inteligência e Matriz foram salvas nos arquivos .txt com sucesso!")

def menu_principal():
    while True:
        limpar_tela()
        print("=== BEM-VINDO AO JOGO DA VELHA ===")
        print("Escolha o modo de execução:")
        print("1 - Modo Visual (Tempo real, com tabuleiro e turnos)")
        print("2 - Modo de Teste (Múltiplas partidas, sem visual)")
        print("0 - Sair")
        
        escolha = input("\nOpção: ")
        
        if escolha == '1':
            modo_visual()
            input("\nPressione Enter para voltar ao menu...")
        elif escolha == '2':
            modo_teste()
            input("\nPressione Enter para voltar ao menu...")
        elif escolha == '0':
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")
            time.sleep(1)

if __name__ == "__main__":
    menu_principal()