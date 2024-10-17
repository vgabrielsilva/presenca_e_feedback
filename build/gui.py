from pathlib import Path
from tkinter import *
from tkinter import messagebox
import sys
import requests
from bs4 import BeautifulSoup
import time
import paho.mqtt.client as mqtt
import base64
from io import BytesIO
from banco_de_imagens import *


# Definições do servidor MQTT privado HiveMQ
MQTT_SERVER = "63bd50c65ab64331beb93ad88527a44d.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "teste"
MQTT_PASSWORD = "Teste123"
MQTT_TOPIC_RECEIVE = "esp_enviar"  # Tópico para receber mensagens
MQTT_TOPIC_SEND = "py_enviar"        # Tópico para enviar mensagens

# Função chamada quando a conexão com o broker MQTT é estabelecida
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT. Código de resultado: {rc}")
    client.subscribe(MQTT_TOPIC_RECEIVE)
    print(f"Inscrito no tópico: {MQTT_TOPIC_RECEIVE}")

# Função chamada quando uma mensagem é recebida no tópico inscrito
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

# Criar o cliente MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Configurar as funções de callback
client.on_connect = on_connect
client.on_message = on_message

def mqtt_init():
    try:
        print("Inicializando cliente MQTT...")
        client.tls_set()  # Configura o uso de TLS
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Erro ao inicializar: {e}")

mqtt_init()

def mqtt_ok(mensagem):
    try:
        print("Conectando ao broker...")
        if not client.is_connected():
            client.reconnect()
        print(f"Enviando: {mensagem}")
        client.publish(MQTT_TOPIC_SEND, mensagem)
    except Exception as e:
        print(f"Erro ao conectar: {e}")



# Função para atualizar a lista de alunos
def atualizar():
    url = 'https://www.sigaa.ufs.br/sigaa/public/curso/alunos.jsf?lc=pt_BR&id=320196'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tds = soup.find_all('td')

        alunos = []
        matricula = ""

        alunos.append("comando_atualizar")
        for td in tds:
            if 'colMatricula' in td.get('class', []):
                matricula = td.text.strip()
            elif matricula:
                nome = td.text.strip()
                
                alunos.append(f"{matricula} {nome}")
                matricula = ""

        dados_alunos = "\n".join(alunos)  # Converte a lista para uma string única

        # Enviar dados via MQTT
        mqtt_ok(dados_alunos)

    else:
        print(f"Falha ao acessar a página. Status code: {response.status_code}")

# Criação da interface gráfica com Tkinter
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\gabri\Desktop\cloneGit\testedois\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_drag(event):
    x = window.winfo_pointerx() - window._offsetx
    y = window.winfo_pointery() - window._offsety
    window.geometry(f"+{x}+{y}")

def on_drag_start(event):
    window._offsetx = event.x
    window._offsety = event.y

window = Tk()
window.geometry("1075x651")
window.configure(bg="#F0F0F0")
window.overrideredirect(True)  # Remover a parte superior da janela (sem título e botão de fechar)

canvas = Canvas(
    window,
    bg="#F0F0F0",
    height=651,
    width=1075,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

barra_titulo = canvas.create_rectangle(
    0.0,
    0.0,
    1075.0,
    44.0,
    fill="#250C6B",
    outline=""
)

canvas.tag_bind(barra_titulo, "<ButtonPress-1>", on_drag_start)
canvas.tag_bind(barra_titulo, "<B1-Motion>", on_drag)


canvas.create_rectangle(
    23.0,
    135.0,
    1051.0,
    627.0,
    fill="#250C6B",
    outline="")

canvas.create_rectangle(
    590.0,
    164.0,
    1026.0,
    598.0,
    fill="#F0F0F0",
    outline="")

canvas.create_rectangle(
    49.0,
    164.0,
    485.0,
    598.0,
    fill="#F0F0F0",
    outline="")

canvas.create_text(
    447.0,
    7.0,
    anchor="nw",
    text="Área do Professor",
    fill="#F0F0F0",
    font=("Poppins Bold", 20 * -1)
)

canvas.create_text(
    54.0,
    77.0,
    anchor="nw",
    text="Atualizar lista de alunos",
    fill="#250C6B",
    font=("Poppins Bold", 16 * -1)
)





def update_counter(event):
    char_count = len(entry_1.get())
    
    if char_count == 0:
        label_counter.config(text="")

    elif char_count > 0 and char_count < 40:
        label_counter.config(text=f"{char_count}", fg="#250C6B")

    else:
        if event.keysym not in ["Delete"]:
            entry_1.delete(len(entry_1.get()) - 1)  # Remove o último 
            label_counter.config(text=f"{40}", fg="#FF0000")
    '''
    elif char_count > 40 and char_count <= 50:
        label_counter.config(text=f"{char_count}", fg="#FF0000")
    
    else:  # char_count > 50
        # Se o contador chegar a 50, bloqueia a entrada, exceto Backspace e Delete
        if event.keysym not in ["BackSpace", "Delete"]:
            entry_1.delete(len(entry_1.get()) - 1)  # Remove o último 
            label_counter.config(text=f"{40}", fg="#FF0000")
    '''
            
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    228.0,
    270.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#CACACA",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=105.0,
    y=258.0,
    width=246.0,
    height=23.0
)

label_counter = Label(window, text="", font=("Poppins", 10 * -1), fg="#250C6B")
label_counter.place(x=75.0, y=260.0)


# Vincula o evento de tecla pressionada ao Entry para atualizar o contador
entry_1.bind("<KeyRelease>", update_counter)



entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    267.0,
    446.0,
    image=entry_image_2
)

entry_2 = Text(
    bd=0,
    bg="#CACACA",
    fg="#000716",
    highlightthickness=0,
    font=("Poppins Light", 16 * -1),
    wrap='word',
    state=DISABLED
)

# scroll vertical
scrollbar = Scrollbar(window, orient="vertical", command=entry_2.yview)
entry_2.configure(yscrollcommand=scrollbar.set)

entry_2.place(
    x=105.0,
    y=330.0,
    width=304.0,  # ajustar a largura para acomodar a barra de scroll
    height=230.0
)

# posicionando scroll
scrollbar.place(
    x=412.0,  # 105 (posição x do entry_2) + 304 (largura do entry_2)
    y=330.0,
    height=232.0
)

assuntos = []
assunto_count = 1

def assuntos_formatados(assuntos):
    formatado = "comando_enviar" + ";".join([f"{idx+1}-{assunto}?" for idx, assunto in enumerate(assuntos)])
    return formatado



def atualizar_conteudo():

    entry_2.config(state=NORMAL)  # habilita a edição temporariamente
    entry_2.delete("1.0", "end")  # usado pra remover o conteúdo atual
    for i, assunto in enumerate(assuntos, start=1):
        entry_2.insert("end", f"ASSUNTO 0{i}:\n{assunto}\n\n")
    entry_2.config(state=DISABLED)  # desabilita a edição 
    assuntos_formatados(assuntos)

def comando():
    global assunto_count
    assunto = entry_1.get()

    if len(assunto) > 40:
        messagebox.showwarning("Limite de caracteres", "O assunto excede o limite de 40 caracteres.")
    elif assunto and len(assuntos) < 5:
        assuntos.append(assunto)
        atualizar_conteudo()

        entry_1.delete(0, 'end')  # Limpa o campo de entrada
        assunto_count += 1
        label_counter.config(text="")
    elif assunto and len(assuntos) == 5:
        messagebox.showwarning("Erro", "O limite de 5 assuntos foi excedido.")
    else:
        messagebox.showwarning("Erro", "Nenhum assunto foi digitado")





def apagar_primeiro_assunto():
    if len(assuntos) >= 1:
        assuntos.pop(0)
        atualizar_conteudo()

def apagar_segundo_assunto():
    if len(assuntos) >= 2:
        assuntos.pop(1)
        atualizar_conteudo()

def apagar_terceiro_assunto():
    if len(assuntos) >= 3:
        assuntos.pop(2)
        atualizar_conteudo()

def apagar_quarto_assunto():
    if len(assuntos) >= 4:
        assuntos.pop(3)
        atualizar_conteudo()

def apagar_quinto_assunto():
    if len(assuntos) >= 5:
        assuntos.pop(4)
        atualizar_conteudo()

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    808.0,
    322.5,
    image=entry_image_3
)


entry_3 = Text(
    bd=0,
    bg="#CACACA",
    fg="#000716",
    highlightthickness=0,
    font=("Poppins Light", 16 * -1),
    wrap='word',
    state=NORMAL
)
entry_3.place(
    x=646.0,
    y=250.0,
    width=324.0,
    height=143.0
)


# scroll vertical
scrollbar_dois = Scrollbar(window, orient="vertical", command=entry_3.yview)
entry_3.configure(yscrollcommand=scrollbar_dois.set)
'''
entry_3.place(
    x=105.0,
    y=330.0,
    width=304.0,  # ajustar a largura para acomodar a barra de scroll
    height=230.0
)
'''
# posicionando scroll
scrollbar_dois.place(
    x=970.0,  # 105 (posição x do entry_2) + 304 (largura do entry_2)
    y=250.0,
    height=143.0
)



entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    808.0,
    489.5,
    image=entry_image_4
)
entry_4 = Text(
    bd=0,
    bg="#CACACA",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=646.0,
    y=417.0,
    width=324.0,
    height=143.0
)

canvas.create_text(
    105.0,
    192.0,
    anchor="nw",
    text="Adicionar assuntos",
    fill="#250C6B",
    font=("Poppins Bold", 16 * -1)
)

canvas.create_text(
    105.0,
    210.0,
    anchor="nw",
    text="abordados",
    fill="#250C6B",
    font=("Poppins Bold", 16 * -1)
)

canvas.create_text(
    646.0,
    191.0,
    anchor="nw",
    text="Presença e",
    fill="#250C6B",
    font=("Poppins Bold", 16 * -1)
)

canvas.create_text(
    646.0,
    209.0,
    anchor="nw",
    text="Feedback",
    fill="#250C6B",
    font=("Poppins Bold", 16 * -1)
)

canvas.create_text(
    105.0,
    297.0,
    anchor="nw",
    text="Deseja apagar algum?",
    fill="#250C6B",
    font=("Poppins Regular", 14 * -1)
)

canvas.create_text(
    105.0,
    245.0,
    anchor="nw",
    text="max assuntos: 5",
    fill="#250C6B",
    font=("Poppins Regular", 10 * -1)
)

canvas.create_text(
    254.0,
    245.0,
    anchor="nw",
    text="max caracteres: 40",
    fill="#250C6B",
    font=("Poppins Regular", 10 * -1)
)


canvas.create_text(
    689.0,
    572.0,
    anchor="nw",
    text="Encerre o sistema para obter os resultados",
    fill="#250C6B",
    font=("Poppins Regular", 11 * -1)
)


def enviar_assunto():
    formatados = assuntos_formatados(assuntos)
    msg = (formatados)
    mqtt_ok(msg)

button_enviar_assunto = PhotoImage(
    file=relative_to_assets("button_enviar.png"))
button_enviar = Button(
    image=button_enviar_assunto,
    borderwidth=0,
    highlightthickness=0,
    command=enviar_assunto,
    relief="flat"
)
button_enviar.place(
    x=363.0,
    y=200.0,
    width=66.0,
    height=25.0
)





# botão pra adicionar assunto
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=comando,
    relief="flat"
)
button_1.place(
    x=363.0,
    y=258.0,
    width=66.0,
    height=25.0
)



def encerrar_programa():
    msg = "comando_encerrar"
    mqtt_ok(msg)
    

# botão pra encerrar e colher dados
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=encerrar_programa,
    relief="flat"
)
button_2.place(
    x=812.0,
    y=202.0,
    width=158.0,
    height=25.0
)





def iniciar():
    comando = "comando_iniciar"
    mqtt_ok(comando)

# botão pra iniciar o sistema
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=iniciar,
    relief="flat"
)
button_3.place(
    x=955.0,
    y=78.0,
    width=96.0,
    height=22.0
)





def atualizar_wifi():
    
    def centralizar_janela(janela):
        # Atualiza as tarefas da janela para garantir que as dimensões sejam precisas
        janela.update_idletasks()
        
        # Obtém as dimensões da janela
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        
        # Obtém as dimensões da tela
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        
        # Calcula as coordenadas x e y para centralizar a janela
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2
        
        # Define a geometria da janela
        janela.geometry(f"{largura}x{altura}+{x}+{y}")
    

    

    # Decodifica a string base64
    icone_bytes = base64.b64decode(icone_wifi_base64)
    icone_imagem = PhotoImage(data=icone_bytes)


    icone_conectar_format = base64.b64decode(botao_conectar_conf)
    icone_conectar_formatado = PhotoImage(data=icone_conectar_format)



    # Cria uma nova janela
    janela2 = Toplevel()
    janela2.title('WIFI')
    janela2.geometry('250x250')  # Define o tamanho da janela
    janela2.resizable(False, False)
    janela2.configure(bg='#f0f0f0')  # Define a cor de fundo
    janela2.iconphoto(False, icone_imagem)
    centralizar_janela(janela2)
    janela2.grab_set()



    label_titulo = Label(janela2, text="Conecte o ESP32", font=("Poppins Bold", 14), fg='#250C6B', bg='#f0f0f0')
    label_titulo.pack(pady=10)

    label_usuario = Label(
        janela2,
        text="Rede",
        font=("Poppins Regular", 8),
        fg='#250C6B',
        bg='#f0f0f0'
    )

    label_usuario.place(
        x = 30.5,
        y = 58.0
    )

    label_senha = Label(
        janela2,
        text="Senha",
        font=("Poppins Regular", 8),
        fg='#250C6B',
        bg='#f0f0f0'
    )

    label_senha.place(
        x = 30.5,
        y = 110.0
    )

    # Adiciona um campo de entrada
    entrada_nome = Entry(
        janela2,
        bd=0,
        bg='#CACACA',
        fg='#000716',
        highlightthickness=0,
        font=("Popping Regular", 12)
    )
 
    entrada_nome.pack(pady=15)

    entrada_senha = Entry(
        janela2,
        bd=0,
        bg='#CACACA',
        fg='#000716',
        highlightthickness=0,
        font=("Popping Regular", 12)
    )
 
    entrada_senha.pack(pady=17)


    def comando_login():

        rede = entrada_nome.get()
        senha = entrada_senha.get()

        login_enviar = (f"comando_wifi{rede}+{senha}")
        mqtt_ok(login_enviar)
        label_resposta.config(text=f"{login_enviar}")





    button_exibir = Button(
        janela2,
        image=icone_conectar_formatado,
        borderwidth=0,
        highlightthickness=0,
        command=comando_login,
        relief="flat"
    )
    button_exibir.image = icone_conectar_formatado

    button_exibir.pack(pady=12)
    
    #botao_exibir = Button(janela2, text='Mostrar Nome', command=mostrar_nome)
    #botao_exibir.pack(pady=5)

    # Rótulo para mostrar a resposta
    label_resposta = Label(janela2, text="", font=("Poppins Regular", 12), bg='#f0f0f0')
    label_resposta.pack(pady=10)

    # Adiciona um botão para fechar a nova janela
    #botao_fechar = Button(janela2, text='Fechar', command=janela2.destroy)
    #botao_fechar.pack(pady=5)






icone_botao_wifi_format = base64.b64decode(botao_wifi_png)
icone_botao_wifi_formatado = PhotoImage(data=icone_botao_wifi_format)

button_wifi = Button(
    image=icone_botao_wifi_formatado,
    borderwidth=0,
    highlightthickness=0,
    command=atualizar_wifi,
    relief="flat"
)
button_wifi.place(
    x=925.0,
    y=78.0,
    width=25.0,
    height=25.0
)














# botão pra apagar o primeiro assunto
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=apagar_primeiro_assunto,
    relief="flat"
)
button_4.place(
    x=284.0,
    y=294.0,
    width=25.0,
    height=25.0
)

# botão pra apagar o segundo assunto
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=apagar_segundo_assunto,
    relief="flat"
)
button_5.place(
    x=314.0,
    y=294.0,
    width=25.0,
    height=25.0
)

# botão pra apagar o terceiro assunto
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=apagar_terceiro_assunto,
    relief="flat"
)
button_6.place(
    x=344.0,
    y=294.0,
    width=25.0,
    height=25.0
)

# botão pra apagar o quarto assunto
button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=apagar_quarto_assunto,
    relief="flat"
)
button_7.place(
    x=374.0,
    y=294.0,
    width=25.0,
    height=25.0
)

# botão pra apagar o quinto assunto
button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=apagar_quinto_assunto,
    relief="flat"
)
button_8.place(
    x=404.0,
    y=294.0,
    width=25.0,
    height=25.0
)


# Botão para atualizar lista de alunos
button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=atualizar,
    relief="flat"
)
button_9.place(x=23.0, y=78.0, width=22.0, height=22.0)

def destruir():
    window.destroy()
    sys.exit()

# Botão para fechar o programa
button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=destruir,
    relief="flat"
)
button_10.place(x=1043.0, y=15.0, width=15.0, height=14.0)

def atualizar_relogio():
    agora = time.localtime()
    hora_str = time.strftime("%H:%M:%S", agora)
    canvas.itemconfig(texto_relogio, text=hora_str)
    window.after(1000, atualizar_relogio)

agora = time.localtime()
hora_str = time.strftime("%H:%M:%S", agora)

texto_relogio = canvas.create_text(
    461.0,
    62.0,
    anchor="nw",
    text=hora_str,
    fill="#250C6B",
    font=("Poppins Bold", 36 * -1)
)

atualizar_relogio()

window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = window.winfo_width()
window_height = window.winfo_height()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"+{x}+{y}")

window.resizable(False, False)
window.mainloop()