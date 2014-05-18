import pyodbc
from os import makedirs,path,listdir
def generate(number):
	DBfile = 'in\\%d.mdb'%(number)
	if not path.exists('out\\%d'%(number)):
		makedirs('out\\%d'%(number))
	conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
	cursor = conn.cursor()
	 
	SQL = 'SELECT * FROM book ORDER BY id'
	ids = map(lambda x:x.id,cursor.execute('SELECT id FROM book ORDER BY id'))
	with open("out\\%d\\index.html"%(number),'wb') as f:
		f.write(' '.join(map(lambda x:"<a href='%d.html'>%d</a>"%(x,x),ids)))
	ids=[ids[0]]+ids+[ids[-1]]
	for i,row in enumerate(cursor.execute(SQL)): # cursors are iterable
	    with open('out\\%d\\%d.html'%(number,row.id),'wb') as f:
	    	f.write('<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body dir="rtl">\n\
	    		<p>PAGE: %d</p>\n\
	    		<p><a href="%d.html">&lt;&lt;&lt;</a> | <a href="../../index.html">INDEX</a> | <a href="%d.html">&gt;&gt;&gt;</a></p>\n\
	    		<p>%s</p>\n\
	    		<p><a href="%d.html">&lt;&lt;&lt;</a> | <a href="../../index.html">INDEX</a> | <a href="%d.html">&gt;&gt;&gt;</a></p>\n\
	    		<p>PAGE: %d</p>\n\
	    		</body></html>'%(row.id,ids[i],ids[i+2],row.nass.decode('windows-1256').encode('utf-8').replace('\r','<br />'),ids[i],ids[i+2],row.id))
	cursor.close()
	conn.close()
for i in listdir('in'):
		generate(int(i[:-4]))


DBfile = 'main.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cursor = conn.cursor()

def get_book_name(id):
	SQL = 'SELECT bk FROM 0bok WHERE bkid=%i'%(id)
	for row in cursor.execute(SQL): # cursors are iterable
		return row.bk.decode('windows-1256').encode('utf-8')
def format_book(id1):
	id=int(id1)
	return '<a href="out/%i/index.html">%s</a>'%(id,get_book_name(id))


op='<!doctype html>\
<html lang="en">\
<head>\
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\
	<title>mobile-books</title>\
</head>\
<body dir="rtl">\
%s\
</body>\
</html>'%('<br />'.join(map(format_book,listdir('out'))))
with open('index.html','wb') as f:
	f.write(op)
cursor.close()
conn.close()

