#!/bin/python
# Agregando librerias necesarias para la generacion de ventanas
# Import the libs to generate windows managed by  the window manager
import pygtk
# Evitar ejecucion de versiones anteriores
# Stop previous version
pygtk.require("2.0")
import gtk

def button(parent,icon,label_text):
	# Crear caja para icon y label
	box = gtk.HBox(True, 0)
	box.set_border_width(2)
	# Creamos la imagen
	image = gtk.Image()
	image.set_from_file(icon)
	# Creamos la etiqueta
	label = gtk.Label(label_text)
	# Empaquetamos icon y label en la caja
	box.pack_start(image, gtk.FALSE, gtk.FALSE, 3)
	box.pack_start(label, gtk.FALSE, gtk.FALSE, 3)
	image.show()
	label.show()
	return box;

# Clase principal
# Main class
class ventana:
	# Evento de borrado
	# Delete event, True will stop destroy event, False will start destroy envet
	def delete(self, widget, data = None):
		return False
	# Stop main()
	# Detiene manejadores de enventos, termina ejecucion de la ventana
	def close(self, widget, data = None):
		gtk.main_quit()
	def main(self):
	# Inicia manejadores de eventos 
	# Start main()
		gtk.main()
	def __init__(self):
		# Ventana gestionada por el manejador de ventana del sistema
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		# Llamada al evento que borrado de ventana
		self.window.connect("delete_event",self.delete)
		# Llamada al evento destructor de la ventana
		self.window.connect("destroy",self.close)
		# Pone el titulo de la ventana
		self.window.set_title("Reproductor Mp3")
		# Valor del borde interno de la ventana
		self.window.set_border_width(10)
		# Creacion de la tabla que contiene los botones
		self.tabla = gtk.Table(1,5,True)
		# Control de volumen 
		self.ajuste = gtk.Adjustment(0,0,50,5,10,50)
		self.control = gtk.HScale(self.ajuste)
		# Creacion de la caja principal
		self.caja = gtk.HBox(True, 0)
		# Botones para el reproductor
		self.play = gtk.Button()
		self.stop = gtk.Button()
		self.next = gtk.Button()
		self.prev = gtk.Button()
		self.pause = gtk.Button()
		# Fin de la creacion de botones
		# Iconos para los botones
		self.plB = button(self.window,"play.png","Reproducir")
		self.stB = button(self.window,"stop.png","Parar")
		self.neB = button(self.window,"next.png","Siguiente")
		self.prB = button(self.window,"prev.png","Anterior")
		self.paB = button(self.window,"pause.png","Pausa")
		# Fin de la creacion de los iconos
		# Agregando iconos
		self.play.add(self.plB)
		self.stop.add(self.stB)
		self.next.add(self.neB)
		self.prev.add(self.prB)
		self.pause.add(self.paB)
		# Pocisionando en tabla
		self.tabla.attach(self.play,0,1,0,1)
		self.tabla.attach(self.stop,0,1,1,2)
		self.tabla.attach(self.next,0,1,2,3)
		self.tabla.attach(self.prev,0,1,3,4)
		self.tabla.attach(self.pause,0,1,4,5)
		# Empaquetando la tabla dentro de la caja
		self.caja.pack_start(self.tabla)
		self.caja.pack_start(self.control)
		# Agregando la caja a la ventana 
		self.window.add(self.caja)
		# Agregando un valor de espaciado a la tabla
		self.tabla.set_col_spacings(2)
		# Mostrando los respectivos elementos
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
		self.window.show()
# Ejecutando 
if __name__=="__main__":
	mainFrame = ventana()
	mainFrame.main()
