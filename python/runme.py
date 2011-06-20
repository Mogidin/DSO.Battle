# -*- coding: UTF-8 -*-

import sys
import os
import sqlite3
import Image, ImageDraw, ImageFont
import DSOsql

MarkTxt="Mark"

(baseX, baseY) = (60, 90) # размер картинки юнита
(markX, markY) = (12, 90) # размер картинки границы

FONT = "font.ttf"
font = ImageFont.truetype(FONT, 12)

NumArg = len(sys.argv)
l = (NumArg - 1) / 3 # количество юнитов

MarkPresent = MarkTxt in sys.argv 

res = Image.new("RGB", (l*baseX+MarkPresent*markX, baseY)) # формируемая картинка

MarkPrint = 0
for i in range (l+MarkPresent): # l=2 > range=[0, 1]
	if sys.argv[1+i*3] == MarkTxt:
		# приклеиваем границу
#		print "есть граница"
		im = DSOsql.GetImage("mark")
		res.paste(im,(i*baseX, 0))
		MarkPrint = 1
	else:
		Unit     = sys.argv[1+(i-MarkPrint)*3+MarkPrint]
		EndNum   = sys.argv[2+(i-MarkPrint)*3+MarkPrint]
		StartNum = sys.argv[3+(i-MarkPrint)*3+MarkPrint]
		# пишем текст на подложке
#		print "%s - %s / %s" % (Unit, EndNum, StartNum)
		back = DSOsql.GetImage("back")
		draw = ImageDraw.Draw(back)
		draw.setfont(font)
		str = "%s/%s" % (EndNum, StartNum)
		(xs, ys) = font.getsize(str)
		draw.text((30 - xs/2, 70), str)
		# и приклеиваем
		im = DSOsql.GetImage(Unit)

		res.paste(back,((i-MarkPrint)*baseX+(MarkPrint*markX), 0))
		res.paste(im,((i-MarkPrint)*baseX+(MarkPrint*markX)+2, 2))

res.save("out.png")

