import pygtk,gtk,message
pygtk.require("2.0")

def create_tree():
	scrolled_window = gtk.ScrolledWindow()
	scrolled_window.set_border_width(0)
	scrolled_window.set_size_request(100,200)
	scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	return scrolled_window

def update_tree(_dir,_swindow):
	try:
		l = len(_dir)
		if l > 0:
			cont = gtk.Table(1,l,True)
			j = 0
			for label in _dir:
				bt = gtk.Label(label)
				cont.attach(bt,0,1,j,j+1,gtk.FILL,gtk.EXPAND,0,0)
				j = j+1
				bt.show()
			cont.show()
			_swindow.add_with_viewport(cont)
		else: 	
			alert = gtk.Label(message.ErrNoImport)
			alert.show()
			_swindow.add_with_viewport(alert)	
	except:
		alert = gtk.Label(message.ErrNoImport)
		alert.show()
		_swindow.add_with_viewport(alert)
