#!/usr/bin/python
# Modulos importables
# gtk: permite integracion con el entorno
# path: modulo propio con rutas y mensajes personalizados
# os: permite comunicar con el os
import gtk,path,os
from xml.dom.minidom import Document
from xml.dom import minidom
import gst
# Describe los tipos de archivos permitidos con una tupla
filepattern = (
         ("MP3","*.mp3"),
        ) 
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
		self.sel = builder.get_object("selec")
		self.tree = builder.get_object("arbol_pistas")
		self.ar = builder.get_object("Archivos")
		self.te = builder.get_object("Textos")
		try:
			dom = minidom.parse("playlist/track.xml")
			for i in range(0,len(dom.getElementsByTagName("track"))):
				self.medialist.append([dom.getElementsByTagName("track")[i].firstChild.data,dom.getElementsByTagName("ruta")[i].firstChild.data])
		except:
			pass
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
		"on_salir_activate":self.destroy
		}
		
		self.player = gst.element_factory_make("playbin2", "player")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		
	  # Conecta 
		builder.connect_signals(dict)
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
		# Se procesa la respuesta de la ventana, -5 abrir -6 cancelar
		xmldocument = open("playlist/track.xml","w")
		# Crea el documento minidom 
		doc = Document()
		# Crea el elemento base <wml> 
		wml = doc.createElement("wml")
		#lo agrega al documento
		doc.appendChild(wml)
		if respt == -5:        
			fileselected = self.agregar_ventana.get_filenames()
			for files in fileselected:
				(dirs,files)= os.path.split(files)
				self.medialist.append([files,dirs])
				# Crea elemento pista <pista> 
				maincard = doc.createElement("pista")
				wml.appendChild(maincard)
				nm = doc.createElement("track")
				maincard.appendChild(nm)
				nombre = doc.createTextNode(files)
				nm.appendChild(nombre)
				dr = doc.createElement("ruta")
				maincard.appendChild(dr)
				path = doc.createTextNode(dirs)
				dr.appendChild(path)
		xmldocument.write(doc.toprettyxml(indent="  "))
		xmldocument.close()	
		
	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
	
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
		
	def on_tree_selection_changed(self,selection):
		model, treeiter = selection.get_selected()
		if treeiter != None:
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
			return palabra 	
				
	def about(self,widget):
		self.help.show()
	def close(self,widget):
		self.help.hide()
	# Funcion que cierra la ventana
	def destroy(self,widget):
		gtk.main_quit()
		
	# Funciones para los botones, posteriormente seran definidas
	def play(self,widget):
		self.stop(widget)
		self.rep = 1
		select = self.tree.get_selection()
		filepath = self.on_tree_selection_changed(select)
		self.player.set_property("uri", "file://"+filepath)
		self.player.set_state(gst.STATE_PLAYING)
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
		if self.rep == 1:
			self.player.set_state(gst.STATE_NULL)
			self.rep = 0
		else:
			pass		
         
#Ejecucion del programa
if __name__ == "__main__":
    main()
    gtk.main()


