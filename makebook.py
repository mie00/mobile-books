import pyodbc
from os import makedirs,path,listdir
def generate(number):
	DBfile = 'data\\%d.mdb'%(number)
	if not path.exists('op\\%d'%(number)):
		makedirs('op\\%d'%(number))
	conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
	cursor = conn.cursor()
	 
	SQL = 'SELECT * FROM book ORDER BY id'
	for row in cursor.execute(SQL): # cursors are iterable
	    with open('op\\%d\\%d.html'%(number,row.id),'wb') as f:

	    	f.write('<!DOCTYPE html><html><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><body dir="rtl">\n\
	    		<p><a href="%d.html">&lt;</a> | <a href="../../index.html">&uarr;</a> | <a href="%d.html">&gt;</a></p>\
	    		<p>%s</p></body></html>'%(row.id-1,row.id+1,row.nass.decode('windows-1256').encode('utf-8').replace('\r','<br />')))
	cursor.close()
	conn.close()

for i in listdir('data'):
	generate(int(i[:-4]))

import updateindex