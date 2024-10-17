from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scrollbar
import sys
import requests
from bs4 import BeautifulSoup
import datetime
import time

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\gabri\Desktop\cloneGit\testedois\build\assets\frame0")



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Funções para movimentar a janela com o mouse
def on_drag(event):
    x = window.winfo_pointerx() - window._offsetx
    y = window.winfo_pointery() - window._offsety
    window.geometry(f"+{x}+{y}")

def on_drag_start(event):
    window._offsetx = event.x
    window._offsety = event.y

window = Tk()

# Configuração da janela
window.geometry("1075x651")
window.configure(bg="#F0F0F0")
window.overrideredirect(True)  # Remove a parte superior da janela (sem título e botão de fechar)

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

# Retângulo superior como barra de título
barra_titulo = canvas.create_rectangle(
    0.0,
    0.0,
    1075.0,
    44.0,
    fill="#250C6B",
    outline=""
)

# Eventos para movimentar a janela
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

# Criação de uma imagem de fundo para o campo de texto
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    267.0,
    446.0,
    image=entry_image_2
)

# Criação do campo de texto
entry_2 = Text(
    bd=0,
    bg="#CACACA",
    fg="#000716",
    highlightthickness=0,
    wrap='word',  # Faz o texto quebrar automaticamente no final da linha
    state=DISABLED
)

# Criação do scrollbar vertical
scrollbar = Scrollbar(window, orient="vertical", command=entry_2.yview)
entry_2.configure(yscrollcommand=scrollbar.set)

# Posicionamento do campo de texto na janela
entry_2.place(
    x=105.0,
    y=330.0,
    width=304.0,  # Ajuste a largura para acomodar o scrollbar
    height=230.0
)

# Posicionamento do scrollbar na janela
scrollbar.place(
    x=409.0,  # 105 (posição x do entry_2) + 304 (largura do entry_2)
    y=330.0,
    height=230.0
)

# Lista para armazenar os assuntos
assuntos = []
assunto_count = 1

def atualizar_conteudo():
    entry_2.config(state=NORMAL)  # Habilita a edição temporariamente
    entry_2.delete("1.0", "end")  # Remove o conteúdo atual
    for i, assunto in enumerate(assuntos, start=1):
        entry_2.insert("end", f"Assunto {i}: {assunto}\n")  # Insere os novos conteúdos
    entry_2.config(state=DISABLED)  # Desabilita a edição novamente

def comando():
    global assunto_count
    assunto = entry_1.get()
    if assunto and len(assuntos) < 5:
        assuntos.append(assunto)
        atualizar_conteudo()
        entry_1.delete(0, 'end')  # Limpa o campo de entrada
        assunto_count += 1

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
    highlightthickness=0
)
entry_3.place(
    x=646.0,
    y=250.0,
    width=324.0,
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
    191.0,
    anchor="nw",
    text="Adicionar assuntos",
    fill="#250C6B",
    font=("Poppins Bold", 16 * -1)
)

canvas.create_text(
    105.0,
    209.0,
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
    689.0,
    573.0,
    anchor="nw",
    text="Encerre o sistema para obter os resultados",
    fill="#250C6B",
    font=("Poppins Regular", 11 * -1)
)

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

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=812.0,
    y=202.0,
    width=158.0,
    height=25.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=955.0,
    y=78.0,
    width=96.0,
    height=22.0
)

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

# Inicia o processo de atualização do relógio
atualizar_relogio()

def atualizar():
    url = 'https://www.sigaa.ufs.br/sigaa/public/curso/alunos.jsf?lc=pt_BR&id=320196'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tds = soup.find_all('td')

        alunos = []
        matricula = ""

        for td in tds:
            if 'colMatricula' in td.get('class', []):
                matricula = td.text.strip()
            elif matricula:
                nome = td.text.strip()
                alunos.append((matricula, nome))
                matricula = ""

        print("Lista de Alunos:")
        for matricula, nome in alunos:
            print(f"Matrícula: {matricula} - Nome: {nome}")
    else:
        print(f"Falha ao acessar a página. Status code: {response.status_code}")

    with open('Lista de alunos', 'w') as arquivo:
        for matricula, nome in alunos:
            #coding: utf-8
            arquivo.write(f"Matrícula: {matricula} - Nome: {nome}\n")

# Botão de atualizar os dados
button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=atualizar,
    relief="flat"
)
button_9.place(
    x=23.0,
    y=78.0,
    width=22.0,
    height=22.0
)

def destruir():
    window.destroy()
    sys.exit()

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=destruir,
    relief="flat"
)

button_10.place(
    x=1043.0,
    y=15.0,
    width=15.0,
    height=14.0
)

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
