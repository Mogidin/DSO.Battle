#!/usr/bin/env python2.6
# -*- coding: UTF-8 -*-

import sqlite3
import sys, os

class Unit:
	def __init__(self, name):
		ConnectOpen()
		sql = "SELECT HP, MinDmg, MaxDmg, Accuracy, Initiative, Courage, Skills FROM Units WHERE name=?"
		cursor.execute(sql, [name])
		f = cursor.fetchone()
		self.name 	= name
		self.HP 	= f[0]
		self.MinDmg 	= f[1]
		self.MaxDmg 	= f[2]
		self.Accuracy 	= f[3]
		self.Initiative = f[4]
		self.Courage 	= f[5]
		self.Skills 	= f[6]
		ConnectClose()

	def __str__(self):
		return "%s\t[HP: %d; Dmg: %d-%d; Accuracy: %d%%; Initiative: %s; Courage: %d; Skills: %s]" \
			% (self.name, self.HP, self.MinDmg, self.MaxDmg, self.Accuracy, self.Initiative, self.Courage, self.Skills)

	def __repr__(self):
		return self.name

class Army:
	def __init__(self, units):
		# units : ((unitname, count), ....)
		ul = self.UnitList = []
		for unit in units:
			u = Unit(unit[0])
			ul.append((u, unit[1], u.HP))

	def __str__(self):
		return "{0}".format(self.UnitList)

	def __getitem__(self, key):
		return self.UnitList[key]

	def GetMaxCourage(self):
		ind = -1
		courage = 0
		for i in range(len(self.UnitList)):
			ccourage = self.UnitList[i][0].Courage
			ccount = self.UnitList[i][1]
			if ccourage > courage and ccount > 0:
				courage = ccourage
				ind = i
		return ind

	def GetMinHP(self):
		ind = -1
		hp = 999999
		for i in range(len(self.UnitList)):
			chp = self.UnitList[i][0].HP
			ccount = self.UnitList[i][1]
			if chp < hp and ccount > 0:
				hp = chp
				ind = i
		return ind

	def GetCount(self):
		count = 0
		for unit in self.UnitList:
			count += unit[1]
		return count

class Battle:
	def __init__(self, Army1, Army2):
		self.Army1 = Army1
		self.Army2 = Army2

def ConnectOpen():
	global connection
	global cursor

	connection = sqlite3.connect("DSO.Battle.db3")
	connection.text_factory = str
	cursor = connection.cursor()

def ConnectClose():
        connection.commit()
        connection.close()	



if __name__ == "__main__":
	a = Army([("Maat", 100), ("Messerwerfer", 50)])
	print a
	i = a.GetMinHP()
	if i>-1:
		print (a[i], a[i][0].HP)
	thp = 0
	for us in a.UnitList:
		thp += us[0].HP * us[1]
	print thp

