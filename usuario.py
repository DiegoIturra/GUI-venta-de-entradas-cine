from tkinter import *
from tkinter import ttk
import psycopg2
from contextlib import contextmanager
from datetime import date,datetime
import string

#--------------------------clase para conectar a la base de datos------------------------------------------
class ConexionBaseDeDatos():

	def __init__(self,ruta):
		self.ruta = ruta

	def __enter__(self):
		self.conexion = psycopg2.connect(self.ruta)
		return self.conexion.cursor()

	def __exit__(self,exc_class,exc,traceback):
		self.conexion.commit()
		self.conexion.close()

#--------------------- funcion decoradora  -----------------------------------------------------------------------
def ejecutarSentenciaSQL(consulta,*valores):
    def decoradorConsulta(funcion):
        def funcionDecorada(*valores):
            ruta = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"
            with ConexionBaseDeDatos(ruta) as sentencia:
                sentencia.execute(consulta,*valores)
                listaDatos = sentencia.fetchall()
            return listaDatos
        return funcionDecorada
    return decoradorConsulta

#-----------------------------------Frame principal de la aplicacion (version usuario)----------------------------
class VentanaPrincipal(object):
	#Constructor
	def __init__(self,parent):
		self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"
		self.nombreCiudad = ""
		self.root = parent
		self.root.title("Bienvenidos a CineDB")
		self.root.resizable(False,False)

		#frame sobre la ventana pricipal
		self.frame = Frame(parent,width="500",height="250")
		self.frame.pack()

		#Label con el logo sobre el frame
		logo = Label(self.frame,text="CineDB",justify="center")
		logo.place(x=50,y=30,width=400,height=100)

		#listas desplegables y boton de botonBuscar
		self.listaRegion = ttk.Combobox(self.frame,state='readonly') #solo lista desplegable(no caja de texto)
		self.listaRegion.place(x=50,y=150,width=200,height=30)
		self.listaRegion["values"] = self.obtenerRegion()
		self.listaRegion.bind("<<ComboboxSelected>>",self.enableWidgets)

		self.nombreRegion = self.listaRegion.get() #prueba

		self.listaCiudad = ttk.Combobox(self.frame,state='disabled')
		self.listaCiudad.place(x=280,y=150,width=200,height=30)
		self.listaCiudad.bind("<<ComboboxSelected>>",self.enableWidgets)

		self.listaCine = ttk.Combobox(self.frame,state='disabled')
		self.listaCine.place(x=50,y=200,width=200,height=30) 	
		self.listaCine.bind("<<ComboboxSelected>>",self.enableWidgets)

		self.botonBuscar = Button(self.frame , text="buscar",padx=20,pady=20,command=self.openFrame)
		self.botonBuscar.place(x=280,y=200,width=200,height=40)
		self.botonBuscar.config(state='disabled')


	@ejecutarSentenciaSQL("SELECT region FROM ps.ciudadyregion")
	def obtenerRegion(self):
		pass

	def obtenerCiudad(self):
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT nombre_ciudad FROM ps.ciudadyregion WHERE region = %s",(self.nombreRegion,))
			listaCiudades = sentencia.fetchall()
		return listaCiudades

	def obtenerCine(self):
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT nombre_cine FROM ps.cine WHERE codigo_postal = (SELECT codigo_postal FROM ps.ciudad WHERE nombre_ciudad = %s)",(self.nombreCiudad,))
			listaCines = sentencia.fetchall()
		return listaCines


	def enableWidgets(self,event):
		""" se van activando los widgets a medida que se seleccionan los anteriores """
		if self.listaRegion.get() != "":
			self.listaRegion["values"] = self.obtenerRegion() #pasarle las regiones obtenidas en la BD
			self.nombreRegion = self.listaRegion.get()#obtener la region seleccionada
			self.nombreRegion = self.nombreRegion.rstrip('}') #parsear
			self.nombreRegion = self.nombreRegion.lstrip('{') #parsear
			self.listaCiudad["values"] = self.obtenerCiudad() #pasarle la ciudad de acuerdo a la region seleccionada
			self.listaCiudad.config(state='readonly') #activar la casilla
			if self.listaCiudad.get() != "":
				self.listaCiudad["values"] = self.obtenerCiudad()
				self.nombreCiudad = self.listaCiudad.get()
				self.nombreCiudad = self.nombreCiudad.rstrip('}')
				self.nombreCiudad = self.nombreCiudad.lstrip('{')
				self.listaCine["values"] = self.obtenerCine()
				self.listaCine.config(state='readonly') #activar la casilla
				if self.listaCine.get() != "":
					self.nombreCine = self.listaCine.get()
					self.botonBuscar.config(state='active')

	def getNombreCine(self):
		self.nombreCine = self.nombreCine.rstrip('}')
		self.nombreCine = self.nombreCine.lstrip('{')
		return self.nombreCine

	def hide(self):
		self.root.withdraw()

	def openFrame(self):
		self.hide()
		subFrame = VentasCine(self)

	def mostrarFrame(self):
		self.show()

	def show(self):
		self.root.update()
		self.root.deiconify()


#----------------------------------Frame que muestar info del Cine ------------------------------------------
#a esta ventana se le pasa el nombre del cine para poder hacer
#las consultas con respecto a la funcion
class VentasCine(Toplevel):

	def __init__(self,mainWindow):
		self.mainWindow = mainWindow
		self.nombreCine = self.mainWindow.getNombreCine() #prueba
		self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"
		Toplevel.__init__(self)

		self.nombrePelicula = ""

		self.title("Ventas CineDB")
		self.resizable(False,False)

		self.frame = Frame(self,width="640",height="480")
		self.frame.pack()

		self.botonCerrar = Button(self.frame , text = "X",command=self.cerrarFrame)
		self.botonCerrar.place(x=570,y=30,width=50,height=40)
		self.botonCerrar.config(bg="red",fg="white")

		self.botonAtras = Button(self.frame , text="<--",command=self.volverAtras,bg="green",fg="white")
		self.botonAtras.place(x=30,y=30,width=50,height=40)

		self.botonCartelera = Button(self.frame , text="Ver Cartelera",command=lambda:self.activarWidgets("<<ComboboxSelected>>"))
		self.botonCartelera.place(x=110,y=30,width=200,height=40)

		self.botonCombos = Button(self.frame , text="Ver Combos",command=self.abrirFrameComida)
		self.botonCombos.place(x=340,y=30,width=200,height=40)

		self.listaPelicula = ttk.Combobox(self.frame,state='disabled')
		self.listaPelicula.place(x=110,y=100,width=430, height=30)
		self.listaPelicula.bind("<<ComboboxSelected>>",self.activarWidgets)

		self.infoPelicula = Text(self.frame , wrap='word',state='normal')
		self.infoPelicula.place(x=30,y=160,width=300,height=310)

		self.listaFunciones = ttk.Combobox(self.frame,state='disabled')
		self.listaFunciones.place(x=360,y=160,width=180,height=30)
		self.listaFunciones.bind("<<ComboboxSelected>>",self.activarWidgets)

		self.listaHorarios = ttk.Combobox(self.frame,state='disabled')
		self.listaHorarios.place(x=360,y=220,width=180,height=30)
		self.listaHorarios.bind("<<ComboboxSelected>>",self.activarWidgets)

		self.labelformato = Label(self.frame,text="Formato: ",anchor='w')
		self.labelformato.place(x=360,y=280,width=180,height=20)

		self.labelPrecio = Label(self.frame , text="Precio: " ,anchor='w')
		self.labelPrecio.place(x=360,y=300,width=180,height=20)

		self.botonContinuar = Button(self.frame , text="Continuar",command=self.mostrarAsientosSala)
		self.botonContinuar.place(x=360,y=360,width=180,height=40)
		self.botonContinuar.config(state='disabled')

		self.isClicked = False #antes de que se oprima el boton cartelera por primera vez

	def abrirFrameComida(self):
		"""abre una ventana que permite la compra de combos de comida"""
		frameComida = FrameVentaComida(self)

	def mostrarAsientosSala(self):
		"""abre un ventana que visualiza los asientos a comprar"""
		frameAsientos = SalaCine(self,self.getClaveFuncion())


	@ejecutarSentenciaSQL("SELECT id_pelicula,nombre_pelicula FROM ps.pelicula ORDER BY id_pelicula")
	def obtenerPelicula(self):
		pass

	def obtenerFechaFuncion(self):
		"""retorna las fechas para una pelicula en un cine especificado y que corresponda al codigo de la pelicula"""
		self.idPelicula = self.listaPelicula.get().split()
		self.idPelicula = self.idPelicula[0]
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT DISTINCT fecha FROM ps.funcion WHERE nombre_cine = %s AND id_pelicula = %s",(self.nombreCine,self.idPelicula,))
			fechas = sentencia.fetchall()
		return fechas

	def obtenerHorarioFuncion(self):
		"""retorna los horarios en una fecha especificada en un cine dado y un codigo de pelicula dado"""
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT hora_inicio FROM ps.funcion WHERE nombre_cine = %s AND id_pelicula = %s\
								AND fecha = (SELECT DISTINCT fecha FROM ps.funcion WHERE fecha = %s AND nombre_cine = %s\
								AND id_pelicula = %s)",
								(self.nombreCine,self.idPelicula,self.fechaSeleccionada,self.nombreCine,self.idPelicula,))
			horarios = sentencia.fetchall()
		return horarios

	def __getNumSala(self):
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT numero_sala FROM ps.funcion WHERE id_pelicula = %s\
								AND fecha = %s AND hora_inicio = %s AND nombre_cine = %s",(self.idPelicula,
								self.fechaSeleccionada,self.horaSeleccionada,self.nombreCine,))
			numSala = sentencia.fetchone()
		numSala = numSala[0]
		return numSala

	def setearInfoPelicula(self):
		"""setea el widget Text con la informacion relevante sobre la pelicula seleccionada en el Combobox de 
		seleccion de peliculas"""
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT nombre_pelicula,duracion,clasificacion,estreno,productora FROM ps.pelicula\
								WHERE id_pelicula = %s",(self.idPelicula,))
			nombrePelicula,duracion,clasificacion,estreno,productora = sentencia.fetchone()
		self.infoPelicula.config(state='normal')
		self.infoPelicula.delete('1.0',END)
		self.infoPelicula.insert('end',"nombre: "+str(nombrePelicula) + '\n')
		self.infoPelicula.insert('end',"duracion: "+str(duracion) + '\n')
		self.infoPelicula.insert('end',"clasificacion: "+str(clasificacion) + '\n')
		self.infoPelicula.insert('end',"estreno: "+str(estreno) + '\n')
		self.infoPelicula.insert('end',"productora: "+str(productora) + '\n')
		self.infoPelicula.config(state='disabled')

	def setearValores(self):
		"""setea los labels con el formato de la pelicula y el precio establecido
		para una funcion"""
		self.numSalaSeleccionada = self.__getNumSala()
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT precio_entrada FROM ps.entradayprecio WHERE numero_Sala = %s",(self.numSalaSeleccionada,))
			precio = sentencia.fetchone()
			self.labelPrecio['text'] = "precioSala: {}".format(precio[0])
			sentencia.execute("SELECT DISTINCT tipo_sala from ps.sala WHERE numero_sala = %s",(self.numSalaSeleccionada,))
			self.formatoSalaSeleccionada = sentencia.fetchone()
			self.labelformato['text'] = "formato: {}".format(self.formatoSalaSeleccionada[0])

			#obtener el precio seleccionado para la funcion
			self.precioEntrada = precio[0]

	def getClaveFuncion(self):
		"""metodo que permite pasar el id_funcion a la la ventana que permite seleccionar los asientos"""
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT id_funcion from ps.funcion WHERE hora_inicio = %s AND id_pelicula = %s\
								AND fecha = %s AND numero_sala = %s AND nombre_cine = %s AND formato = %s",(self.horaSeleccionada,
								self.idPelicula,self.fechaSeleccionada,self.numSalaSeleccionada,self.nombreCine,
								self.formatoSalaSeleccionada,))
			claveFuncion = sentencia.fetchone()
			return claveFuncion[0]

	def getPrecioEntrada(self):
		return self.precioEntrada


	def activarWidgets(self,event):
		"""se van activando los widgets siguientes de acuerdo al 
		item seleccionado en el widget actual"""
		if not self.isClicked:
			self.isClicked = True
		if self.isClicked:
			self.listaPelicula["values"] = self.obtenerPelicula()
			self.nombrePelicula = self.listaPelicula.get() #obtener nombrePelicula
			self.listaPelicula.config(state='readonly')
		if self.listaPelicula.get() != "":
			self.listaFunciones.config(state='readonly')
			self.listaFunciones["values"] = self.obtenerFechaFuncion()
			if self.listaFunciones.get() != "":
				self.setearInfoPelicula()
				self.fechaSeleccionada = self.listaFunciones.get()
				self.listaHorarios["values"] = self.obtenerHorarioFuncion()
				self.listaHorarios.config(state='readonly')
				if self.listaHorarios.get() != "":
					self.horaSeleccionada = self.listaHorarios.get()
					self.setearValores()
					self.botonContinuar.config(state='active')

	def cerrarFrame(self):
		"""Cierra el frame actual y cierra la aplicacion por completo"""
		self.destroy()
		self.mainWindow.root.destroy()

	def volverAtras(self):
		"""destruye el frame actual y muestra el frame de seleccion 
		de region , ciudad y cine"""
		self.destroy()
		self.mainWindow.show()

#clase que muestra un frame para comprar combos seleccionados
class FrameVentaComida(Toplevel):
	def __init__(self,frameVentas):
		self.frameVentas = frameVentas
		self.nombreCine = self.frameVentas.mainWindow.getNombreCine()
		self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"
		Toplevel.__init__(self)
		self.geometry("400x440") #original 320x420
		self.resizable(False,False)

		self.fotosComida = []
		for i in range(1,6):
			self.fotosComida.append(PhotoImage(file="combo{}.png".format(i)))

		#obtener los valores de los precios desde la BD
		self.listaPrecios = self.obtenerPrecios()

		frame = Frame(self)
		frame.place(x=0,y=0,width=700,height=400)

		#variables para los checkButton y Comboboxes
		self.checkCombos = [IntVar() for x in range(5)]
		self.Comboboxes = []


		"""Almacema el item y la cantidad asociada a ese item"""
		self.combosSeleccionados = {}

		self.labelInfo = Label(frame,text="carrito")
		self.labelInfo.place(x=30,y=340,width=350,height=30)

		#posicionar los botones de check y los Comboboxes
		posY = 30
		for i in range(5):
			check = Checkbutton(frame,text="OK",variable=self.checkCombos[i],onvalue=1,offvalue=0,command= lambda i=i: self.verificarProductos(i))
			check.place(x=110,y=posY)
			cantidad = ttk.Combobox(frame)
			self.Comboboxes.append(cantidad)
			self.Comboboxes[i].place(x=30,y=posY,width=50,height=30)
			self.Comboboxes[i].config(state="readonly")
			self.Comboboxes[i]["values"] = [1,2,3,4,5]
			posY += 60


		self.cuadro1 = Label(frame,image=self.fotosComida[0])
		self.cuadro1.place(x=190,y=30,width=50,height=50)
		self.labelPrecio1 = Label(frame,text="${}".format(self.listaPrecios[0][0]))
		self.labelPrecio1.place(x=250,y=30,width=50,height=20)

		self.cuadro2 = Label(frame,image=self.fotosComida[1])
		self.cuadro2.place(x=190,y=90,width=50,height=50)
		self.labelPrecio2 = Label(frame,text="${}".format(self.listaPrecios[1][0]))
		self.labelPrecio2.place(x=250,y=90,width=50,height=20)

		self.cuadro3 = Label(frame,image=self.fotosComida[2])
		self.cuadro3.place(x=190,y=150,width=50,height=50)
		self.labelPrecio3 = Label(frame,text="${}".format(self.listaPrecios[2][0]))
		self.labelPrecio3.place(x=250,y=150,width=50,height=20)

		self.cuadro4 = Label(frame,image=self.fotosComida[3])
		self.cuadro4.place(x=190,y=210,width=50,height=50)
		self.labelPrecio1 = Label(frame,text="${}".format(self.listaPrecios[3][0]))
		self.labelPrecio1.place(x=250,y=210,width=50,height=20)

		self.cuadro5 = Label(frame,image=self.fotosComida[4])
		self.cuadro5.place(x=190,y=270,width=50,height=50)
		self.labelPrecio1 = Label(frame,text="${}".format(self.listaPrecios[4][0]))
		self.labelPrecio1.place(x=250,y=270,width=50,height=20)

		self.botonComprar = Button(self,text="Comprar",command=self.ejecutarCompra)
		self.botonComprar.config(bg="red",fg="white")
		self.botonComprar.place(x=160,y=380,width=80,height=50) #original y=360


	def verificarProductos(self,indice):
		""" Verifica los combos seleccionados y la cantidad escogida de el mismo
		y se agrega a un diccionario item -> cantidad o si desmarca un combo
		este se elimina del diccionario """
		if self.checkCombos[indice].get() == 1 and self.Comboboxes[indice].get() != "":
			self.labelInfo['text'] = "ha seleccionado {} unidades del item {}".format(self.Comboboxes[indice].get(),indice+1)
			self.combosSeleccionados[indice+1] = self.Comboboxes[indice].get()
		if self.checkCombos[indice].get() == 0 and self.Comboboxes[indice].get() != "":
			self.labelInfo['text'] = "ha descartado el item {}".format(indice+1)
			del self.combosSeleccionados[indice+1]

	"""
	se debe abrir un frame que contenga la boleta de comprar y añadir la venta a
	la base de datos
	"""
	def ejecutarCompra(self):
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			fecha = date.today()
			hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			self.totalVenta = 0

			#obtener el monto total de todos los items
			for item,cantidad in self.combosSeleccionados.items():
				sentencia.execute("SELECT precio_combo FROM ps.preciocomida WHERE numero_combo = %s",(item,))
				precio = sentencia.fetchone()
				precio = precio[0]
				self.totalVenta += (precio*int(cantidad))

			#insertar en venta
			sentencia.execute("INSERT INTO ps.venta (hora_venta,fecha_venta,monto_venta,nombre_cine) VALUES \
								(%s,%s,%s,%s)",(hora,fecha,self.totalVenta,self.nombreCine,))
			#obtener su id
			sentencia.execute("SELECT codigo_venta FROM ps.venta WHERE hora_venta = %s AND fecha_venta = %s\
							AND monto_venta = %s AND nombre_cine = %s",(hora,fecha,self.totalVenta,self.nombreCine,))
			codigo = sentencia.fetchone()
			codigo = codigo[0]

			#insertar en venta_comida todos los combos comprados
			for combo in self.combosSeleccionados:
				sentencia.execute("INSERT INTO ps.venta_comida (codigo_venta,numero_combo,nombre_cine) VALUES\
									(%s,%s,%s)",(codigo,combo,self.nombreCine,))

			boleta = FrameBoleta(self)

	@ejecutarSentenciaSQL("SELECT precio_combo FROM ps.preciocomida ORDER BY precio_combo")
	def obtenerPrecios(self):
		pass

	"""metodos para obtener datos en la boleta"""
	def getTotalCompra(self):
		return self.totalVenta

	def getCombosComprados(self):
		combos = set()
		for item,cantidad in self.combosSeleccionados.items():
			combos.add(item)
		return combos


#clase que muestra un label con la info de la compra
class FrameBoleta(Toplevel):
	
	"""
	basicamente un frame que contiene un label con la info de la compra tanto
	de peliculas como de combos de comida
	"""
	def __init__(self,clasePadre):
		self.root = clasePadre
		Toplevel.__init__(self)
		self.geometry("400x400")
		self.resizable(False,False)
		self.title("Boleta de Compra")

		if self.root.__class__.__name__ == 'FrameVentaComida':
			self.__mostrarBoletaComida()
		elif self.root.__class__.__name__ == 'SalaCine':
			self.__mostrarBoletaEntradas()

	def __mostrarBoletaComida(self):
		precio = Label(self,text="Monto Total: ${} ".format(self.root.getTotalCompra())).pack()
		combos = Label(self,text="Combos Comprados: {}".format(self.root.getCombosComprados())).pack()
		botonAceptar = Button(self,text="Aceptar",command=self.__cerrarApp)
		botonAceptar.pack()


	def __mostrarBoletaEntradas(self):
		nombre = Label(self,text="Pelicula: {}".format(self.root.getNombrePelicula())).pack()
		sala = Label(self,text="Sala: {}".format(self.root.getNumeroSala())).pack()
		asientos = Label(self,text="asientos: {}".format(self.root.getAsientosComprados())).pack()
		fecha,hora = self.root.get_fecha_hora_Funcion()
		fechaHora = Label(self,text="fecha: {} --- hora: {}".format(fecha,hora)).pack()
		total = Label(self,text="Total: ${} pesos".format(self.root.getMontoTotal())).pack()
		botonAceptar = Button(self,text="Aceptar",command=self.__cerrarApp)
		botonAceptar.pack()

	def __cerrarApp(self):
		self.destroy()
		self.root.destroy()

#clase que muestra las salas de cines y sus asientos
class SalaCine(Toplevel):
	def __init__(self,frameVentas,idFuncionSeleccionada):
		self.frameVentas = frameVentas
		self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"
		Toplevel.__init__(self)
		self.geometry("1100x500")
		self.title("Asientos")
		self.resizable(False,False)

		self.nombreCine = self.frameVentas.mainWindow.getNombreCine()

		frame = Frame(self,width=700,height=400)
		frame.pack()

		pantalla = Frame(frame,width=500,height=30)
		pantalla.config(bg="black")
		pantalla.grid(row=0,column=0,pady=20,columnspan=24)

		tituloPantalla = Label(pantalla,text="Pantalla",anchor="center")
		tituloPantalla.config(bg="black",fg="white")
		tituloPantalla.place(x=200,y=0,width=100,height=30)

		self.botonComprar = Button(self,text="Comprar",command=self.comprarAsientos) 
		self.botonComprar.config(bg="red",fg="white")
		self.botonComprar.pack()

		self.idFuncionSeleccionada = idFuncionSeleccionada
		self.numSala = self.__getNumSala()
		self.letras = self.getFilas()

		self.filas = len(self.letras)
		self.columnas = self.getColumnas()

		#matriz con la referencia a cada Checkbox
		self.matriz = [[IntVar() for x in range(self.columnas)] for y in range(self.filas)]

		#conjuntos con asietos a bloquear de la ventana
		self.asientosReservados = self.__obtenerAsientosReservados()

		#visualizar asientos
		for i in range(self.filas):
			for j in range(1,self.columnas):
				numAsiento = "{}-{}".format(self.letras[i],j) #numero del asiento a comparar
				check = Checkbutton(frame,text="{}-{}".format(self.letras[i],j),variable=self.matriz[i][j],onvalue=1,offvalue=0,command=lambda i=i,j=j:self.verificarCheckbox(i,j))
				if numAsiento in self.asientosReservados:
					check.config(state='disabled')
				check.grid(row=i+1,column=j+1)

		#conjunto con asientos que el usuario marca
		self.asientosSeleccionados = set()


	def __getNumSala(self):
		"""metodo privado que retorna el numero de la sala en la funcion correspondiente"""
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT numero_sala FROM ps.funcion WHERE id_funcion = %s",(self.idFuncionSeleccionada,))
			numSala = sentencia.fetchone()
		return numSala[0]

	def __obtenerAsientosReservados(self):
		"""consultar los asientos reservados asociados a una funcion y retornar un conjunto
		con los asientos que no estan disponibles para su compra"""
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT num_asiento FROM ps.entradayasiento WHERE id_funcion = %s",(self.idFuncionSeleccionada,))
			asientosReservados = sentencia.fetchall()
		listaReservados = []
		for i in range(len(asientosReservados)):
			listaReservados.append(asientosReservados[i][0])
		return set(listaReservados)

	def verificarCheckbox(self,fila,columna):
		"""
		Al seleccionar un asiento este se guarda en un set y al desmarcarlo
		este se remueve del set
		"""
		asiento = "{}-{}".format(self.letras[fila],columna)
		if self.matriz[fila][columna].get() == 1:
			self.asientosSeleccionados.add(asiento)
		if self.matriz[fila][columna].get() == 0:
			self.asientosSeleccionados.discard(asiento)

	def comprarAsientos(self):
		self.precioEntrada = self.frameVentas.getPrecioEntrada()
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			#todos los asientos reservados los ingresa en entradayasiento
			for asiento in self.asientosSeleccionados:
				sentencia.execute("INSERT INTO ps.entradayasiento (num_asiento,id_funcion,num_sala) VALUES(%s,%s,%s)",
								(asiento,self.idFuncionSeleccionada,self.numSala,))
			#ingresar datos en la tabla venta
			hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			fecha = date.today()
			self.totalVenta = len(self.asientosSeleccionados)*self.precioEntrada
			sentencia.execute("INSERT INTO ps.venta (hora_venta,fecha_venta,monto_venta,nombre_cine)\
							VALUES (%s,%s,%s,%s)",(hora,fecha,self.totalVenta,self.nombreCine,))

			#obtener codigo de la venta para poder ingresar en venta entrada
			sentencia.execute("SELECT codigo_venta FROM ps.venta WHERE hora_venta = %s AND fecha_venta = %s\
								AND monto_venta = %s AND nombre_cine = %s",(hora,fecha,self.totalVenta,self.nombreCine,))
			self.codigoVenta = sentencia.fetchone()
			self.codigoVenta = self.codigoVenta[0]

			#insertar datos en tabla entrada
			sentencia.execute("INSERT INTO ps.entrada (numero_sala,id_funcion) VALUES (%s,%s)",(self.numSala,self.idFuncionSeleccionada,))

			#obtener el codigo_boleta de las entradas para la funcion solicitada
			sentencia.execute("SELECT MAX(codigo_boleta) FROM ps.entrada WHERE id_funcion = %s",(self.idFuncionSeleccionada,))
			self.codigoBoleta = sentencia.fetchone()
			self.codigoBoleta = self.codigoBoleta[0]

			sentencia.execute("INSERT INTO ps.venta_entrada (codigo_venta,codigo_boleta) VALUES (%s,%s)",
							(self.codigoVenta,self.codigoBoleta,))

			boleta = FrameBoleta(self)

	""" metodos para generar la info de la boleta """
	def getAsientosComprados(self):
		return self.asientosSeleccionados
	
	def getMontoTotal(self):
		return self.totalVenta

	def getNumeroSala(self):
		sala = self.__getNumSala()
		return sala

	def get_fecha_hora_Funcion(self):
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT fecha,hora_inicio FROM ps.funcion WHERE id_funcion = %s",(self.idFuncionSeleccionada,))
			fechayHora = sentencia.fetchone()
		fecha,hora = fechayHora
		return fecha,hora

	def getNombrePelicula(self):
		with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
			sentencia.execute("SELECT p.nombre_pelicula FROM ps.funcion AS f,ps.pelicula AS p WHERE \
								p.id_pelicula = f.id_pelicula AND f.id_funcion = %s",(self.idFuncionSeleccionada,))
			nombre = sentencia.fetchone()
			return nombre[0]

	def getColumnas(self):
		"""
		retorna una lista de letras segun el numero de la sala
		"""
		if self.numSala <= 4:
			columnas = 16
		elif self.numSala > 4 and self.numSala <= 6:
			columnas = 15
		elif self.numSala > 6 and self.numSala <= 8:
			columnas = 12
		else:
			columnas = 18
		return columnas

	def getFilas(self):
		"""
		retorna el numero de columnas segun el numero de la sala
		"""
		letras = []
		if self.numSala <= 4:
			for letra in range(0,13): #[A-M]
				letras.append(string.ascii_uppercase[letra])
		elif self.numSala > 4 and self.numSala <= 6:
			for letra in range(0,10): #[A-J]
				letras.append(string.ascii_uppercase[letra])
		elif self.numSala > 6 and self.numSala <= 8:
			for letra in range(0,8): #[A-H]
				letras.append(string.ascii_uppercase[letra])
		else:
			for letra in range(0,16): #[A-P]
				letras.append(string.ascii_uppercase[letra])
		return letras

#-------------------------------------- funcion main ----------------------------------------------------------
if __name__ == '__main__':
	parent = Tk()
	app = VentanaPrincipal(parent)
	parent.mainloop()	