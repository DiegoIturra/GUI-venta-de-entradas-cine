from tkinter import *
from tkinter import ttk
import psycopg2

class Ventana_principal(object):

	def __init__(self, parent, conexion):
		self.principal = parent
		self.conexion = conexion
		self.principal.title("CINEDB")
		self.principal.resizable(0,0) #width, height -->para no redimensionar
		self.principal.geometry("800x500")
		self.principal.config(bg = "dimgray")

		self.frame = Frame(self.principal, width = "600", height = "300", bg = 'Black')
		self.frame.place(x = 100, y = 100)
		self.label = Label(self.frame, text = "Bienvenido a CINEDB", justify = 'center', fg = "goldenrod", font = ("Bookman Old Style", 20)).place(x = 200, y = 100, width = "300", height = "150")
		self.boton = Button(self.principal, text = "Star", command = self.openFrame).place(x = 390, y = 450, width = "50", height = "30")

	def hide(self):
		self.principal.withdraw()

	def openFrame(self):
		self.hide()
		subFrame = Ventana_dos(self, self.conexion)

	def show(self):
		self.principal.update()
		self.principal.deiconify()
			

class Ventana_dos(Toplevel):

	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Opciones")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.frame = Frame(self, width = "600", height = "400", bg = 'Black')
		self.frame.pack()
		self.frame.place(x = 100, y = 50)

		self.boton1 = Button(self.frame, text = 'PELICULA', command = self.boton_pelicula)
		self.boton1.place(x = 100, y = 150, width = "100", height = "50")
		self.boton2 = Button(self.frame, text = 'CINE', command = self.boton_cine)
		self.boton2.place(x = 100, y = 250, width = "100", height = "50")

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def hide(self):
		self.withdraw()

	def boton_pelicula(self):
		self.hide()
		subFrame = Peliculas(self, self.conexion)

	def boton_cine(self):
		self.hide()
		subFrame = Cines(self, self.conexion)

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def show(self):
		self.update()
		self.deiconify()


class Peliculas(Toplevel):
	def __init__ (self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("CONFIGURACION PELICULAS")
		self.resizable(0, 0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.var = IntVar()
		self.ingresar = Label(self, text = 'INGRESAR', bg = 'darkmagenta').place(x = 100, y = 50, width = 300, height = 30)
		self.ingresar_pelicula = Radiobutton(self, text = 'Ingresar película', variable = self.var, value = 1)
		self.ingresar_pelicula.place(x = 150, y = 100)
		self.ingresar_funcion = Radiobutton(self,text = 'Ingresar función', variable = self.var, value = 2)
		self.ingresar_funcion.place(x = 150, y = 130)

		self.actualizar = Label(self, text = 'ACTUALIZAR', bg = 'darkmagenta').place(x = 100, y = 200, width = 300, height = 30)
		self.actualizar_pelicula = Radiobutton(self, text = 'Actualizar película', variable = self.var, value = 3)
		self.actualizar_pelicula.place(x = 150, y = 250)		
		self.actualizar_funcion = Radiobutton(self, text = 'Actualizar función', variable = self.var, value = 4)
		self.actualizar_funcion.place(x = 150, y = 280)

		self.eliminar = Label(self, text = 'ELIMINAR', bg = 'darkmagenta').place(x = 100, y = 350, width = 300, height = 30)
		self.eliminar_pelicula = Radiobutton(self, text = 'Eliminar película', variable = self.var, value = 5)
		self.eliminar_pelicula.place(x = 150, y = 400)
		self.eliminar_funcion = Radiobutton(self, text = 'Eliminar función', variable = self.var, value = 6)
		self.eliminar_funcion.place(x = 150, y = 430)

		self.ok_1 = Button(self, text = 'OK', command = self.openFrame).place(x = 330, y = 100, width = "100", height = "50")
		self.ok_2 = Button(self, text = 'OK', command = self.openFrame).place(x = 330, y = 250, width = "100", height = "50")
		self.ok_3 = Button(self, text = 'OK', command = self.openFrame).place(x = 330, y = 400, width = "100", height = "50")


		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def hide(self):
		self.withdraw()


	def openFrame(self):
		self.hide()
		self.num = self.var.get()

		if self.num == 1:
			subFrame = Ingresar_pel(self, self.conexion)
		elif self.num == 2:
			subFrame = Ingresar_fun(self, self.conexion)
		elif self.num == 3:
			subFrame = Actualizar_pel(self, self.conexion)
		elif self.num == 4:
			subFrame = Actualizar_fun(self, self.conexion)
		elif self.num == 5:
			subFrame = Eliminar_pel(self, self.conexion)
		elif self.num == 6:
			subFrame = Eliminar_fun(self, self.conexion)


class Cines(Toplevel):
	def __init__ (self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("CONFIGURACION CINES")
		self.resizable(0, 0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.boton_ingresar = Button(self, text = "Ingresar cine", command = self.ingresar_cine)
		self.boton_ingresar.place(x = 100, y = 100)
		
		self.boton_actualizar = Button(self, text = "Actualizar cine", command = self.actualizar_cine)
		self.boton_actualizar.place(x = 100, y = 200)

		self.boton_eliminar = Button(self, text = "Eliminar cine", command = self.eliminar_cine)
		self.boton_eliminar.place(x = 100, y = 300)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

		
	def hide(self):
			self.withdraw()

	def ingresar_cine(self):
		self.hide()
		subFrame = Ingresar_cine(self, self.conexion)

	def actualizar_cine(self):
		self.hide()
		subFrame = Actualizar_cine(self, self.conexion)

	def eliminar_cine(self):
		self.hide()
		subFrame = Eliminar_cine(self, self.conexion)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()

class Ingresar_cine(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Ingresar cine")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		#region, ciudad, codigo postal, direccion (sector, calle, numero)
		#Cadena cine 
		#nombre_cine
		
		self.nombre_region = StringVar()
		self.region = Label(self, text = "Region: ", bg = "pink").place(x = 20, y = 50, width = 130)
		self.entry_reg = Entry(self)
		self.entry_reg.place(x = 190, y = 50, width = 560)

		self.nombre_ciudad = StringVar()
		self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 20, y = 100, width = 130)
		self.entry_ciu = Entry(self)
		self.entry_ciu.place(x = 190, y = 100, width = 560)

		self.codigo_postal = IntVar()
		self.codigo = Label(self, text = "Codigo postal: ", bg = "pink", wraplength = 70).place(x = 20, y = 150, width = 130)
		self.entry_cod = Entry(self)
		self.entry_cod.place(x = 190, y = 150, width = 560)

		self.direccion = Label(self, text = "Direccion", bg = "pink").place(x = 200, y = 230, width = 130)
		self.sector_direccion = StringVar()
		self.sector = Label(self, text = "Sector: ", bg = "pink").place(x = 20, y = 280, width = 130)
		self.entry_sec = Entry(self)
		self.entry_sec.place(x = 190, y = 280, width = 560)

		self.calle_direccion = StringVar()
		self.calle = Label(self, text = "Calle: ", bg = "pink").place(x = 20, y = 320, width = 130)
		self.entry_calle = Entry(self)
		self.entry_calle.place(x = 190, y = 320, width = 200)

		self.numero_direccion = IntVar()
		self.numero = Label(self, text = "Numero: ", bg = "pink").place(x = 430, y = 320, width = 130)
		self.entry_num = Entry(self)
		self.entry_num.place(x = 570, y = 320, width = 100)


		#nombre_cine y cadena_cine se generan automaticamente
		#un cine por ciudad
		#agregar las peliculas que están disponibles en los otros cines

		self.boton = Button(self, text = "Ingresar", command = self.ingresar_BD_cines)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def ingresar_BD_cines(self):
		self.nombre_region = self.entry_reg.get()
		self.nombre_ciudad = self.entry_ciu.get()
		self.codigo_postal = self.entry_cod.get()
		self.sector_direccion = self.entry_sec.get()
		self.calle_direccion = self.entry_calle.get()
		self.numero_direccion = self.entry_num.get()


class Actualizar_cine(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Actualizar cine")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.nombre_region = StringVar()
		self.region = Label(self, text = "Region: ", bg = "pink").place(x = 20, y = 50, width = 130)
		self.lista_reg = ttk.Combobox(self, state = "normal")
		self.lista_reg["values"] = ["R1", "R2"]
		self.lista_reg.place(x = 190, y = 50, width = 560)

		self.nombre_ciudad = StringVar()
		self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 20, y = 100, width = 130)
		self.lista_ciu = ttk.Combobox(self, state = "normal")
		self.lista_ciu["values"] = ["C1", "C2"]
		self.lista_ciu.place(x = 190, y = 100, width = 560)

		self.codigo_postal = IntVar()
		self.codigo = Label(self, text = "Codigo postal: ", bg = "pink", wraplength = 70).place(x = 20, y = 150, width = 130)
		self.lista_cod = ttk.Combobox(self, state = "normal")
		self.lista_cod["values"] = ["7347", "83784"]
		self.lista_cod.place(x = 190, y = 150, width = 560)

		self.direccion = Label(self, text = "Direccion", bg = "pink").place(x = 200, y = 230, width = 130)
		self.sector_direccion = StringVar()
		self.sector = Label(self, text = "Sector: ", bg = "pink").place(x = 20, y = 280, width = 130)
		self.lista_sec = ttk.Combobox(self, state = "normal")
		self.lista_sec["values"] = ["bla", "blabla"]
		self.lista_sec.place(x = 190, y = 280, width = 560)

		self.calle_direccion = StringVar()
		self.calle = Label(self, text = "Calle: ", bg = "pink").place(x = 20, y = 320, width = 130)
		self.lista_calle = ttk.Combobox(self, state = "normal")
		self.lista_calle["values"] = ["bla bla", "bla bla"]
		self.lista_calle.place(x = 190, y = 320, width = 200)

		self.numero_direccion = IntVar()
		self.numero = Label(self, text = "Numero: ", bg = "pink").place(x = 430, y = 320, width = 130)
		self.lista_num = ttk.Combobox(self, state = "normal")
		self.lista_num["values"] = ["123", "456"]
		self.lista_num.place(x = 570, y = 320, width = 100)

		self.boton = Button(self, text = "Actualizar", command = self.actualizar_BD_cines)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def actualizar_BD_cines(self):
		self.nombre_region = self.lista_reg.get()
		self.nombre_ciudad = self.lista_ciu.get()
		self.codigo_postal = self.lista_cod.get()
		self.sector_direccion = self.lista_sec.get()
		self.calle_direccion = self.lista_calle.get()
		self.numero_direccion = self.lista_num.get()


class Eliminar_cine(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Eliminar cine")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.nombre_region = StringVar()
		self.region = Label(self, text = "Region: ", bg = "pink").place(x = 20, y = 50, width = 130)
		self.lista_reg =  ttk.Combobox(self, state = "readonlu")
		self.lista_reg["values"] = ["R1", "R2"]
		self.lista_reg.place(x = 190, y = 50, width = 560)

		self.nombre_ciudad = StringVar()
		self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 20, y = 100, width = 130)
		self.lista_ciu =  ttk.Combobox(self, state = "readonly")
		self.lista_ciu["values"] = ["C1", "C2"]
		self.lista_ciu.place(x = 190, y = 100, width = 560)

		self.nombre_cine = IntVar()
		self.cine = Label(self, text = "Cine: ", bg = "pink").place(x = 20, y = 150, width = 130)
		self.lista_cine = ttk.Combobox(self, state = "readonly")
		self.lista_cine["values"] = ["Cine SCL", "Cine CCP"]
		self.lista_cine.place(x = 190, y = 150, width = 560)

		self.boton_eliminar = Button(self, text = "Eliminar", command = self.eliminar_BD_cine)
		self.boton_eliminar.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def eliminar_BD_cine(self):
		self.nombre_region = self.lista_reg.get()
		self.nombre_ciudad = self.lista_ciu.get()
		self.nombre_cine = self.lista_cine.get()
		print(self.nombre_region)
		print(self.nombre_ciudad)
		print(self.nombre_cine)

class Ingresar_pel(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Ingresar peliculas")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.nombre_pelicula = StringVar()
		self.nombre_pel = Label(self, text = "Nombre: ", bg = "pink").place(x = 20, y = 50, width = 130)
		self.entry_pel = Entry(self)
		self.entry_pel.place(x = 190, y = 50, width = 560)

		self.duracion_pelicula = StringVar()
		self.duracion = Label(self, text = "Duración (minutos): ", bg = "pink", wraplength = 70).place(x = 20, y = 100, width = 130)
		self.entry_dur = Entry(self)
		self.entry_dur.place(x = 190, y = 100, width = 560)

		self.clasificacion_pelicula = StringVar()
		self.clasificacion = Label(self, text = "Clasificación: ", bg = "pink", wraplength = 90).place(x = 20, y = 160, width = 130)
		self.lista_clas = ttk.Combobox(self, state = "readonly")
		self.lista_clas["values"] = ["TE", "TE+7", "14", "18"]
		self.lista_clas.place(x = 190, y = 160, width = 180)

		self.estreno_pelicula = StringVar()
		self.estreno = Label(self, text = "Fecha estreno (YYYY-MM-DD): ", bg = "pink", wraplength = 120).place(x = 20, y = 190, width = 170)
		self.entry_est = Entry(self)
		self.entry_est.place(x = 190, y = 190, width = 560)

		self.productora_pelicula = StringVar()
		self.productora = Label(self, text = "Productora: ", bg = "pink").place(x = 20, y = 250, width = 170)
		self.entry_pro = Entry(self)
		self.entry_pro.place(x = 190, y = 250, width = 560)

		self.genero_pelicula1 = StringVar()
		self.genero_pelicula2 = StringVar()
		self.genero_pelicula3 = StringVar()
		self.genero_pelicula4 = StringVar()
		self.genero_pelicula5 = StringVar()
		self.genero_pelicula6 = StringVar()
		self.genero = Label(self, text = "Generos: (hasta 6)", bg = "pink", wraplength = 70).place(x = 20, y = 280, width = 170)
		self.entry_gen1 = Entry(self)
		self.entry_gen1.place(x = 190, y = 280, width = 180)
		self.entry_gen2 = Entry(self)
		self.entry_gen2.place(x = 380, y = 280, width = 180)
		self.entry_gen3 = Entry(self)
		self.entry_gen3.place(x = 570, y = 280, width = 180)
		self.entry_gen4 = Entry(self)
		self.entry_gen4.place(x = 190, y = 310, width = 180)
		self.entry_gen5 = Entry(self)
		self.entry_gen5.place(x = 380, y = 310, width = 180)
		self.entry_gen6 = Entry(self)
		self.entry_gen6.place(x = 570, y = 310, width = 180)

		self.boton = Button(self, text = "Ingresar", command = self.ingresar_BD_peliculas)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def ingresar_BD_peliculas(self):
		self.nombre_pelicula = self.entry_pel.get()
		self.duracion_pelicula = self.entry_dur.get()
		self.clasificacion_pelicula = self.lista_clas.get()
		self.estreno_pelicula = self.entry_est.get()
		self.productora_pelicula = self.entry_pro.get()

		self.genero_pelicula1 = self.entry_gen1.get()
		self.genero_pelicula2 = self.entry_gen2.get()
		self.genero_pelicula3 = self.entry_gen3.get()
		self.genero_pelicula4 = self.entry_gen4.get()
		self.genero_pelicula5 = self.entry_gen5.get()
		self.genero_pelicula6 = self.entry_gen6.get()

		if self.genero_pelicula1 != "":
			print(self.genero_pelicula1)
		if self.genero_pelicula2 != "":
			print(self.genero_pelicula2)
		if self.genero_pelicula3 != "":
			print(self.genero_pelicula3)
		if self.genero_pelicula4 != "":
			print(self.genero_pelicula4)
		if self.genero_pelicula5 != "":
			print(self.genero_pelicula5)
		if self.genero_pelicula6 != "":
			print(self.genero_pelicula6)

		#CREAR CONSULTA AQUI

class Ingresar_fun(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Ingresar funciones")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		#formato, idioma, fecha, salas, hora_inicio, hora_final
		cursor = conexion.cursor()

		self.nombre_region = StringVar()
		self.region = Label(self, text = "Región: ", bg = "pink").place(x = 20, y = 60, width = 130)
		self.lista_reg = ttk.Combobox(self, state = "readonly")
		#----------------------------------------------------------
		SQL = "SELECT region FROM ps.ciudadyregion" # Note: no quotes
		#data = ("O'Reilly", )
		cursor.execute(SQL) # Note: no % operator
		self.regiones = cursor.fetchall()
		#----------------------------------------------------------
		self.lista_reg["values"] = self.regiones
		self.lista_reg.place(x = 190, y = 60, width = 150)
		self.lista_reg.bind("<<ComboboxSelected>>",self.enableWidgets)

		self.nombre_ciudad = StringVar()
		self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 400, y = 60, width = 130)
		self.lista_ciu = ttk.Combobox(self, state = "disabled")
		#-----------------------------------------------------------------------------------------
		#cursor.execute("SELECT nombre_ciudad FROM ps.ciudadyregion WHERE region = %s", (self.nombre_region,))
		
		#-----------------------------------------------------------------------------------------
		self.lista_ciu["values"] = ["hgh"]
		self.lista_ciu.bind("<<ComboboxSelected>>",self.enableWidgets)
		self.lista_ciu.place(x = 560, y = 60, width = 150)

		self.nombre_cine = StringVar()
		self.cine = Label(self, text = "Escoja cine: ", bg = "pink").place(x = 20, y = 100, width = 130) 
		self.lista_cine = ttk.Combobox(self, state = "disabled")
		#-------------------------------------------------------------------------------------------

		#-------------------------------------------------------------------------------------------
		self.lista_cine["values"] = ["Cine AP", "Cine SCL", "Cine CCP", "Cine MG"]
		self.lista_cine.place(x = 190, y = 100, width = 560)

		self.nombre_pelicula = StringVar()
		self.pelicula = Label(self, text = "Escoja pelicula: ", bg = "pink").place(x = 20, y = 140, width = 130)
		self.lista_pel = ttk.Combobox(self, state = "disabled")
		#-------------------------------------------------------------------------------------------

		#-------------------------------------------------------------------------------------------
		self.lista_pel["values"] = ["Peli 1", "Peli 2", "Peli 3", "Peli 4"]
		self.lista_pel.place(x = 190, y = 140, width = 560)

		self.formato_funcion = StringVar()
		self.formato = Label(self, text = "Formato: ", bg = "pink").place(x = 20, y = 180, width = 130)
		self.lista_form = ttk.Combobox(self, state = "readonly")
		self.lista_form["values"] = ["2D", "3D", "4D", "XD"]
		self.lista_form.place(x = 190, y = 180, width = 560)

		self.fecha_funcion = StringVar()
		self.fecha_fun = Label(self, text = "Fecha: (YYYY-MM-DD)", bg = "pink", wraplength = 60).place(x = 20, y = 220, width = 130)#160
		self.fecha = Entry(self)
		self.fecha.place(x = 190, y = 220, width = 560)

		self.salas_disponibles = StringVar()
		self.salas = Label(self, text = "Salas disponibles: ", bg = "pink", wraplength = 70).place(x = 20, y = 300, width = 130)#240
		self.lista_salas = ttk.Combobox(self, state = "disabled")
		#-------------------------------------------------------------------------------------------

		#-------------------------------------------------------------------------------------------
		self.lista_salas["values"] = ["1", "2", "3"]
		self.lista_salas.place(x = 190, y = 300, width = 560)

		self.hora_funcion = StringVar()
		self.hora_fun = Label(self, text = "Hora inicio: (00:00:00)", bg = "pink", wraplength = 90).place(x = 20, y = 380, width = 130)#320
		self.hora = Entry(self)
		self.hora.place(x = 190, y = 380, width = 560)

		self.boton = Button(self, text = "Ingresar", command = self.ingresar_BD_funciones)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

		self.nombre_region = self.lista_reg.get()
		self.data = (self.nombre_region)

		self.nombre_region = self.lista_reg.get()
		print(self.nombre_region)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def ingresar_BD_funciones(self):
		self.nombre_region = self.lista_reg.get()
		self.nombre_ciudad = self.lista_ciu.get()
		self.nombre_cine = self.lista_cine.get()
		self.nombre_pelicula = self.lista_pel.get()
		self.formato_funcion = self.lista_form.get()
		self.fecha_funcion = self.fecha.get()
		self.salas_disponibles = self.lista_salas.get()
		self.hora_funcion = self.hora.get()

	def enableWidgets(self,event):
		""" se van activando los widgets a medida que se seleccionan los anteriores """
		if self.lista_reg.get() != "":
			self.nombre_region = self.lista_reg.get()
			self.lista_ciu.config(state = 'readonly')
		if self.lista_ciu.get() != "":
			self.nombre_ciudad = self.lista_ciu.get()

		#HACER CONSULTA

class Actualizar_pel(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Actualizar películas")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.nombre_pelicula = StringVar()
		self.nombre_pel = Label(self, text = "Nombre: ", bg = "pink").place(x = 20, y = 50, width = 130)
		self.entry_pel = ttk.Combobox(self, state = "normal")
		self.entry_pel["values"] = ["Peli 1", "Peli 2", "Peli 3"]
		self.entry_pel.place(x = 190, y = 50, width = 560)

		self.duracion_pelicula = StringVar()
		self.duracion = Label(self, text = "Duración (minutos): ", bg = "pink", wraplength = 70).place(x = 20, y = 100, width = 130)
		self.entry_dur = ttk.Combobox(self, state = "normal")
		self.entry_dur["values"] = ["308"]
		self.entry_dur.place(x = 190, y = 100, width = 560)

		self.clasificacion_pelicula = StringVar()
		self.clasificacion = Label(self, text = "Clasificación: ", bg = "pink", wraplength = 90).place(x = 20, y = 160, width = 130)
		self.lista_clas = ttk.Combobox(self, state = "normal")
		self.lista_clas["values"] = ["TE", "TE+7", "14", "18"]
		self.lista_clas.place(x = 190, y = 160, width = 180)

		self.estreno_pelicula = StringVar()
		self.estreno = Label(self, text = "Fecha estreno (YYYY-MM-DD): ", bg = "pink", wraplength = 120).place(x = 20, y = 190, width = 170)
		self.entry_est = ttk.Combobox(self, state = "normal")
		self.entry_est["values"] = ["2019-08-23"]
		self.entry_est.place(x = 190, y = 190, width = 560)

		self.productora_pelicula = StringVar()
		self.productora = Label(self, text = "Productora: ", bg = "pink").place(x = 20, y = 250, width = 170)
		self.entry_pro = ttk.Combobox(self, state = "normal")
		self.entry_pro["values"] = ["Disney"]
		self.entry_pro.place(x = 190, y = 250, width = 560)

		self.genero_pelicula1 = StringVar()
		self.genero_pelicula2 = StringVar()
		self.genero_pelicula3 = StringVar()
		self.genero_pelicula4 = StringVar()
		self.genero_pelicula5 = StringVar()
		self.genero_pelicula6 = StringVar()
		self.genero = Label(self, text = "Generos: (hasta 6)", bg = "pink", wraplength = 70).place(x = 20, y = 280, width = 170)
		self.entry_gen1 = ttk.Combobox(self, state = "normal")
		self.entry_gen1["values"] = ["Disney"]
		self.entry_gen1.place(x = 190, y = 280, width = 180)
		self.entry_gen2 = ttk.Combobox(self, state = "normal")
		self.entry_gen2["values"] = ["Disney"]
		self.entry_gen2.place(x = 380, y = 280, width = 180)
		self.entry_gen3 = ttk.Combobox(self, state = "normal")
		self.entry_gen3["values"] = ["Disney"]
		self.entry_gen3.place(x = 570, y = 280, width = 180)
		self.entry_gen4 = ttk.Combobox(self, state = "normal")
		self.entry_gen4["values"] = ["Disney"]
		self.entry_gen4.place(x = 190, y = 310, width = 180)
		self.entry_gen5 = ttk.Combobox(self, state = "normal")
		self.entry_gen5["values"] = ["Disney"]
		self.entry_gen5.place(x = 380, y = 310, width = 180)
		self.entry_gen6 = ttk.Combobox(self, state = "normal")
		self.entry_gen6["values"] = ["Disney"]
		self.entry_gen6.place(x = 570, y = 310, width = 180)

		self.boton = Button(self, text = "Actualizar", command = self.actualizar_BD_peliculas)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def actualizar_BD_peliculas(self):
		self.nombre_pelicula = self.entry_pel.get()
		self.duracion_pelicula = self.entry_dur.get()
		self.clasificacion_pelicula = self.lista_clas.get()
		self.estreno_pelicula = self.entry_est.get()
		self.productora_pelicula = self.entry_pro.get()

		self.genero_pelicula1 = self.entry_gen1.get()
		self.genero_pelicula2 = self.entry_gen2.get()
		self.genero_pelicula3 = self.entry_gen3.get()
		self.genero_pelicula4 = self.entry_gen4.get()
		self.genero_pelicula5 = self.entry_gen5.get()
		self.genero_pelicula6 = self.entry_gen6.get()

		if self.genero_pelicula1 != "":
			print(self.genero_pelicula1)
		if self.genero_pelicula2 != "":
			print(self.genero_pelicula2)
		if self.genero_pelicula3 != "":
			print(self.genero_pelicula3)
		if self.genero_pelicula4 != "":
			print(self.genero_pelicula4)
		if self.genero_pelicula5 != "":
			print(self.genero_pelicula5)
		if self.genero_pelicula6 != "":
			print(self.genero_pelicula6)




class Actualizar_fun(Toplevel): #--------------> debe pedir la funcion que se quiere actualizar en especifico
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Actualizar funciones")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.nombre_region = StringVar()
		self.region = Label(self, text = "Región: ", bg = "pink").place(x = 20, y = 60, width = 130)
		self.lista_reg = ttk.Combobox(self, state = "readonly")
		self.lista_reg["values"] = ["Region 1", "Region 2", "Region 3"]
		self.lista_reg.place(x = 190, y = 60, width = 150)

		self.nombre_ciudad = StringVar()
		self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 400, y = 60, width = 130)
		self.lista_ciu = ttk.Combobox(self, state = "readonly")
		self.lista_ciu["values"] = ["Ciudad 1", "Ciudad 2", "Ciudad 3"]
		self.lista_ciu.place(x = 560, y = 60, width = 150)

		self.nombre_cine = StringVar()
		self.cine = Label(self, text = "Escoja cine: ", bg = "pink").place(x = 20, y = 100, width = 130)
		self.lista_cine = ttk.Combobox(self, state = "readonly")
		self.lista_cine["values"] = ["Cine AP", "Cine SCL", "Cine CCP", "Cine MG"]
		self.lista_cine.place(x = 190, y = 100, width = 560)

		self.nombre_pelicula = StringVar()
		self.pelicula = Label(self, text = "Escoja pelicula: ", bg = "pink").place(x = 20, y = 140, width = 130)
		self.lista_pel = ttk.Combobox(self, state = "readonly")
		self.lista_pel["values"] = ["Peli 1", "Peli 2", "Peli 3", "Peli 4"]
		self.lista_pel.place(x = 190, y = 140, width = 560)

		self.funcion = StringVar()
		self.funciones = Label(self, text = "Función: ", bg = "pink").place(x = 20, y = 180, width = 130)
		self.lista_fun = ttk.Combobox(self, state = "normal")
		self.lista_fun["values"] = ["Fun1", "Fun2", "Fun3", "Fun4"] 
		self.lista_fun.place(x = 190, y = 180, width = 150)

		self.formato_funcion = StringVar()
		self.formato = Label(self, text = "Formato: ", bg = "pink").place(x = 400, y = 180, width = 130)
		self.lista_form = ttk.Combobox(self, state = "normal")
		self.lista_form["values"] = ["2D", "3D", "4D", "XD"] 
		self.lista_form.place(x = 560, y = 180, width = 150)

		self.fecha_funcion = StringVar()
		self.fecha_fun = Label(self, text = "Fecha: (YYYY-MM-DD)", bg = "pink", wraplength = 60).place(x = 20, y = 220, width = 130)
		self.lista_fec = ttk.Combobox(self, state = "normal")
		self.lista_fec["values"] = ["2019-04-23"]
		self.lista_fec.place(x = 190, y = 220, width = 560)

		self.salas_disponibles = StringVar()
		self.salas = Label(self, text = "Salas disponibles: ", bg = "pink", wraplength = 70).place(x = 20, y = 300, width = 130)
		self.lista_salas = ttk.Combobox(self, state = "readonly") #muestra las salas disponibles
		self.lista_salas["values"] = ["1", "2", "3"]
		self.lista_salas.place(x = 190, y = 300, width = 560)

		self.hora_funcion = StringVar()
		self.hora_fun = Label(self, text = "Hora inicio: (00:00:00)", bg = "pink", wraplength = 90).place(x = 20, y = 380, width = 130)
		self.lista_hora = ttk.Combobox(self, state = "normal")
		self.lista_hora["values"] = ["12:34:00", "12:20:00"]
		self.lista_hora.place(x = 190, y = 380, width = 560)

		self.boton = Button(self, text = "Actualizar", command = self.actualizar_BD_funciones)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()
		

	def actualizar_BD_funciones(self):
		self.nombre_region = self.lista_reg.get()
		self.nombre_ciudad = self.lista_ciu.get()
		self.nombre_cine = self.lista_cine.get()
		self.nombre_pelicula = self.lista_pel.get()
		self.funcion = self.lista_fun.get()
		self.formato_funcion = self.lista_form.get()
		self.fecha_funcion = self.lista_fec.get()
		self.salas_disponibles = self.lista_salas.get()
		self.hora_funcion = self.lista_hora.get()


class Eliminar_pel(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Eliminar películas")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.nombre_pelicula = StringVar()
		self.pelicula = Label(self, text = "Escoja película: ", bg = "pink").place(x = 100, y = 100, width = 130)
		self.lista_pel = ttk.Combobox(self, state = "readonly")
		self.lista_pel["values"] = ["Peli 1", "Peli 2", "Peli 3"]
		self.lista_pel.place(x = 300, y = 100, width = 400)

		self.boton = Button(self, text = "Eliminar", command = self.eliminar_BD_peliculas)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def eliminar_BD_peliculas(self):
		self.nombre_pelicula = self.lista_pel.get()
		print(self.nombre_pelicula)

class Eliminar_fun(Toplevel):
	def __init__(self, wind, conexion):
		self.wind = wind
		self.conexion = conexion
		Toplevel.__init__(self)
		self.title("Eliminar funciones")
		self.resizable(0,0)
		self.geometry("800x500")
		self.config(bg = 'dimgray')

		self.nombre_region = StringVar()
		self.region = Label(self, text = "Región: ", bg = "pink").place(x = 100, y = 100, width = 130)
		self.lista_reg = ttk.Combobox(self, state = "readonly")
		self.lista_reg["values"] = ["Region 1", "Region 2", "Region 3"]
		self.lista_reg.place(x = 300, y = 100, width = 400)

		self.nombre_ciudad = StringVar()
		self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 100, y = 140, width = 130)
		self.lista_ciu = ttk.Combobox(self, state = "readonly")
		self.lista_ciu["values"] = ["Ciudad 1", "Ciudad 2", "Ciudad 3"]
		self.lista_ciu.place(x = 300, y = 140, width = 400)

		self.nombre_cine = StringVar()
		self.cine = Label(self, text = "Cine: ", bg = "pink").place(x = 100, y = 180, width = 130)
		self.lista_cine = ttk.Combobox(self, state = "readonly")
		self.lista_cine["values"] = ["Cine 1", "Cine 2", "Cine 3"]
		self.lista_cine.place(x = 300, y = 180, width = 400)

		self.nombre_pelicula = StringVar()
		self.pelicula = Label(self, text = "Pelicula: ", bg = "pink").place(x = 100, y = 220, width = 130)
		self.lista_pel = ttk.Combobox(self, state = "readonly")
		self.lista_pel["values"] = ["Peli 1", "Peli 2", "Peli 3"]
		self.lista_pel.place(x = 300, y = 220, width = 400)

		self.funciones = StringVar()
		self.funcion = Label(self, text = "Función: ", bg = "pink").place(x = 100, y = 260, width = 130)
		self.lista_fun = ttk.Combobox(self, state = "readonly")
		self.lista_fun["values"] = ["Funcion 1", "Funcion 2", "Funcion 3"]
		self.lista_fun.place(x = 300, y = 260, width = 400)

		self.boton = Button(self, text = "Eliminar", command = self.eliminar_BD_funciones)
		self.boton.place(x = 300, y = 450)

		self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
		self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

	def show(self):
		self.update()
		self.deiconify()

	def volverAtras(self):
		self.destroy()
		self.wind.show()

	def eliminar_BD_funciones(self):
		self.nombre_region = self.lista_reg.get()
		self.nombre_ciudad = self.lista_ciu.get()
		self.nombre_cine = self.lista_cine.get()
		self.nombre_pelicula = self.lista_pel.get()
		self.funciones = self.lista_fun.get()

		print(self.nombre_region)
		print(self.nombre_ciudad)
		print(self.nombre_cine)
		print(self.nombre_pelicula)
		print(self.funciones)

if __name__ == '__main__':

	miConexion = psycopg2.connect(user="bdi2019p", password="bdi2019p", host="plop.inf.udec.cl", database="bdi2019p", port=5432)

	parent = Tk()
	app = Ventana_principal(parent, miConexion)	
	parent.mainloop()

	miConexion.close()

