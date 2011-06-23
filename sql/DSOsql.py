#!/usr/bin/env python2.6
# -*- coding: UTF-8 -*-

import sqlite3
import sys, os
import Image, ImageFile
import argparse


def ConnectOpen():
	global connection
	global cursor

	connection = sqlite3.connect("DSO.Battle.db3")
	#connection = sqlite3.connect("/home/mogidin/Downloads/web2py/applications/test/databases/DSO.Battle.db3")
	connection.text_factory = str
	cursor = connection.cursor()

def ConnectClose():
        connection.commit()
        connection.close()	

def InsertImage(name, Fname):
	ConnectOpen()
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
	ConnectClose()

def GetImage(name):
	ConnectOpen()
	sql = "SELECT img FROM Units WHERE name=?"
	cursor.execute(sql, [name])
	item = cursor.fetchone()
	if item == None:
		return
	data = item[0]
	p = ImageFile.Parser()
	p.feed(data)
	ConnectClose()
	return p.close()

def SetMapUnits(map, units):
	ConnectOpen()
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
	ConnectClose()

def SetUnitInfo(unit, params):
	if not len(params) == 7:
		print "\n параметры: HP, MinDmg, MaxDmg, Accuracy, Initiative [F-Fast, N-Normal, S-Slow], Courage, Skills [H-HeadHunter, S-SplashDamage, T-TurmBonus, N-None]"
		sys.exit(1)
	params.append(unit)
	ConnectOpen()
        # проверяем существование элемента в базе
        sql = "SELECT name FROM Units WHERE name=?"
        cursor.execute(sql, [unit])
        item = cursor.fetchone()
        if not item == None:
                sql = "UPDATE Units SET HP=?,MinDmg=?,MaxDmg=?,Accuracy=?,Initiative=?,Courage=?,Skills=? WHERE name=?"
        else:
                sql = "INSERT INTO Units (HP, MinDmg, MaxDmg, Accuracy, Initiative, Courage, Skills, name) VALUES (?,?,?,?,?,?,?,?)"
        cursor.execute(sql, params)
	ConnectClose()

def CheckDB():
	ConnectOpen()
	sqlM = "SELECT name FROM Maps"
	cursor.execute(sqlM)
	Maps=[]
	for map in cursor.fetchall():
		Maps.append(map[0])

        sqlU = "SELECT name FROM Units"
        cursor.execute(sqlU)
        Units=[]
        for unit in cursor.fetchall():
                Units.append(unit[0])

	sqlMUm = "SELECT DISTINCT map FROM MapUnit"
	cursor.execute(sqlMUm)
	MUmap=[]
	for map in cursor.fetchall():
                MUmap.append(map[0])

        sqlMUu = "SELECT DISTINCT unit FROM MapUnit"
        cursor.execute(sqlMUu)
        MUunit=[]
        for unit in cursor.fetchall():
                MUunit.append(unit[0])
	
	print "\nCheck MapUnits in Maps..."
	for map in MUmap:
		if not map in Maps:
			print "Map '%s' from MapUnits not found in Maps" % map

	print "\nCheck Maps in MapUnits..."
        for map in Maps:
                if not map in MUmap:
                        print "Map '%s' from Maps not found in MapUnits" % map

	print "\nCheck MapUnits in Units..."
	for unit in MUunit:
                if not unit in Units:
                        print "Unit '%s' from MapUnits not found in Units" % unit

	print "\nCheck Units in MapUnits..."
        for unit in Units:
                if not unit in MUunit:
                        print "Unit '%s' from Units not found in MapUnit" % unit
	ConnectClose()

def SetAlias(alias, name):
	ConnectOpen()
        # проверяем существование элемента в базе
        sql = "SELECT alias FROM Alias WHERE alias=?"
        cursor.execute(sql, [alias])
        item = cursor.fetchone()
        if not item == None:
                sql = "UPDATE Alias SET name=? WHERE alias=?"
        else:
                sql = "INSERT INTO Alias (name, alias) VALUES (?,?)"
	cursor.execute(sql, (name, alias))
	ConnectClose()

def PrintData(type, params):
	if type == "all":
		PrintData("unit")
		PrintData("mapunit")
		PrintData("alias")
	elif type == "unit":
		ConnectOpen()
		print "\nUnit list:"
		sql = "SELECT name FROM Units ORDER BY name"
		cursor.execute(sql)
		for unit in cursor.fetchall():
			print "\t%s" % unit[0]
		ConnectClose()
	elif type == "map":
		ConnectOpen()
                print "\nMap list:"
                sql = "SELECT name FROM Maps ORDER BY name"
                cursor.execute(sql)
                for map in cursor.fetchall():
                        print "\t%s" % map[0]
		ConnectClose()
	elif type == "mapunit":
		ConnectOpen()
		if len(params) > 0:
			maps = []
			for map in params:
				maps.append((map,))
		else:
			sql = "SELECT name FROM Maps ORDER BY name"
			cursor.execute(sql)
			maps = cursor.fetchall()

		print "\nMapUnit list:"
		sqlMU = "SELECT unit FROM MapUnit WHERE map=?"
		for map in maps:
			print "\t%s" % map[0]
			cursor.execute(sqlMU,[map[0]])
			units = cursor.fetchall()
			for unit in units:
				print "\t\t%s" % unit[0]
		ConnectClose()
	elif type == "alias":
		ConnectOpen()
                print "\nAlias list:"
                sql = "SELECT alias, name FROM Alias ORDER BY name"
                cursor.execute(sql)
                for alias in cursor.fetchall():
                        print "\t%s\t: %s" % (alias[0], alias[1])
		ConnectClose()

if __name__ == "__main__":
#	reload(sys)
#	sys.setdefaultencoding("UTF-8")
	try:
		type = sys.argv[1]
	except:
		print "\nнедостаточно параметров.\nпараметр -h для вывода справки."
		sys.exit(0)

	if type == "--unit": # добавляем юнит
		try:
			name = sys.argv[2]
			Fname = sys.argv[3]
		except:
			print "\nнедостаточно параметров"
			sys.exit(0)
		InsertImage(name,Fname)
	elif type == "--setunitinfo":
                try:
                        unit = sys.argv[2]
                except:
                        print "\nнедостаточно параметров"
                        sys.exit(0)
                SetUnitInfo(unit, sys.argv[3:])
	elif type == "--show": # получаем картинку юнита
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
	elif type == "--load": # добавляем юнитов из каталога
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
	elif type == "--map": # задаём список юнитов на карте
                try:
                        map = sys.argv[2]
                except:
                        print "\nнедостаточно параметров"
                        sys.exit(0)
		SetMapUnits(map, sys.argv[3:])
        elif type == "--check": # задаём список юнитов на карте
                CheckDB()
        elif type == "--alias": # задать алиас
                try:
                        alias = sys.argv[2]
			name = sys.argv[3]
                except:
                        print "\nнедостаточно параметров"
                        sys.exit(0)
                SetAlias(alias, name)
	elif type == "--print":
                try:
                        ptype = sys.argv[2]
                except:
                        print "\tall		: показать всё"
                        print "\tunit		: показать список юнитов"
                        print "\tmap		: показать список карт"
                        print "\tmapunit		: показать юнитов на картах"
                        print "\talias		: показать алиасы"
                        sys.exit(0)
                PrintData(ptype, sys.argv[3:])
	elif type == "-h":
		print \
			"\n\t--unit Unit Image	: добавить юнита" \
			"\n\t--setunitinfo Unit Param...	: записать ТТХ юнита" \
			"\n\t--load Dir		: добавить юнитов из каталога" \
			"\n\t--show Unit		: показать картинку юнита" \
			"\n\t--map Map Units...	: указать юнитов на карте" \
			"\n\t--check 		: проверить базу данных" \
			"\n\t--alias Alias Name	: добавить алиас для юнита/карты" \
			"\n\t--print			: показать данные" \
			""
	else:
		print "\nпараметр не распознан"

