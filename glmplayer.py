#!/usr/bin/python
# Modulos importables
# gtk: permite integracion con el entorno
# path: modulo propio con rutas y mensajes personalizados
# os: permite comunicar con el os
# xml.dom.minidom para manejo de documentos xml
import gtk,path,os
import MySQLdb
import gst,subprocess
import eyeD3
from mutagen.mp3 import MP3
# Describe los tipos de archivos permitidos con una tupla
filepattern = (
         ("MP3","*.mp3"),
        ) 

db=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='pistas')
cursor=db.cursor()
sql='SELECT * FROM data;'
cursor.execute(sql)
resultado=cursor.fetchall()
# funcion para revertir una cadena de caracteres
def reverse(list):
	if len(list)==1:
		return list
	else:
		return list[-1]+reverse(list[:-1])             
# Clase principal
class main:
	# Definicion de la funcion __init__ que construye la clase
	def __init__(self):
    # Crea la ventana de trabajo Principal y obtiene los objetos en Glade
		builder = gtk.Builder()
		builder.add_from_file(path.PATH) 
	 # Fin de la conexion con glade para la ventana principal
	 # Crea la ventana para importar musica, nombrada Add	
		self.agregar_ventana = builder.get_object("Add")
		self.help = builder.get_object("About")
	 # Crea un filtro para aplicarlo a la seleccion de archivos
		self.filtro = gtk.FileFilter()
		self.rep = 0 
	 # Obtiene el objeto gtkliststore de glade y lo conecta	
		self.medialist = builder.get_object("media")
	 # Obtiene el manejador de selecciones
		self.sel = builder.get_object("selec")
	 # Estos objetos que siguen aun no se han utilizado en el codigo del programa
	 # Obtiene el gtk.TreeWiev
		self.tree = builder.get_object("arbol_pistas")
	 # Obtiene el objeto Archivos que contiene el texto
		self.info = builder.get_object("info")
		self.info.set_text("No se ha reproducido nada aun")
	# Lee las pistas del documento XML	
    # Diccionario de eventos y Conexion de los mismos.
		dict = {"on_agregar_activate": self.abrir_archivos,
		"gtk_main_quit":self.destroy,
		"on_play_clicked":self.play,
		"on_pause_clicked":self.pause,
		"on_prev_clicked":self.prev,
		"on_next_clicked":self.next,
		"on_stop_clicked":self.stop,
		"on_ayud_activate":self.about,
		"on_About_destroy":self.close,
		"on_salir_activate":self.destroy,
		"on_volumen_value_changed":self.cb_master_slider_change
		}
		
		# Conecta 
		builder.connect_signals(dict)
		
		# Generacion del elemento controlador de la reproducccion
		self.player = gst.element_factory_make("playbin2", "player")
		# Obtiene el Bus
		bus = self.player.get_bus()
		# Agrega un vigilador de senales
		bus.add_signal_watch()
		# Habilita la emision de senales, esto ayuda con el control de Errores
		bus.enable_sync_message_emission()
		# Conecta las respectivas funciones de muestra de mensajes 
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		

		if len(resultado) > 0:
			for registro in resultado:
				self.medialist.append([registro[0],registro[1]])
		else:
			self.medialist.append(['No se ha importado nada Todavia','...'])




	def cb_master_slider_change(self, widget,event,data=None):
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
			proc.wait()
		except:
			pass	
	# Definicion de la funcion para agregar archivos de sonido
	def abrir_archivos(self,widget):
		# Tipos de archivos agregables
		pattern = (".mp3") 
		# Nombre para el filtro, es el que aparece en la ventana	
		self.filtro.set_name("*.mp3")
		# para cada nombre y tipo en la tupla de filtros
		for name, pattern in filepattern:
			# Agrega el filtro, en nuestro caso, por el momento solo *.mp3
 			self.filtro.add_pattern(pattern)         
 		# Agrega el filtro a la ventana de seleccion de archivos	
		self.agregar_ventana.add_filter(self.filtro)
		# Corre la ventana y guarda la respuesta
		respt=self.agregar_ventana.run()
		# Siempre debemos remover el filtro
		self.agregar_ventana.remove_filter(self.filtro)
		# Termina ejecucion y se esconde la ventana
		self.agregar_ventana.hide()
		if respt == -5:
			fileselected = self.agregar_ventana.get_filenames()
			for files in fileselected:
				(dirs,files)= os.path.split(files)
				sql = """INSERT INTO `data`(`nombre`, `ruta`) \
                VALUES ('%s', '%s');""" % (files,dirs)
				if cursor.execute(sql):
					self.medialist.append([files,dirs])

			
	# Funcion que emite los mensajes, asignada anteriomente 
	def on_message(self, bus, message):
		# Los parametros son pasados por el controlador del Bus
		t = message.type 
		# Obtiene el mensaje y lo procesa
		if t == gst.MESSAGE_EOS: 
			# Detiene la reproduccion
			self.player.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ERROR:
			# Por el momento muestra el error en consola, debe mostralo en ventana
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			
	# Esta funcion es recomendable que se mantenga de esta manera 
	# He obtenido esta definicion bien estructurada de la documentacion de gstreamer
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			gtk.gdk.threads_enter()
			imagesink.set_xwindow_id(self.movie_window.window.xid)
			gtk.gdk.threads_leave()
				
	# Funcion que se registra al cambio en la medialist por ende en el gtk.TreeWiev
	def on_tree_selection_changed(self,selection):
		# Obtiene un Iterador
		model, treeiter = selection.get_selected()
		# Si treeiter es igual a None no hay elementos en la lista
		if treeiter != None:
		# Todo esto que ven aqui es pura carpinteria, tuve que tratar la cadena 
		# obtenida del mendialist porque venia con espacios raros y tuve que eliminarlos
			palabra = "" 
			contador = 0
			for letra in model[treeiter][1]:
				if letra != "\n":
					if letra == " " and contador == 0:
						pass
					else:	
						palabra = palabra+letra
						contador = contador+1
			contador = 0
			palabra = reverse(palabra)
			nueva = ""
			for letra in palabra:
				if letra != "\n":
					if letra == " " and contador == 0:
						pass
					else:	
						nueva = nueva+letra
						contador = contador+1
			palabra = reverse(nueva)+"/"
			contador = 0			
			for letra in model[treeiter][0]:
				if letra != "\n":
					if letra == " " and contador == 0:
							pass
					else:	
						palabra = palabra+letra
						contador = contador+1
			contador = 0
			palabra = reverse(palabra)
			nueva = ""
			for letra in palabra:
				if letra != "\n":
					if letra == " " and contador == 0:
						pass
					else:	
						nueva = nueva+letra
						contador = contador+1			 
			palabra = reverse(nueva)
			# Regresa la nueva palabra sin espacios raros, ahora la ruta ya es 100 por ciento valida
			return palabra 	
	# Muestra el mensaje de about 
	def about(self,widget):
		self.help.show()
	# Cierra el mensjae de about
	def close(self,widget):
		self.help.hide()
	# Funcion que cierra la ventana
	def destroy(self,widget):
		gtk.main_quit()
		
	# Funciones para los botones, posteriormente seran definidas
	def play(self,widget):
		try:	
			self.stop(widget)
			self.rep = 1
			select = self.tree.get_selection()
			# Llama a la funcion que trata la ruta
			filepath = self.on_tree_selection_changed(select)
			tag = eyeD3.Tag()
			audio = MP3(filepath)
			try:
				duration = audio.info.length
			except:
				pass
			tag.link(filepath)
			try:
				self.info.set_text(" Now Playing... "+tag.getArtist()+" - "+tag.getAlbum()+" - "+tag.getTitle()+"  ")
				# Envia la ruta al objeto de gstreamer 
				self.player.set_property("uri", "file://"+filepath)
				# Reproduce
				self.player.set_state(gst.STATE_PLAYING)
			except:
				pass
		except:
			pass
		
	def pause(self,widget):
		# funcion de pausa
		pass
		
	def prev(self,widget):
		# funcion de anterior
		pass
		
	def next(self,widget):
		# funcion de siguiente
		pass
		
	def stop(self,widget):
		# funcion de alto
		try:
			if self.rep == 1:
				self.player.set_state(gst.STATE_NULL)
				self.rep = 0
				self.info.set_text(" Se ha detenido la reproduccion")
			else:
				pass
		except:
			pass		
         
#Ejecucion del programa
if __name__ == "__main__":
    main()
    gtk.main()


