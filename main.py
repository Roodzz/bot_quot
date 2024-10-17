import pyautogui
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

# Variáveis globais
acoes_registradas = []  # Lista para armazenar as ações registradas
contador_loops = 0  # Contador de loops

# Função para registrar as ações do usuário
def registrar_acoes():
    global acoes_registradas
    acoes_registradas = []  # Limpa ações anteriores
    messagebox.showinfo("Instruções", "Inicie o processo manual. Ao terminar, volte e pressione 'Enter'.")
    
    while True:
        evento = pyautogui.position()  # Captura a posição atual do mouse
        acoes_registradas.append(('mouse_move', evento))
        time.sleep(0.1)  # Evita capturar dados em excesso

# Função para reproduzir as ações registradas
def reproduzir_acoes():
    for acao in acoes_registradas:
        tipo, dados = acao
        if tipo == 'mouse_move':
            pyautogui.moveTo(dados)  # Move o mouse para a posição registrada
        elif tipo == 'click':
            pyautogui.click(dados)  # Executa um clique na posição registrada
        elif tipo == 'keypress':
            pyautogui.press(dados)  # Pressiona uma tecla registrada

# Função que roda o loop automatizado a cada 5 minutos
def loop_automatizado():
    global contador_loops
    while True:
        contador_loops += 1
        atualizar_historico(f"Loop {contador_loops}: Reproduzindo ações...")
        reproduzir_acoes()  # Executa as ações gravadas
        time.sleep(300)  # Espera 5 minutos antes do próximo loop

# Função para iniciar o registro em uma thread separada
def iniciar_registro_thread():
    threading.Thread(target=registrar_acoes).start()

# Função para atualizar o histórico na interface
def atualizar_historico(mensagem):
    historico_texto.config(state=tk.NORMAL)
    historico_texto.insert(tk.END, mensagem + "\n")
    historico_texto.config(state=tk.DISABLED)

# Função para iniciar o loop de automação em uma thread separada
def iniciar_loop_thread():
    threading.Thread(target=loop_automatizado, daemon=True).start()

# Interface principal com Tkinter
def criar_interface():
    janela = tk.Tk()
    janela.title("Bot Mímico - Monitor de Ações")

    botao_registrar = tk.Button(janela, text="Iniciar Registro", command=iniciar_registro_thread)
    botao_registrar.pack(padx=20, pady=10)

    botao_iniciar_loop = tk.Button(janela, text="Iniciar Loop", command=iniciar_loop_thread)
    botao_iniciar_loop.pack(padx=20, pady=10)

    global historico_texto
    historico_texto = scrolledtext.ScrolledText(janela, width=40, height=10, state=tk.DISABLED)
    historico_texto.pack(padx=20, pady=10)

    janela.mainloop()

# Inicia a interface gráfica
criar_interface()
