#!/bin/python

# agregando librerias necesarias para la generacion de ventanas
# evitar ejecucion de versiones anteriores
import pygtk
pygtk.require("2.0")
import gtk


# funcion para creacion de botones con etiqueta e imagen
def buttonBox(parent,icon,label_text):

	# Crear caja para icon y label
	box = gtk.HBox(True, 0)
	# Creamos la imagen
	image = gtk.Image()
	image.set_from_file(icon)
	# Creamos la etiqueta
	label = gtk.Label(label_text)
	# Empaquetamos icon y label en la caja
	box.pack_start(image, False, False, 3)
	box.pack_start(label, False, False, 3)
	image.show()
	label.show()
	return box;

# funcion para creacion de botones con imagen sin etiqueta
def buttonBox2(parent,icon):

	# Crear caja para icon
	box = gtk.HBox(True, 0)
	box.set_border_width(2)
	# Creamos la imagen
	image = gtk.Image()
	image.set_from_file(icon)
	# Empaquetamos icon en la caja
	box.pack_start(image, False, False, 3)
	image.show()
	return box;

# funcion para poner la escala a valores iniciales
def scale_set_default_values(scale):

	# politica de actualizacion 
	scale.set_update_policy(gtk.UPDATE_CONTINUOUS)
	# digitos a mostrar en la escala
	scale.set_digits(1)
	# pocision pre definida
	scale.set_value_pos(gtk.POS_TOP)
	# dibujado
	scale.set_draw_value(True)

# clase principal
class ventana:

	# evento de borrado
	def delete(self, widget, data = None):
		return False

	# detiene manejadores de enventos, termina ejecucion de la ventana
	def close(self, widget, data = None):
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

		# Creacion de las tablas y cajas
		self.tabla = gtk.Table(10,1,True)
		self.caja = gtk.VBox(False, 0)
		self.caja2 = gtk.VBox(True, 0)

		#Entrada de texto para busqueda
		self.entry = gtk.Entry(0)
		self.entry.set_text("Busqueda...")

		# menu
		self.menu = gtk.Menu()
		self.menu2 = gtk.Menu()
		self.menu3 = gtk.Menu()
  		self.item1 = gtk.MenuItem("Abrir")
  		self.item2 = gtk.MenuItem("Actualizar")
  		self.item3 = gtk.MenuItem("Importar")
		self.item4 = gtk.MenuItem("Preferencias")
		self.item5 = gtk.MenuItem("Help F2")
		self.item1.show()
  		self.item2.show()
  		self.item3.show()
		self.item4.show()
		self.item5.show()
 		self.menu.append(self.item1)
  		self.menu.append(self.item2)
  		self.menu.append(self.item3)
		self.menu2.append(self.item4)
		self.menu3.append(self.item5)
		self.archivo = gtk.MenuItem("Archivo")
		self.editar = gtk.MenuItem("Editar")
		self.ayuda = gtk.MenuItem("Ayuda")
		self.archivo.set_submenu(self.menu)
		self.editar.set_submenu(self.menu2)
		self.ayuda.set_submenu(self.menu3)
		self.archivo.show()
		self.editar.show()
		self.ayuda.show()
		self.menu_bar = gtk.MenuBar()
		self.menu_bar.show()	
		self.menu_bar.append(self.archivo)
		self.menu_bar.append(self.editar)
		self.menu_bar.append(self.ayuda)


                        
                
		# Control de volumen 
		self.ajuste = gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
		self.control = gtk.HScale(self.ajuste)
		scale_set_default_values(self.control)
                self.vIcon = gtk.Image()
                self.vIcon.set_from_file("volumen.png") 
                
		# Botones para el reproductor
		self.plB = buttonBox2(self.window,"play.png")
		self.stB = buttonBox2(self.window,"stop.png")
		self.neB = buttonBox2(self.window,"next.png")
		self.prB = buttonBox2(self.window,"prev.png")
		self.paB = buttonBox2(self.window,"pause.png")
		self.play = gtk.Button()
		self.stop = gtk.Button()
		self.next = gtk.Button()
		self.prev = gtk.Button()
		self.pause = gtk.Button()
		self.play.add(self.plB)
		self.stop.add(self.stB)
		self.next.add(self.neB)
		self.prev.add(self.prB)
		self.pause.add(self.paB)
		# Pocisionando en tabla
		self.tabla.attach(self.play,0,1,0,1,gtk.FILL,gtk.FILL,0,0)
		self.tabla.attach(self.stop,1,2,0,1,gtk.FILL,gtk.FILL,0,0)
		self.tabla.attach(self.next,2,3,0,1,gtk.FILL,gtk.FILL,0,0)
		self.tabla.attach(self.prev,3,4,0,1,gtk.FILL,gtk.FILL,0,0)
		self.tabla.attach(self.pause,4,5,0,1,gtk.FILL,gtk.FILL,0,0)
		self.tabla.attach(self.vIcon,6,7,0,1,gtk.FILL,gtk.FILL,0,0)
		self.tabla.attach(self.control,7,8,0,1,gtk.FILL,gtk.FILL,0,0)

		# Empaquetados
		self.caja.pack_start(self.menu_bar,False,False,0)
		self.caja.pack_start(self.caja2,False,False,0)
		self.caja.pack_start(self.entry,False,False,0)
		self.caja2.pack_start(self.tabla,False,False,0)
		self.window.add(self.caja)

		# Mostrando los respectivos elementos
		self.vIcon.show()
		self.entry.show()
		self.plB.show()
		self.stB.show()
		self.neB.show()
		self.prB.show()
		self.paB.show()
		self.play.show()
		self.stop.show()
		self.next.show()
		self.prev.show()
		self.pause.show()
		self.control.show()
		self.tabla.show()
		self.caja.show()
		self.caja2.show()
		self.window.show()

# programa principal
if __name__=="__main__":
	mainFrame = ventana()
	mainFrame.main()

