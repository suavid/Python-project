#!/usr/bin/python

import gtk

class main:

	def __init__(self):
    # Crea la ventana de trabajo Principal y obtiene los objetos en Glade
		builder = gtk.Builder()
		builder.add_from_file("interface/glmplayer.glade") 
		self.agregar_ventana = builder.get_object("Add")
    # Diccionario de eventos y Conexion de los mismos.
		dict = {"on_agregar_activate": self.abrir_archivos,
		"gtk_main_quit":self.destroy
		}
		builder.connect_signals(dict)
		
	def abrir_archivos(self,widget):
		self.agregar_ventana.run()
		self.agregar_ventana.hide()
	def destroy(self,widget):
		gtk.main_quit()
         
#Ejecucion del programa
if __name__ == "__main__":
    main()
    gtk.main()

