# -*- coding: UTF-8 -*-

ImgDir = "img/" # каталог с изображениями

MarkTxt = "Mark" # метка границы
Mark = ImgDir+"mark.png" # картинка разделитель ("граница")
Back = ImgDir+"back.png" # подложка

# юниты на картах
Karte = {
	"Spieler"			:("Rekruten", "Bogenschutzen", "Miliz", "Reiterei", "Langbogenschutzen", "Soldaten", "Armbrustschutze", "Elitesoldat", "Kanonier"), \
	"Die Insel der Freibeuter"	:("Deckschrubber", "Pistolenschutzen", "Krahenfuse", "Sabelrassler", "Messerwerfer", "Maat", "VerruckterSmutje"), \
	"Kopfgeldjäger"			:"", \
	"Alte Bekannte"			:("Kultist", "DunklePriester", "Schattenschleicher", "Feuertanzer", "DunklerHohepriester", "TanzenderDerwisch", "Sumpfhexe"), \
	"Mutterliebe"			:("Pistolenschutzen", "Krahenfuse", "Maat", "Wolf", "DieWildeWaltraud", "VerruckterSmutje"), \
	"Sumpfhexe"			:"", \
	"Verräter"			:("DesertierteMiliz", "DesertierterLangbogenschutzen", "DesertierteReiterei", "DesertierterSoldat", "SirRobin", "DickeBertha"), \
	"Die Schwarzen Priester"	:"", \
	"Sattelfest"			:("Nomade","Lanzenreiter","BerittenerBogenschütze","Kompositbogenschütze","Kataphrakt","BeritteneAmazone","BrüllenderStier"), \
	"Räuberbande"			:"", \
	"Beutelschneider"		:"", \
	"Die Nordmänner"		:("Walkure", "Karl", "Thrall", "Huskarl", "Berserker", "Jomswikinger"), \
	"Die Dunkle Bruderschaft"	:"", \
	"Die Schwarzen Ritter"		:"", \
	"Viktor der Verschlagene"	:("Plunderer", "Schlager", "Wachhund", "Waldlaufer", "Raufbold", "EinaugigerBert", "Stinktier", "Metallgebiss", "DieWildeWaltraud", "Wolf"), \
	"Söhne der Steppe"		:"", \
	"Einsame Experimente"		:""
}

# иконки юнитов
Unit = {
	# Spieler
	"Rekruten"		:ImgDir+"Rekruten.png", \
	"Bogenschutzen"		:ImgDir+"Bogenschützen.png", \
	"Miliz"			:ImgDir+"Miliz.png", \
	"Reiterei"		:ImgDir+"Reiterei.png", \
	"Langbogenschutzen"	:ImgDir+"Langbogenschützen.png", \
	"Soldaten"		:ImgDir+"Soldaten.png", \
	"Armbrustschutze"	:ImgDir+"Armbrustschütze.png", \
	"Elitesoldat"		:ImgDir+"Elitesoldat.png", \
	"Kanonier"		:ImgDir+"Kanonier.png", \
	# Räuber
	"Plunderer"		:ImgDir+"Plünderer.png", \
	"Steinwerfer"		:ImgDir+"Steinwerfer.png", \
	"Schlager"		:ImgDir+"Schläger.png", \
	"Wachhund"		:ImgDir+"Wachhund.png", \
	"Waldlaufer"		:ImgDir+"Waldläufer.png", \
	"Raufbold"		:ImgDir+"Raufbold.png", \
	"EinaugigerBert"	:ImgDir+"EinäugigerBert.png", \
	"Stinktier"		:ImgDir+"Stinktier.png", \
	"Chuck"			:ImgDir+"Chuck.png", \
	"Metallgebiss"		:ImgDir+"Metallgebiss.png", \
	"DieWildeWaltraud"	:ImgDir+"DieWildeWaltraud.png", \
	# ведьма
	"Kultist"		:ImgDir+"Kultist.png", \
	"DunklePriester"	:ImgDir+"DunklerPriester.png", \
	"Schattenschleicher"	:ImgDir+"Schattenschleicher.png", \
	"Feuertanzer"		:ImgDir+"Feuertänzer.png", \
	"DunklerHohepriester"	:ImgDir+"DunklerHohepriester.png", \
	"TanzenderDerwisch"	:ImgDir+"TanzenderDerwisch.png", \
	"Sumpfhexe"		:ImgDir+"Sumpfhexe.png", \
	# пираты
	"Deckschrubber"		:ImgDir+"Deckschrubber.png", \
	"Pistolenschutze"	:ImgDir+"Pistolenschütze.png", \
	"Krahenfuse"		:ImgDir+"Krähenfüße.png", \
	"Messerwerfer"		:ImgDir+"Messerwerfer.png", \
	"Sabelrassler"		:ImgDir+"Säbelrassler.png", \
	"Maat"			:ImgDir+"Maat.png", \
	"VerruckterSmutje"	:ImgDir+"VerrückterSmutje.png", \
#	"BrullenderStier"	:ImgDir+"BrüllenderStier.png", \
	# ботельшнайдер
	"DickeBertha"		:ImgDir+"DickeBertha.png", \
	"SirRobin"		:ImgDir+"SirRobin.png", \
	"Wolf"			:ImgDir+"Wolf.png", \
	# викинги
	"Walkure"		:ImgDir+"Walküre.png", \
	"Karl"			:ImgDir+"Karl.png", \
	"Thrall"		:ImgDir+"Thrall.png", \
	"Huskarl"		:ImgDir+"Huskarl.png", \
	"Berserker"		:ImgDir+"Berserker.png", \
	"Jomswikinger"		:ImgDir+"Jomswikinger.png", \
	# Sattelfest
	"BeritteneAmazone"	:ImgDir+"BeritteneAmazone.png", \
        "BerittenerBogenschutze":ImgDir+"BerittenerBogenschütze.png", \
        "BrullenderStier"	:ImgDir+"BrüllenderStier.png", \
        "Kataphrakt"		:ImgDir+"Kataphrakt.png", \
        "Kompositbogenschutze"	:ImgDir+"Kompositbogenschütze.png", \
        "Lanzenreiter"		:ImgDir+"Lanzenreiter.png", \
        "Nomade"		:ImgDir+"Nomade.png", \
}

