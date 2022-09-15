import tkinter

ventana = tkinter.Tk()
ventana.geometry("400x800")
botonStart = tkinter.Button(ventana, text="Start Fishing", command = saludo)
botonStart.pack()
ventana.mainloop()