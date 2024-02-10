
from tkinter import *
from tkinter import filedialog as fd, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd


# Ventana principal
veninicial = Tk()
veninicial.title("Transformada de Fourier")
veninicial.resizable(1, 1)
veninicial.geometry("1540x750")
veninicial.config(bg="#529586") #background
veninicial.config(bd=20)   #border
veninicial.config(relief="ridge")
veninicial.config(cursor="hand2")

# Inicialización de variables
bloqueo = 0
bloqueo1 = 0
seleccion = 0
conteo = 0
funcion = 0
magnitud = 0
real = 0
polar = 0
imaginaria = 0
fig = 0
fig1 = 0
fig2 = 0
fig3 = 0
fig4 = 0
frecuencias = 0
transformadas_re = 0
transformadas_im = 0
transformadas_ra = 0


def registro():
    global funcion
    global magnitud
    global real
    global polar
    global imaginaria
    global fig
    global fig1
    global fig2
    global fig3
    global fig4

    # Gráfico de la función
    fig = Figure(figsize=(6, 3), dpi=100, facecolor=("#529586"))
    funcion = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, veninicial)
    canvas.get_tk_widget().place(x=10, y=350)
    funcion.set_title("Función")
    funcion.set_ylabel("g(t)")

    # Gráfica polar de la función
    fig1 = Figure(figsize=(3.5, 3.5), dpi=100, facecolor=("#529586"))
    polar = fig1.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig1, veninicial)
    canvas.get_tk_widget().place(x=200, y=10)
    polar.axvline(0, c="k")
    polar.axhline(0, c="k")
    polar.set_title("Función en Plano Complejo")

    # Gráfico parte Real
    fig2 = Figure(figsize=(8.5, 2), dpi=100, facecolor=("#529586"))
    real = fig2.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig2, veninicial)
    canvas.get_tk_widget().place(x=650, y=60)
    real.grid()
    real.set_title("Real")
    real.set_ylabel("re{$\^{g}(f)$}")

    # Gráfico parte Imaginaria
    fig3 = Figure(figsize=(8.5, 2), dpi=100, facecolor=("#529586"))
    imaginaria = fig3.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig3, veninicial)
    canvas.get_tk_widget().place(x=650, y=270)
    imaginaria.grid()
    imaginaria.set_title("Imaginaria")
    imaginaria.set_ylabel("im{$\^{g}(f)$}")

    # Gráfico Magnitud
    fig4 = Figure(figsize=(8.5, 2), dpi=100, facecolor=("#529586"))
    magnitud = fig4.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig4, veninicial)
    canvas.get_tk_widget().place(x=650, y=480)
    magnitud.grid()
    magnitud.set_title("Magnitud")
    magnitud.set_ylabel("|$\^{g}(f)$|")


funciones = {"sin": "np.sin", "cos": "np.cos", "tan": "np.tan", "log": "np.log",
             "pi": "np.pi", "sqrt": "np.sqrt", "exp": "np.exp", "(": "(f_dt*", "^": "**"}


def reemplazo(s):
    for i in funciones:
        if i in s:
            s = s.replace(i, funciones[i])
    return s


def tiempo():
    tiemF = float(Tiem.get())
    t = np.linspace(0.000001, tiemF, 2000)
    return t


def formula():
    global seleccion
    global bloqueo1
    global conteo
    try:
        if F_dt.get() != "" and a_dt.get() != "" and f_t.get() != "" and Tiem.get() != "" and Fre.get() != "":
            t = tiempo()
            bloqueo1 = 1
            seleccion = 1
            f_dt = int(F_dt.get())
            A_dt = int(a_dt.get())
            g_t = reemplazo(f_t.get())
            g_t = A_dt * eval(g_t)
            return g_t
        else:
            messagebox.showerror("Error", "Faltan valores de ingreso")
            bloqueo1 = 0
            conteo = 0
    except NameError:
        messagebox.showerror("Error", "Se ha introduciodo mal la función")
        for i in var:
            if i == "x" or i == "y":
                messagebox.showerror("Error", "Se debe implementar la variable t")
    except SyntaxError:
        messagebox.showerror("Error", "Se ha introduciodo mal la sintaxis")
    except ValueError:
        messagebox.showerror("Error", "Se ha introduciodo mal el número")
    except TypeError:
        messagebox.showerror("Error", "Se ha introduciodo mal la función")
        for i in var:
            if i == "x" or i == "X":
                messagebox.showerror("Error", "Se debe implementar la variable t")


def placomp():
    freT = float(Fre.get())
    constD = 299 / freT
    f_df = valescala1.get() / constD
    if seleccion == 1:
        t = tiempo()
        g_t = formula()
    else:
        aux3 = tiem_fun()
        t = aux3[0]
        g_t = aux3[1]
    re = g_t * np.cos(-2 * np.pi * f_df * t)
    im = g_t * np.sin(-2 * np.pi * f_df * t)
    centro_masa_re = sum(re) / len(re)
    centro_masa_im = sum(im) / len(im)

    return re, im, centro_masa_re, centro_masa_im


def transformada(t, g_t, f_df):
    centro_masa_re = sum(g_t * np.cos(-2 * np.pi * f_df * t)) / len(g_t * np.cos(-2 * np.pi * f_df * t))
    centro_masa_im = sum(g_t * np.sin(-2 * np.pi * f_df * t)) / len(g_t * np.sin(-2 * np.pi * f_df * t))
    radio = np.sqrt(np.power(centro_masa_re, 2) + np.power(centro_masa_im, 2))
    return centro_masa_re, centro_masa_im, radio


def datostrans():
    global frecuencias
    global transformadas_re
    global transformadas_im
    global transformadas_ra

    if seleccion == 1:
        t = tiempo()
        g_t = formula()
    else:
        aux3 = tiem_fun()
        t = aux3[0]
        g_t = aux3[1]
    freT = float(Fre.get())
    frecuencias = np.linspace(0, freT, 1025)
    transformadas_re = []
    transformadas_im = []
    transformadas_ra = []
    for frec in frecuencias:
        aux = transformada(t, g_t, frec)
        transformadas_re.append(aux[0])
        transformadas_im.append(aux[1])
        transformadas_ra.append(aux[2])
    return frecuencias, transformadas_re, transformadas_im, transformadas_ra


def graficar():
    global bloqueo
    if bloqueo1 == 1:
        try:
            bloqueo = 1
            registro()
            valescala1.set(0)

            if seleccion == 1:
                t = tiempo()
                g_t = formula()
            else:
                aux3 = tiem_fun()
                t = aux3[0]
                g_t = aux3[1]

            funcion.plot(t, g_t)
            aux1 = placomp()
            polar.plot(aux1[0], aux1[1])
            polar.scatter(aux1[2], aux1[3], c="r", s=200)
            aux2 = datostrans()
            real.plot(aux2[0], aux2[1])
            imaginaria.plot(aux2[0], aux2[2])
            magnitud.plot(aux2[0], aux2[3])
        except ValueError:
            if seleccion == 1:
                messagebox.showerror("Error", "Se ha introduciodo mal el número")
            else:
                messagebox.showerror("Error", "Verifique valor de la frecuencia de la transformada")
    else:
        messagebox.showerror("Error", "Ingrese la función o cargue sus datos")
        bloque = 0


def escala(n):
    global conteo
    conteo += 1
    if bloqueo1 == 1:
        registro()
        valescala = valescala1.get()

        if seleccion == 1:
            t = tiempo()
            g_t = formula()
        else:
            aux3 = tiem_fun()
            t = aux3[0]
            g_t = aux3[1]

        funcion.plot(t, g_t)
        aux4 = placomp()
        polar.plot(aux4[0], aux4[1])
        polar.scatter(aux4[2], aux4[3], c="r", s=200)
        aux2 = datostrans()
        real.plot(aux2[0], aux2[1])
        real.scatter(aux2[0][valescala], aux2[1][valescala], c="r", s=50)
        imaginaria.plot(aux2[0], aux2[2])
        imaginaria.scatter(aux2[0][valescala], aux2[2][valescala], c="r", s=50)
        magnitud.plot(aux2[0], aux2[3])
        magnitud.scatter(aux2[0][valescala], aux2[3][valescala], c="r", s=50)

    else:
        if conteo == 1:
            messagebox.showerror("Error", "Ingrese la función o cargue sus datos")


# Variable inicializada
ruta = 0


def crearNuevaVentana():
    global ruta
    global bloqueo1
    ruta = fd.askopenfilename(initialdir="/", title="Seleccione archivo",
                              filetypes=(("csv files", "*.csv"), ("todos los archivos", "*.*")))
    if ruta != '':
        tiem_fun()
        messagebox.showinfo("Información", "Se ha cargado correctamente la informacion")
        messagebox.showinfo("Información", "Ingrese el valor de la frecuencia de la transformada")
    else:
        messagebox.showwarning("Alerta", "No se ha ingresado la ruta de acceso")
        bloqueo1 = 0


def tiem_fun():
    global seleccion
    global bloqueo1
    seleccion = 2
    bloqueo1 = 1
    tiem = []
    func = []
    with open(ruta) as f:
        primera_linea = True
        for linea in f:
            if primera_linea:
                primera_linea = False
            else:
                func.append(float(linea.split(',')[1]))
                tiem.append(float(linea.split(',')[0]))
    tiem = np.array(tiem)
    func = np.array(func)
    return tiem, func

def guardarDat():
    if bloqueo == 1:
        nomarchivo = fd.asksaveasfilename(initialdir="/", title="Guardar como",
                                          filetypes=(("csv files", "*.csv"), ("todos los archivos", "*.*")))
        if nomarchivo != "":
            nomarchivo1 = nomarchivo + ".csv"
            data = {"W": frecuencias, "Real": transformadas_re, "Imaginaria": transformadas_im,
                    "Magnitud": transformadas_ra}
            df = pd.DataFrame(data, columns=["W", "Real", "Imaginaria", "Magnitud"])
            df.to_csv(nomarchivo1)
            messagebox.showinfo("Información", "Los datos se han guardado correctamente")
        else:
            messagebox.showwarning("Alerta", "No se ha guardado el documento")
    else:
        messagebox.showerror("Error", "No existen datos")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Llamado de la funcion registro
    registro()

    # Entrada de la función
    f_t = StringVar()
    ent1 = Entry(veninicial, textvariable=f_t, width=20)
    ent1.config(bg="white", justify="left")
    ent1.place(x=10, y=40)
    Label(veninicial, text="Ingrese la Función:").place(x=10, y=10)

    # Entrada de la frecuencia en el dominio del tiempo
    F_dt = StringVar()
    ent2 = Entry(veninicial, textvariable=F_dt, width=15)
    ent2.config(bg="white", justify="left")
    ent2.place(x=10, y=110)
    Label(veninicial, text="Frecuencia Función:").place(x=10, y=80)

    # Entrada de la amplitud
    a_dt = StringVar()
    ent3 = Entry(veninicial, textvariable=a_dt, width=15)
    ent3.config(bg="white", justify="left")
    ent3.place(x=10, y=180)
    Label(veninicial, text="Amplitud:").place(x=10, y=150)

    # Entrada de la frecuencia para la transformada
    Fre = StringVar()
    ent5 = Entry(veninicial, textvariable=Fre, width=15)
    ent5.config(bg="white", justify="left")
    ent5.place(x=10, y=250)
    Label(veninicial, text="Frecuencia Transformada:").place(x=10, y=220)

    # Entrada de tiempo
    Tiem = StringVar()
    ent4 = Entry(veninicial, textvariable=Tiem, width=15)
    ent4.config(bg="white", justify="left")
    ent4.place(x=10, y=320)
    Label(veninicial, text="Tiempo:").place(x=10, y=290)

    # Botones cargar función, cargar datos y graficar
    boton1 = Button(veninicial, text="Cargar Función", bg="white", command=formula).place(x=200, y=650)
    boton3 = Button(veninicial, text="Graficar", bg="white", command=graficar).place(x=350, y=650)
    Label(veninicial, text="Cargue los datos de la señal de entrada desde un archivo:").place(x=700, y=10)
    boton2 = Button(veninicial, text="Cargar Datos", bg="white", command=crearNuevaVentana).place(x=1100, y=10)

    # Botón guardar datos
    boton4 = Button(veninicial, text="Guardar Datos", bg="white", command=guardarDat).place(x=1300, y=10)

    # Scale
    valescala1 = IntVar()
    escala1 = Scale(veninicial, length=260, from_=0, to=1024, tickinterval=33, orient=VERTICAL, variable=valescala1,
                    command=escala).place(x=550, y=50)
    veninicial.mainloop()

    veninicial.mainloop()