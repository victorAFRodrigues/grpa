#Pyautogui Functions
import os
from time import sleep

from pyautogui import click, locateCenterOnScreen, position, press


def start_program(path: str):
    """
    Inicia um programa no Windows a partir de um caminho.

    Args:
        path (str): Caminho para o executável ou arquivo.
    """
    os.startfile(path)


def localize_ui_element(image_path: str):
    """
    Localiza um elemento da interface na tela com base em uma imagem.

    Faz até 3 tentativas de localização antes de lançar uma exceção.

    Args:
        image_path (str): Caminho para a imagem de referência.

    Returns:
        Box: Coordenadas (x, y) do centro do elemento encontrado.
    """
    for i in range(3):
        try:
            element_position = locateCenterOnScreen(image_path, confidence=0.9, minSearchTime=2)
            if element_position:
                return element_position
        except:
            print(f'Elemento: [{image_path}] \nnão encontrado, tentando novamente em 5 segundos...')
            sleep(5)
            if i == 2:
                print('Elemento não encontrado após 3 tentativas.')
                raise


def click_on_image(image_path: str, aditional_x=0, aditional_y=0, clicks=2):
    """
    Clica em um elemento localizado na tela com base em uma imagem.

    Args:
        image_path (str): Caminho para a imagem de referência.
        aditional_x (int): Deslocamento horizontal do clique.
        aditional_y (int): Deslocamento vertical do clique.
        clicks (int): Número de cliques.
    """
    element = localize_ui_element(image_path)
    if element:
        click(x=element.x + aditional_x, y=element.y + aditional_y, clicks=clicks)
        click()


def sleep_press(key: str, seg=1):
    """
    Pressiona uma tecla e aguarda um tempo antes de prosseguir.

    Args:
        key (str): Nome da tecla a ser pressionada.
        seg (int): Tempo em segundos para aguardar.
    """
    press(key)
    sleep(seg)


def show_position(delay=3):
    """
    Mostra a posição atual do mouse após um tempo de espera.

    Args:
        delay (int): Tempo em segundos antes de capturar a posição.
    """
    sleep(delay)
    print(position())


def write_data(arr):
    """
    Digita uma lista de textos no teclado, pressionando ENTER após cada item.

    Args:
        arr (list): Lista de strings a serem digitadas.
    """
    for item in arr:
        os.write(item)
        sleep(0.5)
        press('enter')

