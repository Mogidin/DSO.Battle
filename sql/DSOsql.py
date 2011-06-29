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
#	if not len(params) == 7:
#		print "\n параметры: HP, MinDmg, MaxDmg, Accuracy, Initiative [F-Fast, N-Normal, S-Slow], Courage, Skills [H-HeadHunter, S-SplashDamage, T-TurmBonus, N-None]"
#		sys.exit(1)
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
	if type == "All":
		PrintData("Unit", [])
		PrintData("MapUnit", [])
		PrintData("Alias", [])
	elif type == "Unit":
		ConnectOpen()
		print "\nUnit list:"
		sql = "SELECT name FROM Units ORDER BY name"
		cursor.execute(sql)
		for unit in cursor.fetchall():
			print "\t%s" % unit[0]
		ConnectClose()
	elif type == "Map":
		ConnectOpen()
                print "\nMap list:"
                sql = "SELECT name FROM Maps ORDER BY name"
                cursor.execute(sql)
                for map in cursor.fetchall():
                        print "\t%s" % map[0]
		ConnectClose()
	elif type == "MapUnit":
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
	elif type == "Alias":
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
	parser = argparse.ArgumentParser()
	parser.add_argument('name', nargs='*', metavar=('"Name unit or map"'), default=None)
	parser.add_argument('--image', '-i', nargs=1, metavar=('Image'), dest='UnitImage')
	parser.add_argument('--setunitinfo', '-sui', nargs=7, metavar=('HP', 'MinDmg', 'MaxDmg', 'Acuracy', 'Initiative', 'Courage', 'Skills'), dest='UnitInfo')
# HP, MinDmg, MaxDmg, Accuracy, Initiative [F-Fast, N-Normal, S-Slow], Courage, Skills [H-HeadHunter, S-SplashDamage, T-TurmBonus, N-None]"
	parser.add_argument('--show', '-s', action='store_true')
	parser.add_argument('--mapunit', '-mu', nargs='+', dest='MapUnit')
	parser.add_argument('--check', '-c', action='store_true')
	parser.add_argument('--alias', '-a', nargs=2, metavar=('"Name unit or map"', 'Alias'))
	parser.add_argument('--print', '-p', choices=['All', 'Unit', 'Map', 'MapUnit', 'Alias'], dest='PrintType')
	parser.add_argument('--load', '-l', nargs=1, dest='Dir')

	args = parser.parse_known_args()[0]
	print args

	if args.UnitImage != None and args.name != None: # добавить картинку юнита
		InsertImage(args.name[0], args.UnitImage[0])
	if args.UnitInfo != None and args.name != None: # добавить информацию по юниту
		SetUnitInfo(args.name[0], args.UnitInfo)
	if args.show == True and args.name != None: # показать картинку юнита
		im = GetImage(args.name[0])
		if im != None:
			im.show()
	if args.Dir != None: # добавляем картинки юнитов из каталога
		dir = args.Dir
		if not os.path.exists(dir):
                        print "\nпуть не существует"
			sys.exit(1)
		files = os.listdir(dir)
		for ifile in files:
			fullname = os.path.join(dir, ifile)  # получаем полное имя
			if os.path.isfile(fullname):        # если это файл...
				name = os.path.splitext(os.path.basename(fullname))[0]
				InsertImage(name, fullname)
	if args.MapUnit != None and args.name != None: # задаём список юнитов на карте
		SetMapUnits(args.name[0], args.MapUnit)
	if args.check == True: # проверяем базу данных
		CheckDB()
	if args.PrintType != None: # показать данные
		PrintData(args.PrintType, args.name)
        if args.alias != None and args.name != None: # задать алиас
		SetAlias(args.alias, args.name)

	sys.exit(0)
