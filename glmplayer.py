#!/usr/bin/python

import tweepy
import gtk
import path
import os
from xml.dom.minidom import Document
from xml.dom import minidom
import random
import gst
import time
import subprocess
import threading
from threading import Thread
import eyeD3
import gobject
gobject.threads_init()
import mutagen
from mutagen import File
from mutagen.id3 import APIC
from mutagen.mp3 import MP3 
import webbrowser

filepattern = (
         ("MP3","*.mp3"),
        ) 
auth = tweepy.OAuthHandler('V6yc6n5Mp7L8SATCxzrbHg','SOvHZc2w0v8XCZrBbMriat3QJfuynkvOQRV2xvIF50')
# CLASE PRINCIPAL
class main:

##################################################################################
# CONSTRUCTOR
	def __init__(self):

		##########################################################################
   		# VENTANA PRINCIPAL
		builder = gtk.Builder()
		builder.add_from_file(path.PATH) 
	 	###########################################################################

	 	###########################################################################
	 	# VENTANAS SECUNDARIAS	
		self.agregar_ventana = builder.get_object("Add")
		self.help = builder.get_object("About")
		###########################################################################
		############################################################################
		# OBJETOS ACTIVOS EN LA VENTANA
		self.tree = builder.get_object("arbol_pistas")
		self.medialist = builder.get_object("media")
		self.sel = builder.get_object("selec")
		self.imagen = builder.get_object("caratula")
		self.info = builder.get_object("info")
		self.artista = builder.get_object("artista")
		self.album = builder.get_object("album")
		self.titulo = builder.get_object("titulo")
		self.duracion = builder.get_object("duracion")
		self.progressBar = builder.get_object("bar")
		self.usuario = builder.get_object("usuario")
		self.clave = builder.get_object("clave")
		self.usuario2 = builder.get_object("n_usuario")
		self.clave2 = builder.get_object("n_clave")
		self.clave2_2 = builder.get_object("n_clave_2")
		self.status = builder.get_object("status")
		self.msj = builder.get_object("msj")
		self.codigo = builder.get_object("codigo")
		self.user = builder.get_object("user")
		self.step1 = builder.get_object("step1")
		self.step2 = builder.get_object("step2")
		self.logged = builder.get_object("logged")
		self.tweet1 = builder.get_object("tweet1")
		self.tweet2 = builder.get_object("tweet2")
		self.tweet3 = builder.get_object("tweet3")
		self.tweet4 = builder.get_object("tweet4")
		self.tweet5 = builder.get_object("tweet5")
		self.tweet6 = builder.get_object("tweet6")
		self.h1 = builder.get_object("h1")
		self.h2 = builder.get_object("h2")
		self.h3 = builder.get_object("h3")
		self.h4 = builder.get_object("h4")
		self.h5 = builder.get_object("h5")
		self.h6 = builder.get_object("h6")
		self.f1 = builder.get_object("f1")
		self.f2 = builder.get_object("f2")
		self.f3 = builder.get_object("f3")
		self.plog = builder.get_object("statuslog")
		############################################################################

		############################################################################
		# OTRAS ACCIONES
		self.info.set_text("No se ha reproducido nada aun")
		self.filtro = gtk.FileFilter()
		try:
			dom = minidom.parse("track.xml")
			for i in range(0,len(dom.getElementsByTagName("track"))):
				self.medialist.append([path.clearing(dom.getElementsByTagName("track")[i].firstChild.data),path.clearing(dom.getElementsByTagName("ruta")[i].firstChild.data)])
		except:
			pass
		self.clave.set_visibility(False) 
		self.clave.set_invisible_char ('*') 
		self.clave2.set_visibility(False) 
		self.clave2.set_invisible_char ('*') 
		self.clave2_2.set_visibility(False) 
		self.clave2_2.set_invisible_char ('*') 
		self.plog.set_pulse_step(0.01)
		#############################################################################


		#############################################################################
		# VARIABLES DE MAPEO DE REPRODUCCION
		self.MAPA = [] 
		self.current = 0
		self.controler = 0
		self.max = 0
		#############################################################################

		#############################################################################
    	# EVENTOS
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
		"on_volumen_value_changed":self.cb_master_slider_change,
		"on_log_clicked":self.login,
		"on_acceso_clicked":self.acceso,
		"on_nuevo_clicked":self.registrar,
		"on_tweet_clicked":self.tuitear,
		"on_final_clicked":self.completado,
		"on_refresh_clicked":self.refresh,
		"on_AbrirB_clicked":self.abrir_archivos
		}
		builder.connect_signals(dict)
		#############################################################################

		#############################################################################
		# CONTROLADOR DE REPRODUCCION
		self.player = gst.element_factory_make("playbin2", "player")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		self.hilo = MiThread(0,self.progressBar,1)
		#############################################################################
#####################################################################################

	def login(self,widget):
		Log = LOG(self.login_state,self.plog,self.info)
		Log.start()

	def login_state(self):
		found = -1
		count = 0
		clave = self.clave.get_text()
		usuario = self.usuario.get_text()
		try:
			dom = minidom.parse("OAuth.xml")
			for i in range(0,len(dom.getElementsByTagName("id"))):
				if usuario == dom.getElementsByTagName("id")[i].firstChild.data and  clave == dom.getElementsByTagName("clave")[i].firstChild.data:
					found = i
					count = count + 1
			if count > 0: 
				auth.set_access_token(dom.getElementsByTagName("KEY")[found].firstChild.data,dom.getElementsByTagName("SECRET")[found].firstChild.data)
				global API 
				API = tweepy.API(auth)
				self.recent_tweets()
				US = DEF(self.US)
				US.start()
				HM = DEF(self.Home)
				HM.start()
				self.user.set_text( dom.getElementsByTagName("id")[found].firstChild.data )
				self.step1.hide()
				self.logged.show()
			else:
				self.status.set_text('Usuario o clave incorrecta')
 		except:
			pass

	def recent_tweets(self):
		arrayObject = API.user_timeline()
		self.tweet1.set_text(self.parrafo(arrayObject[0].text))
		self.tweet2.set_text(self.parrafo(arrayObject[1].text))
		self.tweet3.set_text(self.parrafo(arrayObject[2].text))
		self.tweet4.set_text(self.parrafo(arrayObject[3].text))
		self.tweet5.set_text(self.parrafo(arrayObject[4].text))
		self.tweet6.set_text(self.parrafo(arrayObject[5].text))

	def Home(self):
		self.info.set_text('Cargando Home')
		arrayObject = API.home_timeline()
		self.h1.set_text(arrayObject[0].user.screen_name+'\n '+self.parrafo(arrayObject[0].text))
		self.h2.set_text(arrayObject[1].user.screen_name+'\n '+self.parrafo(arrayObject[1].text))
		self.h3.set_text(arrayObject[2].user.screen_name+'\n '+self.parrafo(arrayObject[2].text))
		self.h4.set_text(arrayObject[3].user.screen_name+'\n '+self.parrafo(arrayObject[3].text))
		self.h5.set_text(arrayObject[4].user.screen_name+'\n '+self.parrafo(arrayObject[4].text))
		self.h6.set_text(arrayObject[5].user.screen_name+'\n '+self.parrafo(arrayObject[5].text))
		self.info.set_text('Home Cargado')

	def US(self):
		arrayObject = API.followers()
		self.f1.set_text('@'+arrayObject[0].screen_name)
		self.f2.set_text('@'+arrayObject[1].screen_name)
		self.f3.set_text('@'+arrayObject[2].screen_name)
		self.info.set_text('Seguidores recientes cargados')

	def song(self):
		try:
			if self.titulo.get_text() == '...' or self.titulo.get_text() == '' or self.titulo.get_text() == ' ':
				API.update_status("Escuchando Musica a traves de #GLMPlayer")
			else:
				titulo = ''
				for letra in self.titulo.get_text():
					if letra == ' ':
						pass
					else:
						titulo = titulo + letra
				API.update_status("#NP #"+ titulo +" a traves de #GLMPlayer")
			RC = DEF(self.recent_tweets)
			RC.start()
		except:
			self.info.set_text('Tweet duplicado, no se envia actualizacion')

	def parrafo(self,string):
		bufferstr = '\n  '
		token_ctn = 0
		break_ctn = 0
		for token in string:
			if token_ctn < 60:
				bufferstr = bufferstr + token
				token_ctn = token_ctn + 1
			else:
				if token == ' ' and break_ctn == 0:
					bufferstr = bufferstr + '  \n  '
					break_ctn = 1
					token_ctn = token_ctn + 1
				else:
					bufferstr = bufferstr + token
					token_ctn = token_ctn + 1
		bufferstr = bufferstr + '\n  '
		return bufferstr

	def refresh(self,widget):
		RC = DEF(self.recent_tweets)
		US = DEF(self.US)
		RC.start()
		US.start()

#####################################################################################
# CONTROL DEL VOLUMEN
	def cb_master_slider_change(self, widget,event,data=None):
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
			proc.wait()
		except:
			pass	
#####################################################################################

#################################################################################
# VERIFICACION DE LA CUENTA DE TWITTER
	def acceso(self,widget):
		self.step1.hide()
		self.step2.show()


###################################################################################

####################################################################################
# TUITEAR
	def tuitear(self,widget):
		SN = DEF(self.song)
		SN.start()

####################################################################################

#####################################################################################
# REGISTRO
	def registrar(self,widget):
		CUsuario = self.usuario2.get_text()
		CClave = self.clave2.get_text()
		CClave2 = self.clave2_2.get_text()
		dom = minidom.parse("OAuth.xml")
		count = 0
		for i in range(0,len(dom.getElementsByTagName("id"))):
			if CUsuario == dom.getElementsByTagName("id")[i].firstChild.data:
				count = count + 1
		if count > 0: 
			self.msj.set_text('El usuario ya existe')
		else:
			if ( CClave == CClave2 ) and ( len(CUsuario) ) > 0 and ( len(CClave) > 5 ):
				webbrowser.open(auth.get_authorization_url())
			else:
				self.msj.set_text('* Minimo 6 caracteres para la clave \n * Rellene todos los campos \n * Verifique que las claves coincidan ')


######################################################################################

######################################################################################
# COMPLETADO
	def completado(self,widget):
		try:
			CUsuario = self.usuario2.get_text()
			CClave = self.clave2.get_text()
			CClave2 = self.clave2_2.get_text()
			auth.get_access_token(int(self.codigo.get_text()))
			ACCESS_KEY = auth.access_token.key
			ACCESS_SECRET = auth.access_token.secret
			########################################
			dom = minidom.parse("OAuth.xml")
			wml = dom.getElementsByTagName('wml')
			prin = dom.createElement('usuario')
			wml[0].appendChild(prin)

			ids = dom.createElement('id')
			prin.appendChild(ids)
			texts = dom.createTextNode(CUsuario)
			ids.appendChild(texts)

			clave = dom.createElement('clave')
			prin.appendChild(clave)
			Pass = dom.createTextNode(CClave)
			clave.appendChild(Pass)

			KEY = dom.createElement('KEY')
			prin.appendChild(KEY)
			CKEY = dom.createTextNode(ACCESS_KEY)
			KEY.appendChild(CKEY)

			SECRET = dom.createElement('SECRET')
			prin.appendChild(SECRET)
			CSECRET = dom.createTextNode(ACCESS_SECRET)
			SECRET.appendChild(CSECRET)

			xmldocument = open("OAuth.xml","w")
			dom.writexml(xmldocument)
			xmldocument.close()
			#####################################
			self.step2.hide()
			self.step1.show()
		except:
			self.msj.set_text('Lo sentimos, el codigo no es valido,\n intenta de nuevo')

######################################################################################

#####################################################################################
# AGREGAR ARCHIVOS
	def abrir_archivos(self,widget):
		pattern = (".mp3") 	
		self.filtro.set_name("*.mp3")
		for name, pattern in filepattern:
 			self.filtro.add_pattern(pattern)         	
		self.agregar_ventana.add_filter(self.filtro)
		respt=self.agregar_ventana.run()
		self.agregar_ventana.remove_filter(self.filtro)
		self.agregar_ventana.hide()
		dom = minidom.parse("track.xml")
		wml = dom.getElementsByTagName('wml')
		if respt == -5:
			fileselected = self.agregar_ventana.get_filenames()
			for files in fileselected:
				(dirs,files)= os.path.split(files)
				self.medialist.append([files,dirs])
				maincard = dom.createElement("pista")
				wml[0].appendChild(maincard)
				nm = dom.createElement("track")
				maincard.appendChild(nm)
				nombre = dom.createTextNode(files)
				nm.appendChild(nombre)
				dr = dom.createElement("ruta")
				maincard.appendChild(dr)
				path = dom.createTextNode(dirs)
				dr.appendChild(path)
			xmldocument = open("track.xml","w")
			dom.writexml(xmldocument)
			xmldocument.close()
#####################################################################################

#####################################################################################			
# MENSAJES DE ERROR PARA CONSOLA
	def on_message(self, bus, message):
		t = message.type 
		if t == gst.MESSAGE_EOS: 
			self.player.set_state(gst.STATE_NULL)
			self.next_state()
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
####################################################################################
			
####################################################################################
# MANEJADORA GSTREAMER                                                             
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
####################################################################################

####################################################################################
# VENTANAS
	# Muestra el mensaje de about 
	def about(self,widget):
		self.help.show()

	# Cierra el menjSae de about
	def close(self,widget):
		self.help.hide()

	# Funcion que cierra la ventana
	def destroy(self,widget):
		gtk.main_quit()
		self.hilo.stop()
####################################################################################

####################################################################################
# CONTROLES
	def play(self,widget):
		self.play_state()
	
	def pause(self,widget):
		self.player.set_state(gst.STATE_PAUSED)
		self.info.set_text(" Se ha pausado la reproduccion")
		self.state,self.dur = self.hilo.pause()	
		self.controler = 1
		
	def prev(self,widget):
		self.prev_state()
		
	
	def next(self,widget):
		self.next_state()

	def stop(self,widget):
		self.stop_state()
#####################################################################################

#####################################################################################
# MANEJADORES DE REPRODUCCION Y MAPEO DE LISTA
	def REP(self):
		self.stop_state()
		select = self.tree.get_selection()
		filepath = path.on_tree_selection_changed(select)
		tag = eyeD3.Tag()
		audio = MP3(filepath)
		file = File(filepath)
		try:
			artwork = file.tags['APIC:'].data 
			with open('artwork.png', 'wb') as img:
				img.write(artwork)
			self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size('artwork.png', 200, 200))
		except:
			self.imagen.set_from_file("NOCD.png")
		
		duration = audio.info.length
		times = int(duration/60) + ((duration/60) - int(duration/60))/60
		tag.link(filepath)
		self.info.set_text(" Se ha iniciado la reproduccion ")
		self.artista.set_text(tag.getArtist())
		self.album.set_text(tag.getAlbum())
		self.duracion.set_text("%.2f" % times + "  min")
		self.titulo.set_text(tag.getTitle())
		self.player.set_property("uri", "file://"+filepath)
		self.hilo = MiThread(duration,self.progressBar,1)
		self.hilo.start()
		self.player.set_state(gst.STATE_PLAYING)

	def play_state(self):
		if self.controler == 1:
			self.player.set_state(gst.STATE_PLAYING)
			self.info.set_text(" Se ha iniciado la reproduccion ")
			self.hilo = MiThread(self.dur,self.progressBar,self.state)
			self.hilo.start()
			self.controler = 0
		else:
			select = self.tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			contador = 0
			val = 0
			node = " "
			for i in filas:
				for token in i:
					if token == '(' or token == ' ' or token == ',' or token == ')':
						pass
					else:
						node = token
				val = int(node)
				iterador = modelo.get_iter(i)
				while iterador != None:
					iterador = modelo.iter_next(iterador)
					contador = contador + 1
			self.MAPA = path.ObtenerLista(contador,val)
			self.max = contador
			self.current = 0;
			self.REP()
	# Corregir error con funcion next
	def next_state(self):
		if self.current >= self.max - 2:
			self.current = -1
		self.current = self.current + 1
		select = self.tree.get_selection()
		(modelo,filas) = select.get_selected_rows()
		iterador = modelo.get_iter(self.MAPA[self.current])
		select.select_iter(iterador)
		self.REP()
	#Corregir error con funcion prev
	def prev_state(self):
		if self.current <= 0:
			self.current = self.max - 1
		self.current = self.current - 1	
		select = self.tree.get_selection()
		(modelo,filas) = select.get_selected_rows()
		iterador = modelo.get_iter(self.MAPA[self.current])
		select.select_iter(iterador)
		self.REP()	

	def stop_state(self):	
		self.player.set_state(gst.STATE_NULL)
		self.info.set_text(" Se ha detenido la reproduccion")
		self.hilo.stop()	
###################################################################################

###################################################################################
# MANEJO DE HILO DE PROGRESO         
class MiThread(threading.Thread):  
    def __init__(self, duration,progressBar,curr):  
        threading.Thread.__init__(self)  
        self.duration = duration
        self.curr = curr
        self.progressBar =  progressBar
        self.flag = True
  
    def run(self): 
    	self.flag = True 
        while (self.curr < self.duration ) and self.flag == True:
        	step = 100 / self.duration
        	nxt = self.curr * step
        	self.progressBar.set_value(nxt)
          	time.sleep(1)
          	self.curr = self.curr + 1

    def stop(self):
      	self.flag = False
      	self.curr = 1
      	self.progressBar.set_value(0)

    def pause(self):
    	self.flag = False
    	return self.curr,self.duration


 #MANEJO DE HILO DE pulso     
class BAR(threading.Thread):  
    def __init__(self, bar,flag):  
        threading.Thread.__init__(self)  
        self.bar = bar
        self.flag = flag

    def run(self): 
    	while self.flag:
    		time.sleep(0.01)
    		self.bar.pulse()
    	self.bar.set_fraction(0)

    def stop(self,var):
    	self.flag = var

###################################################################################
# MANEJO DE HILO DE twitter     
class LOG(threading.Thread):  
    def __init__(self, login,plog,info = None):  
        threading.Thread.__init__(self)  
        self.function = login
        self.plog = plog
        self.info = info

    def run(self): 
		self.info.set_text('Estamos cargando tus datos desde https://twitter.com')
		Pul = BAR(self.plog,True)
		Pul.start()
		self.function()
		Pul.stop(False)
		self.info.set_text('Tweets recientes cargados')

##################################################################################

class DEF(threading.Thread):  
    def __init__(self, function):  
        threading.Thread.__init__(self)  
        self.function = function

    def run(self): 
		self.function()

# Ejecucion del programa
if __name__ == "__main__":
    main()
    gtk.main()


