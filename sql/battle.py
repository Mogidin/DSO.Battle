#!/usr/bin/env python2.6
# -*- coding: UTF-8 -*-

import sqlite3
import sys, os
import copy, random

InitiativeType=("F", "N", "S")

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
		

class Unit:
	def __init__(self, name, db):
		sql = "SELECT HP, MinDmg, MaxDmg, Accuracy, Initiative, Courage, Skills FROM Units WHERE name=?"
		db.cursor.execute(sql, [name])
		f = db.cursor.fetchone()
		self.name 	= name
		self.HP 	= f[0]
		self.MinDmg 	= f[1]
		self.MaxDmg 	= f[2]
		self.Accuracy 	= f[3]
		self.Initiative = f[4]
		self.Courage 	= f[5]
		self.Skills 	= f[6]

	def __str__(self):
		return "%s\t[HP: %d; Dmg: %d-%d; Accuracy: %d%%; Initiative: %s; Courage: %d; Skills: %s]" \
			% (self.name, self.HP, self.MinDmg, self.MaxDmg, self.Accuracy, self.Initiative, self.Courage, self.Skills)

	def __repr__(self):
		return self.name

	def GetEnemy(self, army):
		ind = -1
		if "H" in self.Skills: # HeadHunter, ищем минимальный HP
			ind = army.GetMinHP()
		else: # ищем максимальный Courage
			ind = army.GetMaxCourage()
		return ind

class UnitStack:
	def __init__(self, name, count, db):
		self.Unit = Unit(name, db)
		self.Count = count
		self.LastHP = self.Unit.HP

	def __str__(self):
		return "{0}, {1}".format(self.Unit.name, self.Count)

	def __repr__(self):
		return self.Unit.name


class Army:
	def __init__(self, units, db):
		# units : ((unitname, count), ....)
		self.UnitList = []
		# ul : ((unit, count, hp_last), ...)
		for unit in units:
			self.UnitList.append(UnitStack(unit[0], unit[1], db))

	def __str__(self):
		str = "Army\n"
		for us in self.UnitList:
			str += "\t{0}\n".format(us)
		return str
#		return "{0}".format(self.UnitList)

	def __getitem__(self, key):
		return self.UnitList[key]

	def GetMaxCourage(self):
		ind = -1
		courage = 0
		for i in range(len(self.UnitList)):
			ccourage = self.UnitList[i].Unit.Courage
			ccount = self.UnitList[i].Count
			if ccourage > courage and ccount > 0:
				courage = ccourage
				ind = i
		return ind

	def GetMinHP(self):
		ind = -1
		hp = 999999
		for i in range(len(self.UnitList)):
			chp = self.UnitList[i].Unit.HP
			ccount = self.UnitList[i].Count
			if chp < hp and ccount > 0:
				hp = chp
				ind = i
		return ind

	def GetByInitiative(self, InType):
		ul = []
		for i in range(len(self.UnitList)):
			cInType = self.UnitList[i].Unit.Initiative
			count = self.UnitList[i].Count
			if cInType == InType and count > 0:
				ul.append(i)
		return ul

	def GetCount(self):
		count = 0
		for unit in self.UnitList:
			count += unit.Count
		return count

class Battle:
	def __init__(self, Army1, Army2):
		self.Army1 = Army1
		self.Army2 = Army2
	def Round(self):
		for InType in InitiativeType: # для каждого типа инициативы
			tmp_a1 = copy.deepcopy(self.Army1)
			tmp_a2 = copy.deepcopy(self.Army2)
			print "# step %s" % InType
			# ходит армия 1
			ul1 = tmp_a1.GetByInitiative(InType)
			for i in ul1:
				us = tmp_a1[i]
				acc = us.Unit.Accuracy
				enemy = us.Unit.GetEnemy(self.Army2)
				if enemy == -1:
					break
				eus = self.Army2[enemy]
				# драча
				#ad = id = 0
				for c in range(us.Count):
					if random.randrange(101) > acc:
						dmg = us.Unit.MinDmg
						#id += 1
					else:
						dmg = us.Unit.MaxDmg
						#ad += 1
					#print "# %s damage %d" % (us.Unit.name, dmg)
					if "S" in us.Unit.Skills: # SplashDamage
						while dmg > 0:
							if dmg >= eus.LastHP:
								dmg -= eus.LastHP
								#print "%s left %d" % (eus.Unit.name, 0)
								eus.Count -= 1
								if eus.Count == 0:
									eus.LastHP = 0
									enemy = us.Unit.GetEnemy(self.Army2)
									if enemy == -1:
										break
									eus = self.Army2[enemy]
								eus.LastHP = eus.Unit.HP
							else:
								eus.LastHP -= dmg
								#print "%s left %d" % (eus.Unit.name, eus.LastHP)
								dmg = 0
					else:
						eus.LastHP -= dmg
						#print "%s left %d" % (eus.Unit.name, eus.LastHP)
						if eus.LastHP <= 0:
							eus.Count -= 1
							if eus.Count == 0:
								eus.LastHP = 0
								enemy = us.Unit.GetEnemy(self.Army2)
								if enemy == -1:
									break
								eus = self.Army2[enemy]
							eus.LastHP = eus.Unit.HP
				#end for c in range(us.Count):
				#print "min %d max %d" % (id, ad)
			#end for i in ul1:
			#print "# 1"
			#print self.Army1
			#print tmp_a1
			#print self.Army2
			#print tmp_a2

			# ходит армия 2
			ul2 = tmp_a2.GetByInitiative(InType)
			for i in ul2:
				us = tmp_a2[i]
				acc = us.Unit.Accuracy
				enemy = us.Unit.GetEnemy(self.Army1)
				if enemy == -1:
					break
				eus = self.Army1[enemy]
				# драча
				#ad = id = 0
				for c in range(us.Count):
					if random.randrange(101) > acc:
						dmg = us.Unit.MinDmg
						#id += 1
					else:
						dmg = us.Unit.MaxDmg
						#ad += 1
					#print "# %s damage %d" % (us.Unit.name, dmg)
					if "S" in us.Unit.Skills: # SplashDamage
						while dmg > 0:
							if dmg >= eus.LastHP:
								dmg -= eus.LastHP
								#print "%s left %d" % (eus.Unit.name, 0)
								eus.Count -= 1
								if eus.Count == 0:
									eus.LastHP = 0
									enemy = us.Unit.GetEnemy(self.Army1)
									if enemy == -1:
										break
									eus = self.Army1[enemy]
								eus.LastHP = eus.Unit.HP
							else:
								eus.LastHP -= dmg
								#print "%s left %d" % (eus.Unit.name, eus.LastHP)
								dmg = 0
					else:
						eus.LastHP -= dmg
						#print "%s left %d" % (eus.Unit.name, eus.LastHP)
						if eus.LastHP <= 0:
							eus.Count -= 1
							if eus.Count == 0:
								eus.LastHP = 0
								enemy = us.Unit.GetEnemy(self.Army1)
								if enemy == -1:
									break
								eus = self.Army1[enemy]
							eus.LastHP = eus.Unit.HP
				#end for c in range(us.Count):
				#print "min %d max %d" % (id, ad)
			#end for i in ul2:
			#print "# 2"
			print self.Army1
			#print tmp_a1
			print self.Army2
			#print tmp_a2

		#end for InType in InitiativeType:
		#self.Army1 = copy.copy(tmp_a1)
		#self.Army2 = copy.copy(tmp_a2)


if __name__ == "__main__":
	random.seed()


	db = DBClass("DSO.Battle.db3")
	db.Connect()
	
#	a1 = Army([("Raufbold", 74), ("Einäugiger Bert", 1)], db)
#	a2 = Army([("Rekrut", 70), ("Langbogenschütze", 130), ("General", 1)], db)
	
	a1 = Army([("Maat", 100)], db)
	a2 = Army([("Soldat", 200), ("General", 1)], db)

	b = Battle(a1, a2)


	while a1.GetCount() != 0 and a2.GetCount() != 0:
		b.Round()

		#print a1
		#print a2

	db.Close()


