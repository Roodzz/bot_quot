import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
from tkinter import scrolledtext


API_TOKEN = 'SEU_TOKEN_AQUI'
bot = telebot.TeleBot(API_TOKEN)

mensagem_usuario = "" 
valor_manual = ""  
contador_loops = 0  

@bot.message_handler(func=lambda message: True)
def receber_mensagem(message):
    global mensagem_usuario
    mensagem_usuario = message.text
    bot.reply_to(message, "Mensagem recebida! Aguardando próxima execução...")
    print(f"Mensagem recebida: {mensagem_usuario}")

def abrir_janela_valor():
    def enviar_valor():
        global valor_manual
        valor_manual = entrada.get()  
        janela_valor.destroy() 

    janela_valor = tk.Tk()
    janela_valor.title("Inserir Valor Manual")

    label = tk.Label(janela_valor, text="Digite o valor para a automação:")
    label.pack(padx=20, pady=5)

    entrada = tk.Entry(janela_valor)
    entrada.pack(padx=20, pady=5)

    botao = tk.Button(janela_valor, text="Enviar", command=enviar_valor)
    botao.pack(padx=20, pady=10)

    janela_valor.mainloop()

def automacao_navegador():
    global contador_loops
    contador_loops += 1  

    driver = webdriver.Chrome()  
    driver.get('https://exemplo.com')
    time.sleep(5)  

    campo_valor = driver.find_element(By.NAME, 'campo-input-valor')
    campo_valor.send_keys(valor_manual)

    if "cima" in mensagem_usuario.lower():
        botao = driver.find_element(By.ID, 'botao-cima')
        acao = "CIMA"
    else:
        botao = driver.find_element(By.ID, 'botao-baixo')
        acao = "BAIXO"

    botao.click()  
    atualizar_historico(f"Loop {contador_loops}: Botão {acao}")
    driver.quit()  

def atualizar_historico(mensagem):
    historico_texto.config(state=tk.NORMAL)  
    historico_texto.insert(tk.END, mensagem + "\n")  
    historico_texto.config(state=tk.DISABLED)  

def loop_automatizado():
    while True:
        abrir_janela_valor() 
        automacao_navegador() 
        atualizar_contador()  
        print(f"Esperando 5 minutos... (Loop {contador_loops})")
        time.sleep(300)  

def atualizar_contador():
    contador_label.config(text=f"Contador de Loops: {contador_loops}")

janela_principal = tk.Tk()
janela_principal.title("Monitor de Automação")

contador_label = tk.Label(janela_principal, text=f"Contador de Loops: {contador_loops}")
contador_label.pack(padx=20, pady=10)

historico_texto = scrolledtext.ScrolledText(janela_principal, width=40, height=10, state=tk.DISABLED)
historico_texto.pack(padx=20, pady=10)

import threading
threading.Thread(target=lambda: bot.polling(), daemon=True).start()

threading.Thread(target=loop_automatizado, daemon=True).start()

janela_principal.mainloop()
