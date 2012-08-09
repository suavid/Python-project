import pygtk,gtk
pygtk.require("2.0")

# funcion para creacion de botones con etiqueta e imagen
def buttonBox(padre,icono,label_text):

	# Crear main_frame para icon y label
	box = gtk.HBox(True, 0)
	# Creamos la imagen
	imagen = gtk.Image()
	imagen.set_from_file(icono)
	# Creamos la etiqueta
	label = gtk.Label(label_text)
	# Empaquetamos icon y label en la main_frame
	box.pack_start(imagen, False, False, 3)
	box.pack_start(label, False, False, 3)
	image.show()
	label.show()
	return box;

# funcion para creacion de botones con imagen sin etiqueta
def buttonBox2(padre,icono):

	# Crear main_frame para icon
	box = gtk.HBox(True, 0)
	box.set_border_width(2)
	# Creamos la imagen
	image = gtk.Image()
	image.set_from_file(icono)
	# Empaquetamos icon en la main_frame
	box.pack_start(image, False, False, 3)
	image.show()
	return box;

def show(*lista):
	for item in lista:
		item.show() 

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
