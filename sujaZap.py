import pyautogui as pag
import time
import random
from pynput.mouse import Listener
import pyperclip
import keyboard

frases = [
    'seu maluco',
    'doido mesmo',
    'rei da zoeira',
    'fazendo graça',
    'fala sério',
    'vai nessa',
    'malandro',
    'só besteira',
    'figura',
    'sorriso negro',
    'engraçadinho',
    'aprontando',
    'só risada',
    'talento',
    'bagunça',
    'humor',
    'artista',
    'circo',
    'nervoso',
    'aprontou',
    'cara viado',
    'piada de mulher',
    'mestre',
    'macaco',
    'bagunça',
    'apronto',
    'infame',
    'irresponsavel',
    'zoeiro'
]
posicoes = []
posicoesSairInicial = []

def on_click(x, y, button, pressed):
    if pressed:
        posicoes.append((x, y))
        print(f'Posição do clique: ({x}, {y})')

    # Após 5 cliques, para o Listener
    if len(posicoes) >= 5:
        print("5 cliques registrados:", posicoes)
        return False

def on_click_sair(x, y, button, pressed):
    if pressed:
        posicoesSairInicial.append((x, y))
        print(f'Posição do clique: ({x}, {y})')

    # Após 5 cliques, para o Listener
    if len(posicoesSairInicial) >= 3:
        print("5 cliques registrados:", posicoesSairInicial)
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


def definir_posicoes():
    posicoesCorretas = []
    posicoesSair = []
    salvo = input('Tem as posicoes de criar grupo salvas? (s/n): ')

    if salvo.lower() == 's':
        posicoes_input = input("Cole as posições salvas:")
        try:
            posicoesSalvas = eval(posicoes_input)

            if all(isinstance(i, tuple) and len(i) == 2 for i in posicoesSalvas):
                print("Posições salvas fornecidas:", posicoesSalvas)
                posicoesCorretas = posicoesSalvas
            else:
                print("Formato inválido. As posições devem ser uma lista de tuplas com 2 elementos.")
                return

        except (SyntaxError, NameError):
            print("Erro: A entrada não está no formato correto.")
            return
    else:
        print("Crie um grupo nos proximos 5 cliques para salvar as posicoes")
        time.sleep(2)
        pag.hotkey('alt','tab')

        with Listener(on_click=on_click) as listener:
            listener.join()

        print('voce escolheu: ', posicoes)
        posicoes_str = str(posicoes)

        # Copia a string da lista para o clipboard
        pyperclip.copy(posicoes_str)

        print("As posições foram copiadas para o clipboard.")
        posicoesCorretas = posicoes

    salvoSair = input('Tem as posicoes de sair salvas? (s/n): ')

    if salvoSair.lower() == 's':
        posicoes_input = input("Cole as posições salvas:")

        try:
            posicoesSairTemp = eval(posicoes_input)

            if all(isinstance(i, tuple) and len(i) == 2 for i in posicoesSairTemp):
                print("Posições salvas fornecidas:", posicoesSairTemp)
                posicoesSair = posicoesSairTemp
            else:
                print("Formato inválido. As posições devem ser uma lista de tuplas com 2 elementos.")
                return
        except (SyntaxError, NameError):
            print("Erro: A entrada não está no formato correto.")
            return
    else:
        print("Crie um grupo nos proximos 5 cliques para salvar as posicoes")
        time.sleep(2)
        pag.hotkey('alt','tab')

        with Listener(on_click=on_click_sair) as listener:
            listener.join()
        
        print('voce escolheu: ', posicoesSairInicial)
        posicoes_sair = str(posicoesSairInicial)

        pyperclip.copy(posicoes_sair)

        print("As posições foram copiadas para o clipboard.")
        posicoesSair = posicoesSairInicial

    quantidade = int(input("Quantos grupos? "))
    nome_contato = input("Nome do contato: ")
    criar_grupo(posicoesCorretas, posicoesSair, quantidade, nome_contato)
        

definir_posicoes()