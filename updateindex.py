import pyodbc
from os import listdir
DBfile = 'main.mdb'
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cursor = conn.cursor()

def get_book_name(id):
	SQL = 'SELECT bk FROM 0bok WHERE bkid=%i'%(id)
	for row in cursor.execute(SQL): # cursors are iterable
		return row.bk.decode('windows-1256').encode('utf-8')
def format_book(id1):
	id=int(id1)
	return '<a href="op/%i/1.html">%s</a>'%(id,get_book_name(id))


op='<!doctype html>\
<html lang="en">\
<head>\
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\
	<title>mobile-books</title>\
</head>\
<body dir="rtl">\
%s\
</body>\
</html>'%('<br />'.join(map(format_book,listdir('op'))))
with open('index.html','wb') as f:
	f.write(op)
cursor.close()
conn.close()

