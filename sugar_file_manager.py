#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sugar-file-manager
#       
#       Copyright 2011 Daniel Francis <santiago.danielfrancis@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
import gio
import gtk
from sugar.activity import activity
import filemanager

class SugarFileManagerActivity(activity.Activity):
	def paste(self, widget, source, destination):
		filemanager.copy(gio.File(source).get_path(), gio.File(destination).get_path())
	
	def new_dir(self, widget, current_dir):
		filemanager.new_directory(gio.File(uri=current_dir).get_path())
	
	def current_directory_menu(self, widget, menu):
		create_directory = gtk.MenuItem("Crear Carpeta")
		create_directory.connect("activate", self.new_dir, widget.get_current_directory())
		create_directory.show()
		menu.append(create_directory)
		clipboard_data = filemanager.clipboard.get_file_uri()
		if clipboard_data:
			if clipboard_data + "/" != widget.get_current_directory() and os.path.dirname(clipboard_data) + "/" != widget.get_current_directory():
				_paste = gtk.MenuItem("Pegar")
				_paste.connect("activate", self.paste, clipboard_data, widget.get_current_directory())
				_paste.show()
				menu.append(_paste)
		return True
	
	def copy_file(self, widget, uri):
		filemanager.clipboard.copy_file_to_clipboard(uri)
	
	def delete_file(self, widget, uri):
		gfile = gio.File(uri=uri)
		filemanager.delete(gfile.get_path())
	
	def file_menu(self, widget, uri, menu):
		copy = gtk.MenuItem("Copiar")
		copy.connect("activate", self.copy_file, uri)
		copy.show()
		menu.append(copy)
		delete = gtk.MenuItem("Eliminar")
		delete.connect("activate", self.delete_file, uri)
		delete.show()
		menu.append(delete)
		return True
	
	def go_up_callback(self, widget, filemanager_widget):
		filemanager_widget.go_up()
	
	def refresh_callback(self, widget, filemanager_widget):
		filemanager_widget.set_current_directory(filemanager_widget.get_current_directory())
	
	def __init__(self, handle):
		activity.Activity.__init__(self, handle)
		os.environ["FILEMANAGER_PATH"] = os.path.join(os.environ["SUGAR_BUNDLE_PATH"], "share", "sugar-file-manager")
		self.set_title("Sugar File Manager")
		toolbox = activity.ActivityToolbox(self)		
		self.set_toolbox(toolbox)
		toolbox.show()
		toolbox.get_activity_toolbar().share.hide()
		toolbox.get_activity_toolbar().keep.hide()
		#vbox = gtk.VBox() 	 # NO ENCONTRE SOLUCIÓN
		#toolbar = gtk.Toolbar()
		#button1 = gtk.ToolButton("gtk-go-up")
		#button1.show()
		#toolbar.insert(button1, -1)
		#refresh = gtk.ToolButton("gtk-refresh")
		#refresh.show()
		#toolbar.insert(refresh, -1)
		toolbar.show()
		vbox.pack_start(toolbar, False, True)
		widget = filemanager.Widget()
		#go_up.connect("clicked", go_up_callback, widget)
		#refresh.connect("clicked", refresh_callback, widget)
		widget.show()
		current_directory = gio.File(path=os.environ["HOME"])
		widget.set_current_directory(current_directory.get_uri())
		widget.connect("file-menu", self.file_menu)
		widget.connect('current-directory-menu', self.current_directory_menu)
		vbox.pack_start(widget, True, True, 0)
		vbox.show()
		self.set_canvas(widget)
		self.show()
