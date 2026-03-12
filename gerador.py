import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

imagens = []
musica = ""

timeline_campos = []
memorias_campos = []
historia_campos = []

def selecionar_imagens():
    global imagens
    imagens = filedialog.askopenfilenames(
        title="Selecionar imagens",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
    )
    label_imgs.config(text=f"{len(imagens)} imagens selecionadas")

def selecionar_musica():
    global musica
    musica = filedialog.askopenfilename(
        title="Selecionar música",
        filetypes=[("Audio", "*.mp3 *.wav")]
    )
    label_musica.config(text="Música selecionada")

def adicionar_timeline():
    frame = tk.Frame(frame_timeline)
    frame.pack(pady=2)

    titulo = tk.Entry(frame, width=20)
    titulo.pack(side="left")

    texto = tk.Entry(frame, width=40)
    texto.pack(side="left")

    timeline_campos.append((titulo, texto))

def adicionar_memoria():
    entrada = tk.Entry(frame_memorias, width=60)
    entrada.pack(pady=2)
    memorias_campos.append(entrada)

def adicionar_historia():
    entrada = tk.Entry(frame_historia, width=60)
    entrada.pack(pady=2)
    historia_campos.append(entrada)

def gerar():

    titulo = entrada_titulo.get()
    subtitulo = entrada_subtitulo.get()

    os.makedirs("img", exist_ok=True)
    os.makedirs("audio", exist_ok=True)

    fotos_js = []

    for i, img in enumerate(imagens):

        nome = f"foto{i+1}.png"
        destino = os.path.join("img", nome)

        if os.path.abspath(img) != os.path.abspath(destino):
            shutil.copy(img, destino)

        fotos_js.append(f'"img/{nome}"')

    if musica:
        destino = os.path.abspath("audio/musica.mp3")
        origem = os.path.abspath(musica)

        if origem != destino:
            shutil.copy(origem, destino)

    fotos_string = ",\n".join(fotos_js)

    timeline_lista = []

    for t, txt in timeline_campos:
        if t.get() and txt.get():
            timeline_lista.append(
                f'{{titulo:"{t.get()}",texto:"{txt.get()}"}}'
            )

    timeline_string = ",\n".join(timeline_lista)

    historia_lista = []

    for h in historia_campos:
        if h.get():
            historia_lista.append(f'"{h.get()}"')

    historia_string = ",\n".join(historia_lista)

    memorias_lista = []

    for m in memorias_campos:
        if m.get():
            memorias_lista.append(f'"{m.get()}"')

    memorias_string = ",\n".join(memorias_lista)

    dados = f"""
const casal = {{

titulo: "{titulo}",

subtitulo: "{subtitulo}",

musica: "audio/musica.mp3",

fotos: [
{fotos_string}
],

timeline: [
{timeline_string}
],

historia: [
{historia_string}
],

memorias: [
{memorias_string}
]

}}
"""

    with open("dados.js", "w", encoding="utf-8") as f:
        f.write(dados)

    messagebox.showinfo("Sucesso", "dados.js atualizado!")

app = tk.Tk()
app.title("Love Capsule Generator")
app.geometry("650x750")

tk.Label(app, text="Título").pack()
entrada_titulo = tk.Entry(app, width=50)
entrada_titulo.pack()

tk.Label(app, text="Subtítulo").pack()
entrada_subtitulo = tk.Entry(app, width=50)
entrada_subtitulo.pack()

tk.Button(app, text="Selecionar imagens", command=selecionar_imagens).pack(pady=5)
label_imgs = tk.Label(app, text="Nenhuma imagem selecionada")
label_imgs.pack()

tk.Button(app, text="Selecionar música", command=selecionar_musica).pack(pady=5)
label_musica = tk.Label(app, text="Nenhuma música")
label_musica.pack()

tk.Label(app, text="Timeline").pack(pady=5)

frame_timeline = tk.Frame(app)
frame_timeline.pack()

tk.Button(app, text="+ adicionar evento", command=adicionar_timeline).pack()

tk.Label(app, text="História").pack(pady=5)

frame_historia = tk.Frame(app)
frame_historia.pack()

tk.Button(app, text="+ adicionar parágrafo", command=adicionar_historia).pack()

tk.Label(app, text="Memórias").pack(pady=5)

frame_memorias = tk.Frame(app)
frame_memorias.pack()

tk.Button(app, text="+ adicionar memória", command=adicionar_memoria).pack()

tk.Button(app, text="GERAR dados.js", command=gerar).pack(pady=20)

app.mainloop()