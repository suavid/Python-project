import random

PATH = "glmplayer.glade"


# funcion para invertir una cadena de caracteres
def reverse(list):
	if len(list)==1:
		return list
	else:
		return list[-1]+reverse(list[:-1])  
# Fin de funcion para invertir una cadena



# Funcion que se registra al cambio en la medialist por ende en el gtk.TreeWiev
def on_tree_selection_changed(selection):
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

def ObtenerLista(Limite,init):
	numeros = []
	numeros.append(init)
	while len(numeros) < (Limite-1):
		numero = random.randint(0, Limite)
		if not numero in numeros:
			numeros.append(numero)
	return numeros

def clearing(array):
	palabra = ""
	contador = 0
	for letra in array:
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
