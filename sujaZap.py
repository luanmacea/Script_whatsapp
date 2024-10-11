import pyautogui as pag
import time
import random
from pynput.mouse import Listener
import pyperclip
import keyboard
from functools import partial

import json
import os



frases = [
    'vai trabalhar',
    'voce é um amigo',
    'você é estranho'
]

def on_click(x, y, button, pressed, ammount, posicoes):
    if pressed:
        posicoes.append((x, y))
        print(f'Posição do clique: ({x}, {y})')

    # Após 5 cliques, para o Listener
    if len(posicoes) >= ammount:
        print(f"{ammount} cliques registrados:", posicoes)
        return False

def criar_grupo(posicoes, posicoesSair, quantidade, nome):
    pag.hotkey('alt','tab')
    for i in range(quantidade):

        if keyboard.is_pressed('F3'):
            print("Execução interrompida.")
            break

        #primerio bt
        pag.moveTo(posicoes[0][0], posicoes[0][1])
        pag.click()

        #Cliq new group
        pag.moveTo(posicoes[1][0], posicoes[1][1])
        pag.click()

        # digitando nome do alvo
        pag.write(nome)
        time.sleep(0.5)

        pag.moveTo(posicoes[2][0], posicoes[2][1])
        pag.click()

        time.sleep(0.5)

        pag.moveTo(posicoes[3][0], posicoes[3][1])
        pag.click()

        pag.write(f'{nome} {random.choice(frases)}')
        time.sleep(0.5)
        if keyboard.is_pressed('F3'):
            print("Execução interrompida.")
            break

        pag.moveTo(posicoes[4][0], posicoes[4][1])
        pag.click()
        time.sleep(1.2)

        #sair
        pag.moveTo(posicoesSair[0][0], posicoesSair[0][1])
        pag.click()
        time.sleep(0.5)

        pag.moveTo(posicoesSair[1][0], posicoesSair[1][1])
        pag.click()
        time.sleep(0.5)

        pag.moveTo(posicoesSair[2][0], posicoesSair[2][1])
        pag.click()
        time.sleep(0.5)
        if keyboard.is_pressed('F3'):
            print("Execução interrompida.")
            break

def salvar_posicoes_no_json(posicoes, nome_save):
    caminho_arquivo = 'configs.json'

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            dados = json.load(f)
    else:
        # Cria um novo conteúdo padrão se o arquivo não existir
        dados = {"configs": {nome_save: []}}

    # Atualiza as posições no JSON
    dados['configs'][nome_save] = posicoes

    # Salva o conteúdo atualizado de volta no arquivo
    with open(caminho_arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

def carregar_posicoes_do_json():
    caminho_arquivo = 'configs.json'

    # Verifica se o arquivo existe
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            return json.load(f)
    return None

def guardando_posicoes(texto, quantidade, nome_save):
    posicoes = []
    salvo = input(texto)

    if salvo.lower() == 's':
        posicoes_input = input("Cole as posições salvas:")
        try:
            posicoesSalvas = eval(posicoes_input)

            if all(isinstance(i, tuple) and len(i) == 2 for i in posicoesSalvas):
                print("Posições salvas fornecidas:", posicoesSalvas)
                if len(posicoesSalvas) != quantidade:
                    print("As posições salvas devem ter pelo menos", quantidade, "elementos, tente novamente.")
                    guardando_posicoes(texto, quantidade, nome_save)
                    return
                posicoes = posicoesSalvas
                salvar_posicoes_no_json(posicoes, nome_save)
            else:
                print("Formato inválido. As posições devem ser uma lista de tuplas com 2 elementos.")
                return

        except (SyntaxError, NameError):
            print("Erro: A entrada não está no formato correto.")
            return
    else:
        print(f"Crie um grupo nos proximos {quantidade} cliques para salvar as posicoes")
        print('3')
        time.sleep(0.7)
        print('2')
        time.sleep(0.7)
        print('1')
        time.sleep(0.7)
        pag.hotkey('alt','tab')

        on_click_ammount = partial(on_click, ammount=quantidade, posicoes=posicoes)
        with Listener(on_click=on_click_ammount) as listener:
            listener.join()

        time.sleep(0.3)
        pag.hotkey('alt','tab')
        print('voce escolheu: ', posicoes)
        posicoes_str = str(posicoes)

        # Copia a string da lista para o clipboard
        pyperclip.copy(posicoes_str)

        # Salva as posições no arquivo JSON
        salvar_posicoes_no_json(posicoes, nome_save)

        print("As posições foram copiadas para o clipboard.")
    return posicoes

def definir_posicoes():
    posicoesCriar = []
    posicoesSair = []

    posicoes_salvas = carregar_posicoes_do_json()

    if posicoes_salvas is not None:
        posicoesCriarSalvas = posicoes_salvas['configs'].get('posicaoCriar', [])
        posicoesSairSalvas = posicoes_salvas['configs'].get('posicaoSair', [])

        print(len(posicoesCriarSalvas))

        if (len(posicoesCriarSalvas) == 5) and (len(posicoesSairSalvas) == 3):
            confirmacao = input("Deseja utilizar as posições salvas dentro do sistema? [s/n]: ")

            if confirmacao.lower() == 's':
                posicoesCriar = posicoesCriarSalvas
                posicoesSair = posicoesSairSalvas

    if not posicoesCriar:
        posicoesCriar = guardando_posicoes("Tem as posições de criar grupo? [s/n]: ", 5, 'posicaoCriar')
    if not posicoesSair:
        posicoesSair = guardando_posicoes("Tem as posições de sair do grupo? [s/n]: ", 3, 'posicaoSair')

    quantidade = int(input("Quantos grupos? "))
    nome_contato = input("Nome do contato: ")
    criar_grupo(posicoesCriar, posicoesSair, quantidade, nome_contato)
        
definir_posicoes()