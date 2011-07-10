#!/usr/bin/env python2.6
# -*- coding: UTF-8 -*-

import sqlite3
import sys, os
import Image, ImageFile
import argparse

class DBClass:
	def __init__(self, filename):
		self.file = filename
	def Connect(self):
		self.connection = sqlite3.connect(self.file)
		self.connection.text_factory = str
		self.cursor = self.connection.cursor()
	def Commit(self):
	        self.connection.commit()
	def Close(self):
		self.connection.close()
		

def UnAlias(db, alias):
	sql = "SELECT name FROM Alias WHERE alias=?"
	db.cursor.execute(sql, [alias])
        item = db.cursor.fetchone()
        if not item == None:
		name = item[0]
	else:
		name = alias
	return name

def InsertImage(db, name, Fname):
	name = UnAlias(db, name)
	f = file(Fname, "rb")
	data = f.read()
	f.close()
	# проверяем существование элемента в базе
	sql = "SELECT name FROM Units WHERE name=?"
	db.cursor.execute(sql, [name])
        item = db.cursor.fetchone()
        if not item == None:
		if args.replace:
			sql = "UPDATE Units SET img=? WHERE name=?"
		else:
			print "\n такой элемент уже существует"
			sys.exit(1)
	else:
		sql = "INSERT INTO Units (img, name) VALUES (?,?)"
	db.cursor.execute(sql, (sqlite3.Binary(data), name) )

def GetImage(db, name):
	name = UnAlias(db, name)
	sql = "SELECT img FROM Units WHERE name=?"
	db.cursor.execute(sql, [name])
	item = db.cursor.fetchone()
	if item == None:
		return
	data = item[0]
	p = ImageFile.Parser()
	p.feed(data)
	return p.close()

def SetMapUnits(db, map, units):
        # проверяем существование элемента в базе
        sql = "SELECT name FROM Maps WHERE name=?"
        db.cursor.execute(sql, [map])
        item = db.cursor.fetchone()
        if item == None: # добавляем карту
		sql = "INSERT INTO Maps (name) VALUES (?)"
		db.cursor.execute(sql, [map])
	sqlS = "SELECT map, unit FROM MapUnit WHERE map=? AND unit=?"
	sqlA = "INSERT INTO MapUnit (map, unit) VALUES (?, ?)"
	for unit in units:
		db.cursor.execute(sqlS, (map, unit))
		item = db.cursor.fetchone()
	        if item == None:
        	        db.cursor.execute(sqlA, (map, unit))

def SetUnitInfo(db, unit, params):
	unit = UnAlias(db, unit)
#	if not len(params) == 7:
#		print "\n параметры: HP, MinDmg, MaxDmg, Accuracy, Initiative [F-Fast, N-Normal, S-Slow], Courage, Skills [H-HeadHunter, S-SplashDamage, T-TurmBonus, N-None]"
#		sys.exit(1)
	params.append(unit)
        # проверяем существование элемента в базе
        sql = "SELECT name FROM Units WHERE name=?"
        db.cursor.execute(sql, [unit])
        item = db.cursor.fetchone()
        if not item == None:
		if args.replace:
			sql = "UPDATE Units SET HP=?,MinDmg=?,MaxDmg=?,Accuracy=?,Initiative=?,Courage=?,Skills=? WHERE name=?"
		else:
			print "\n такой элемент уже существует"
			sys.exit(1)
        else:
                sql = "INSERT INTO Units (HP, MinDmg, MaxDmg, Accuracy, Initiative, Courage, Skills, name) VALUES (?,?,?,?,?,?,?,?)"
        db.cursor.execute(sql, params)

def GetUnitInfo(db, unit):
	unit = UnAlias(db, unit)
        sql = "SELECT HP,MinDmg,MaxDmg,Accuracy,Initiative,Courage,Skills FROM Units WHERE name=?"
        db.cursor.execute(sql, [unit])
        item = db.cursor.fetchone()
        if not item == None:
		print "{7} # HP: {0}; MinDmg: {1}; MaxDmg: {2}; Accuracy: {3}; Initiative: {4}; Courage: {5}; Skills: {6};".format(item[0], item[1], item[2], item[3], item[4], item[5], item[6], unit)

def CheckDB(db):
	sqlM = "SELECT name FROM Maps"
	db.cursor.execute(sqlM)
	Maps=[]
	for map in db.cursor.fetchall():
		Maps.append(map[0])

        sqlU = "SELECT name FROM Units"
        db.cursor.execute(sqlU)
        Units=[]
        for unit in db.cursor.fetchall():
                Units.append(unit[0])

	sqlMUm = "SELECT DISTINCT map FROM MapUnit"
	db.cursor.execute(sqlMUm)
	MUmap=[]
	for map in db.cursor.fetchall():
                MUmap.append(map[0])

        sqlMUu = "SELECT DISTINCT unit FROM MapUnit"
        db.cursor.execute(sqlMUu)
        MUunit=[]
        for unit in db.cursor.fetchall():
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

def SetAlias(db, alias, name):
        # проверяем существование элемента в базе
        sql = "SELECT alias FROM Alias WHERE alias=?"
        db.cursor.execute(sql, [alias])
        item = db.cursor.fetchone()
        if not item == None:
		if args.replace:
			sql = "UPDATE Alias SET name=? WHERE alias=?"
		else:
			print "\n такой элемент уже существует"
			sys.exit(1)
        else:
                sql = "INSERT INTO Alias (name, alias) VALUES (?,?)"
	db.cursor.execute(sql, (name, alias))

def PrintData(db, type, params):
	if type == "All":
		PrintData(db, "Unit", [])
		PrintData(db, "MapUnit", [])
		PrintData(db, "Alias", [])
	elif type == "Unit":
		print "\nUnit list:"
		sql = "SELECT name FROM Units ORDER BY name"
		db.cursor.execute(sql)
		for unit in db.cursor.fetchall():
			print "\t%s" % unit[0]
	elif type == "Map":
                print "\nMap list:"
                sql = "SELECT name FROM Maps ORDER BY name"
                db.cursor.execute(sql)
                for map in db.cursor.fetchall():
                        print "\t%s" % map[0]
	elif type == "MapUnit":
		if len(params) > 0:
			maps = []
			for map in params:
				maps.append((map,))
		else:
			sql = "SELECT name FROM Maps ORDER BY name"
			db.cursor.execute(sql)
			maps = db.cursor.fetchall()

		print "\nMapUnit list:"
		sqlMU = "SELECT unit FROM MapUnit WHERE map=?"
		for map in maps:
			print "\t%s" % map[0]
			db.cursor.execute(sqlMU,[map[0]])
			units = db.cursor.fetchall()
			for unit in units:
				strA = ""
				if args.verbose:
					sqlA = "SELECT alias FROM Alias WHERE name=?"
					db.cursor.execute(sqlA, [unit[0]])
					item = db.cursor.fetchone()
					if item != None:
						strA = "(%s) " % item
				print "\t\t%s%s" % (strA, unit[0])
	elif type == "Alias":
                print "\nAlias list:"
                sql = "SELECT alias, name FROM Alias ORDER BY name"
                db.cursor.execute(sql)
                for alias in db.cursor.fetchall():
                        print "\t%s\t: %s" % (alias[0], alias[1])

if __name__ == "__main__":
#	reload(sys)
#	sys.setdefaultencoding("UTF-8")
	global args

	db = DBClass("DSO.Battle.db3")
	db.Connect()

	parser = argparse.ArgumentParser()
	parser.add_argument('name', nargs='*', metavar=('Name'), default=None)
	parser.add_argument('--image', '-i', nargs=1, metavar=('Image'), dest='UnitImage')
	parser.add_argument('--setunitinfo', '-sui', nargs=7, metavar=('HP', 'MinDmg', 'MaxDmg', 'Acuracy', 'Initiative', 'Courage', 'Skills'), dest='UnitInfo')
# HP, MinDmg, MaxDmg, Accuracy, Initiative [F-Fast, N-Normal, S-Slow], Courage, Skills [H-HeadHunter, S-SplashDamage, T-TurmBonus, N-None]"
	parser.add_argument('--getunitinfo', '-gui', action='store_true', dest='UnitInfo')
	parser.add_argument('--show', '-s', action='store_true')
	parser.add_argument('--mapunit', '-mu', nargs='+', dest='MapUnit')
	parser.add_argument('--check', '-c', action='store_true')
	parser.add_argument('--alias', '-a', nargs=1, metavar=('Alias'))
	parser.add_argument('--print', '-p', choices=['All', 'Unit', 'Map', 'MapUnit', 'Alias'], dest='PrintType')
	parser.add_argument('--load', '-l', nargs=1, dest='Dir')
	parser.add_argument('--replace', '-y', action='store_true')
	parser.add_argument('--verbose', '-v', action='store_true')

	args = parser.parse_known_args()[0]
#	print args

	if args.UnitImage != None and args.name != None: # добавить картинку юнита
		InsertImage(db, args.name[0], args.UnitImage[0])
		db.Commit()

	if args.UnitInfo == True and args.name != None: # показать информацию по юниту
		GetUnitInfo(db, args.name[0])
	elif args.UnitInfo != None and args.name != None: # добавить информацию по юниту
		SetUnitInfo(db, args.name[0], args.UnitInfo)
		db.Commit()

	if args.show == True and args.name != None: # показать картинку юнита
		im = GetImage(db, args.name[0])
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
				InsertImage(db, name, fullname)
		db.Commit()

	if args.MapUnit != None and args.name != None: # задаём список юнитов на карте
		SetMapUnits(db, args.name[0], args.MapUnit)
		db.Commit()

	if args.check == True: # проверяем базу данных
		CheckDB(db)

	if args.PrintType != None: # показать данные
		PrintData(db, args.PrintType, args.name)

        if args.alias != None and args.name != None: # задать алиас
		SetAlias(db, args.alias[0], args.name[0])
		db.Commit()

	db.Close()
	sys.exit(0)
