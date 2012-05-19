#!/usr/bin/env python
#
# Prost Web Server is simple web server for quickly and easily starting of web server without good computer knowledge
# Prost Web Server is 100% Python writen.
# Copyright (C) 2006 PoisoneR
# Author: PoisoneR
# License: GPL

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.



# TODO:
# option witch dir to serve, must change the path variable
# icons of files
# distribute

import os
import sys
import cgi
import urllib
import socket
import getopt
import BaseHTTPServer
import SimpleHTTPServer
from StringIO import StringIO

__author__ = "PoisoneR"
__version__ = "0.1.1"
__copyright__ = "(c) 2006 PoisoneR <poisonerbg@gmail.com>"
__projecthome__ = "http://pwebserv.sourceforge.net"

port = 4040 #default port
if os.name == 'nt':
	uid = 1000 #the user is not root
else:
	uid = os.getuid()

class ProstWebServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	server_version = "ProstWebServer/" + __version__
	def list_directory(self, path):
		"""Overwrite the list_directory method"""
		print path
		try:
			list = os.listdir(path)
		except os.error:
			self.send_error(404, "No permission to list directory")
			return None
		list.sort(key=lambda a: a.lower())
		f = StringIO()
		parentDir = ".."	
		f.write("<html>\n")
		f.write("<body bgcolor=\"black\" link=\"white\" alink =\"blue\" vlink=\"yellow\">\n<font color=\"lime\">\n")
		f.write("<title>Prost Web Server - Directory listing for %s</title>\n" % urllib.unquote(self.path))
		f.write("<h3>Directory listing for %s</h3>\n" % urllib.unquote(self.path))
		f.write("<hr>\n<ul>\n")
		f.write("<a href=\"%s\"> Parent Directory</a>\n" % urllib.quote(parentDir))
		for name in list:
			fullname = os.path.join(path, name)
			displayname = linkname = name
			# print linkname
			fsize = getFileSize(fullname)
			# Append / for directories or @ for symbolic links
			if os.path.isdir(fullname):
				displayname = name + "/"
				linkname = name + "/"
			if os.path.islink(fullname):
				displayname = name + "@"
				# Note: a link to a directory displays with @ and links with /
			f.write('<li><a href="%s">%s</a> - %s kB\n' % (urllib.quote(linkname), cgi.escape(displayname), fsize))
		f.write("</ul>\n<hr>\n")
		f.write("<a href=\"%s\">Prost Web Server v%s</a> at %s Port %s\n" % (__projecthome__, __version__, socket.gethostbyaddr(socket.gethostname())[0], port))
		f.write("</font>\n</body>\n")
		f.write("</html>\n")
		length = f.tell()
		f.seek(0)
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.send_header("Content-Length", str(length))
		self.end_headers()
		return f

def getFileSize(path):
	"""retrurn the file size by path"""
	stat = os.stat(path)
	filesize = stat[6]
	filesize = int(filesize) / 1024 # in kB
	return filesize

def helpScreen():
	print """pwebserv""", __version__, """ - Prost Web Server
""",__copyright__,"""

Usage:
	pwebserv [-h] [-p port_number]

	-h, --help show this screen and exit
	-p, --port change the default port(""",port,""") of the web server
	-v, --version show the version of the program and exit
	
Example:
	Go to the directory which you want to be a document root and type:
	pwebserv -p 1234

The project page is at""", __projecthome__,"""
This program is covered by the GNU General Public License. See COPYING for
further information."""
	sys.exit(0)

def versionInfo():
	print 'Prost Web Server version', __version__
	sys.exit(0)

def error(msg):
	print msg
	sys.exit(2)

def parseOptions():
	global port
	try:
		opts, args = getopt.getopt (sys.argv[1:], "hvp:v", ["port=", "help", "version"] )
	except getopt.GetoptError:
		error ('Wrong command-line option. See "pwebserv --help" first.')
	
	#print opts
	#print args
	for option, argument in opts:
		if option in ['-p', '--port']:
			try:
				port = int(argument)
			except:
				error("The argument for port number must be integer.")
		if option in ['-h', '--help']:
			helpScreen()
		if option in ['-v', '--version']:
                        versionInfo()

def main():
	parseOptions()
	if uid == 0:
		error("Don't run pwebserv as root.")
	if port < 1024:
		error("Please select port >= 1024")
	
	pwebserv = BaseHTTPServer.HTTPServer(('', port), ProstWebServerHandler)
	print "The pwebserv is running on port", port
	try:
		pwebserv.serve_forever()
	except KeyboardInterrupt:
		error("Interruped by user with SIGINT.")

if __name__ == "__main__":
	main()

# vim:set syntax=python: