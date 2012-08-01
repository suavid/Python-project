#!/bin/python

import pygtk
pygtk.require("2.0")
import gtk

class ventana:
	def delete(self, widget, data = None):
		return False
	def close(self, widget, data = None):
		gtk.main_quit()
	def main(self):
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
		self.playIcon = gtk.Image()
		self.stopIcon = gtk.Image()
		self.nextIcon = gtk.Image()
		self.prevIcon = gtk.Image()
		self.pauseIcon = gtk.Image()
		self.plB = gtk.HBox(True,0)
		self.stB = gtk.HBox(True,0)
		self.neB = gtk.HBox(True,0)
		self.prB = gtk.HBox(True,0)
		self.paB = gtk.HBox(True,0)
		self.plT = gtk.Label("Reproducir")
		self.stT = gtk.Label("Detener")
		self.neT = gtk.Label("Siguiente")
		self.prT = gtk.Label("Anterior")
		self.paT = gtk.Label("Pausar")
		self.playIcon.set_from_file("play.png")
		self.stopIcon.set_from_file("stop.png")
		self.nextIcon.set_from_file("next.png")
		self.prevIcon.set_from_file("prev.png")
		self.pauseIcon.set_from_file("pause.png")
		self.plB.pack_start(self.plT)
		self.plB.pack_start(self.playIcon)
		self.stB.pack_start(self.stT)
		self.stB.pack_start(self.stopIcon)
		self.neB.pack_start(self.neT)
		self.neB.pack_start(self.nextIcon)
		self.prB.pack_start(self.prT)
		self.prB.pack_start(self.prevIcon)
		self.paB.pack_start(self.paT)
		self.paB.pack_start(self.pauseIcon)
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
		self.plT.show()
		self.stT.show()
		self.neT.show()
		self.prT.show()
		self.paT.show()
		self.playIcon.show()
		self.stopIcon.show()
		self.nextIcon.show()
		self.prevIcon.show()
		self.pauseIcon.show()
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
