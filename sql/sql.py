# -*- coding: UTF-8 -*-

import sqlite3
import sys, os
import Image, ImageFile

def InsertImage(name, Fname):
	f = file(Fname, "rb")
	data = f.read()
	f.close()
	# проверяем существование элемента в базе
	sql = "SELECT name FROM Units WHERE name=?"
	cursor.execute(sql, [name])
        item = cursor.fetchone()
        if not item == None:
		sql = "UPDATE Units SET img=? WHERE name=?"
	else:
		sql = "INSERT INTO Units (img, name) VALUES (?,?)"
	cursor.execute(sql, (sqlite3.Binary(data), name) )

def GetImage(name):
	sql = "SELECT img FROM Units WHERE name=?"
	cursor.execute(sql, [name])
	item = cursor.fetchone()
	if item == None:
		return
	data = item[0]
	p = ImageFile.Parser()
	p.feed(data)
	return p.close()

def SetMapUnits(map, units):
        # проверяем существование элемента в базе
        sql = "SELECT name FROM Maps WHERE name=?"
        cursor.execute(sql, [map])
        item = cursor.fetchone()
        if item == None: # добавляем карту
		sql = "INSERT INTO Maps (name) VALUES (?)"
		cursor.execute(sql, [map])
	sqlS = "SELECT map, unit FROM MapUnit WHERE map=? AND unit=?"
	sqlA = "INSERT INTO MapUnit (map, unit) VALUES (?, ?)"
	for unit in units:
		cursor.execute(sqlS, (map, unit))
		item = cursor.fetchone()
	        if item == None:
        	        cursor.execute(sqlA, (map, unit))
 		

if __name__ == "__main__":
	global connection
	global cursor
#	reload(sys)
#	sys.setdefaultencoding("UTF-8")
	try:
		type = sys.argv[1]
	except:
		print "\nнедостаточно параметров.\nпараметр -h для вывода справки."
		sys.exit(0)

	connection = sqlite3.connect("DSO.Battle.db3")
	connection.text_factory = str
	cursor = connection.cursor()

	if type == "-a": # добавляем юнит
		try:
			name = sys.argv[2]
			Fname = sys.argv[3]
		except:
			print "\nнедостаточно параметров"
			sys.exit(0)
		InsertImage(name,Fname)
	elif type == "-g": # получаем картинку юнита
		try:
			name = sys.argv[2]
		except:
			print "\nнедостаточно параметров"
			sys.exit(0)
		im = GetImage(name)
		if im == None:
			pass
		else:
			im.show()
	elif type == "-i": # добавляем юнитов из каталога
                try:
                        dir = sys.argv[2]
                except:
                        print "\nнедостаточно параметров"
                        sys.exit(0)

		if not os.path.exists(dir):
                        print "\nпуть не существует"
			sys.exit(1)
		files = os.listdir(dir)
		for ifile in files:
			fullname = os.path.join(dir, ifile)  # получаем полное имя
			if os.path.isfile(fullname):        # если это файл...
				name = os.path.splitext(os.path.basename(fullname))[0]
				InsertImage(name, fullname)
	elif type == "-m": # задаём список юнитов на карте
                try:
                        map = sys.argv[2]
                except:
                        print "\nнедостаточно параметров"
                        sys.exit(0)
		SetMapUnits(map, sys.argv[3:])
	elif type == "-h":
		print \
			"\n\t-a Unit Image	: добавить юнита" \
			"\n\t-i Dir		: добавить юнитов из каталога" \
			"\n\t-g Unit		: показать картинку юнита" \
			"\n\t-m Map Units...	: указать юнитов на карте"

	connection.commit()
	connection.close()
