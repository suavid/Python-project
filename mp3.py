#!/bin/python

# agregando librerias necesarias para la generacion de ventanas
# evitar ejecucion de versiones anteriores
import pygtk,gtk
pygtk.require("2.0")
import os,glob,tree,ext

# clase principal
class ventana:

        def file_ok_sel(self, w,campo):
                self.directorio = campo.get_filename()
		print self.directorio
                
        def importar(self,widget, data = None):
		dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_select_multiple(True)
		filter = gtk.FileFilter()
		config = open("mp.config","a")
		filter.set_name("*.mp3")
		filter.add_mime_type("video/mpeg")
		filter.add_mime_type("video/x-mpeg")
		filter.add_mime_type("image/gif")
		filter.add_pattern("*.mp3")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
    			for files in dialog.get_filenames():
				config.write(files+"\n")
		elif response == gtk.RESPONSE_CANCEL:
    			print 'Closed, no files selected'
		config.close()
		dialog.destroy()

        
	# evento de borrado
	def delete(self, widget, data = None):
		return False

	# detiene manejadores de enventos, termina ejecucion de la ventana
	def close(self,widget,data = None):
		gtk.main_quit()

	def main(self):
	# inicia manejadores de eventos 
		gtk.main()

	def __init__(self):

		# Ventana gestionada por el manejador de ventana del sistema
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event",self.delete)
		self.window.connect("destroy",self.close)
		self.window.set_title("Reproductor Mp3")
		self.window.set_border_width(0)
                
		# Creacion de las tablas y frames
		self.btn_nav = gtk.Table(9,1,True)
		self.controles = gtk.Table(3,1,True)
		self.vol_box_icon = gtk.Table(1,1,False)
		self.main_frame = gtk.VBox(False, 0)
		self.div_2 = gtk.HBox(False, 0)
		self.configure = open("mp.config","r")
                self.directorio = self.configure.readlines()
                
		#Entrada de texto para busqueda
		self.campo_busq = gtk.Entry(0)
		self.campo_busq.set_text("Busqueda...")

		# Menu
		# Creacion de los submenus
		self.submenu_1 = gtk.Menu()
		self.submenu_2 = gtk.Menu()
		self.submenu_3 = gtk.Menu()
		# Creacion de los Items de cada Submenu
		# Para submenu_1
  		self.item1_1 = gtk.MenuItem("Abrir")
  		self.item1_2 = gtk.MenuItem("Actualizar")
  		self.item1_3 = gtk.MenuItem("Importar")
		# Para submenu_2
		self.item2_1 = gtk.MenuItem("Preferencias")
		# Para submenu_3
		self.item3_1 = gtk.MenuItem("Help F2")
		# Mostrando Items
		ext.show(self.item1_1,self.item1_2,self.item1_3,self.item2_1,self.item3_1)
		# Agregando items a respectivos submenus
 		self.submenu_1.append(self.item1_1)
  		self.submenu_1.append(self.item1_2)
  		self.submenu_1.append(self.item1_3)
		self.submenu_2.append(self.item2_1)
		self.submenu_3.append(self.item3_1)
		# Creando Items del menu principal
		# Corresponde submenu1
		self.archivo = gtk.MenuItem("Archivo")
		# Corresponde submenu2
		self.editar = gtk.MenuItem("Editar")
		# Corresponde submenu3
		self.ayuda = gtk.MenuItem("Ayuda")
		# Agregando submenus a menu principal
		self.archivo.set_submenu(self.submenu_1)
		self.editar.set_submenu(self.submenu_2)
		self.ayuda.set_submenu(self.submenu_3)
		# Mostrando submenus
		ext.show(self.archivo,self.editar,self.ayuda)
		# Eventos
		self.item1_3.connect_object("activate", self.importar,None)
		# Creando Barra de Menu
		self.menu_bar = gtk.MenuBar()
		self.menu_bar.show()
		# Agregando a Barra de Menu	
		self.menu_bar.append(self.archivo)
		self.menu_bar.append(self.editar)
		self.menu_bar.append(self.ayuda)

                # Seccion con barras de desplazamiento
		self.vent_list = tree.create_tree()
		tree.update_tree(self.directorio,self.vent_list)
		
		# Control de volumen 
		# Creacion del ajuste
		self.ajuste = gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
		# Creacion del control con el ajuste previamente creado
		self.control = gtk.HScale(self.ajuste)
		# Poniendo valores y politicas por defecto
		ext.scale_set_default_values(self.control)
		# Icono del control de volumen
                self.vIcon = gtk.Image()
                self.vIcon.set_from_file("icons/volumen.png") 
                
		# Botones para el reproductor
		# Creacion de cajas con iconos
		self.plB = ext.buttonBox2(self.window,"icons/play.png")
		self.stB = ext.buttonBox2(self.window,"icons/stop.png")
		self.neB = ext.buttonBox2(self.window,"icons/next.png")
		self.prB = ext.buttonBox2(self.window,"icons/prev.png")
		self.paB = ext.buttonBox2(self.window,"icons/pause.png")
		# Creacion de los botones
		self.play = gtk.Button()
		self.stop = gtk.Button()
		self.next = gtk.Button()
		self.prev = gtk.Button()
		self.pause = gtk.Button()
		# Agregando iconos a Botones
		self.play.add(self.plB)
		self.stop.add(self.stB)
		self.next.add(self.neB)
		self.prev.add(self.prB)
		self.pause.add(self.paB)

		# Pocisionando en tablas
		# Tablas para botones
		self.btn_nav.attach(self.play,0,1,0,1,gtk.FILL,gtk.FILL,0,0)
		self.btn_nav.attach(self.stop,1,2,0,1,gtk.FILL,gtk.FILL,0,0)
		self.btn_nav.attach(self.next,2,3,0,1,gtk.FILL,gtk.FILL,0,0)
		self.btn_nav.attach(self.prev,3,4,0,1,gtk.FILL,gtk.FILL,0,0)
		self.btn_nav.attach(self.pause,4,5,0,1,gtk.FILL,gtk.FILL,0,0)
		# Tabla para icono de volumen
		self.vol_box_icon.attach(self.vIcon,0,1,0,1,gtk.FILL,gtk.FILL,10,10)
		# Tabla para control de volumen y caja de busqueda
		self.controles.attach(self.control,1,2,0,1,gtk.FILL,gtk.FILL,0,0)
		self.controles.attach(self.campo_busq,0,1,0,1,gtk.FILL,gtk.FILL,10,10)

		# Empaquetados
		self.main_frame.pack_start(self.menu_bar,False,False,0)
		self.main_frame.pack_start(self.vent_list,False,False,0)
		self.main_frame.pack_start(self.div_2,False,False,0)
		self.div_2.pack_start(self.btn_nav,False,False,0)
		self.div_2.pack_start(self.controles,False,False,0)
		self.div_2.pack_start(self.vol_box_icon,False,False,0)
		self.window.add(self.main_frame)
		
		#Mostrando elementos
		ext.show(self.vent_list,self.vIcon,self.campo_busq,self.plB,self.stB,self.neB)
		ext.show(self.prB,self.paB,self.play,self.stop,self.next,self.prev)
		ext.show(self.pause,self.control,self.btn_nav,self.controles)
		ext.show(self.vol_box_icon,self.main_frame,self.div_2,self.window)

# programa principal
if __name__=="__main__":
	mainFrame = ventana()
	mainFrame.main()

