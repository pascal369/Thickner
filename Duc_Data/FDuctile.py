# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
import ParamFDuctile

doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
#JDPA A300
lst=('00_Flange Length Tube','01_Single Flange Length Tube','02_F3T-shaped Tube','03_F2T-shaped Tube',
'04_Flange Reducer','05_F90Elbow','06_F45Elbow','07_Gate_valve_Secondary Pipe B1','08_Flange Short Tube',
'09_Flange Lid','10_Manhole Cover','11_Trumpet Mouth','12_F Soft seal gate valve_internal thread','13_F Soft seal gate valve_external thread'
)

FC_type={
'00':'フランジ長管','01':'片フランジ長管','02': '三フランジT字管','03': '二フランジT字管','04':'フランジ片落管','05':'フランジ曲管_90',
'06':'フランジ曲管_45','07':'仕切弁副管B1号','08':'フランジ短管','09':'フランジふた','10':'人孔ふた','11':'らっぱ口','12':'F_ソフトシール仕切弁(内ねじ)','13':'F_ソフトシール仕切弁(外ねじ)'
}

#仕切弁-----------------------------------------------------------------------------------------------------------------------
gate=['075','100','150','200','250','300','350','400','450','500']

#直管-------------------------------------------------------------------------------------------------------------------------
strp=[
'075','100','150','200','250','300','350','400','450','500','600','700','800','900',
'1000','1100','1200','1350','1500'
]

#三フランジT字管-----------------------------------------------------------------------------------------------------------------
trct=[
'075x075','100x075','100x100','150x075','150x100','150x150',
'200x100','200x150','200x200','250x100','250x150','250x250','300x100',
'300x150','300x200','300x300','350x250','350x350','400x300','400x400',
'450x300','450x450','500x300','500x350','500x500','600x400','600x500',
'600x600','700x400','700x500','700x600','700x700','800x500','800x600',
'800x700','800x800','900x600','900x700','900x800','900x900','1000x600',
'1000x800','1000x1000','1100x600','1100x800','1100x1100','1200x600','1200x900',
'1200x1200','1350x600','1350x900','1350x1350','1500x600','1500x1000','1500x1500',
]
#二フランジT字管----------------------------------------------------------------------------------------------------
trct2=[
'075x075','100x075','100x100','150x075','150x100','150x150',
'200x100','200x150','200x200','250x100','250x150','250x250','300x100',
'300x150','300x200','300x300','350x250','350x350','400x300','400x400',
'450x300','450x450','500x300','500x350','500x500','600x400','600x500',
'600x600','700x400','700x500','700x600','700x700','800x500','800x600',
'800x700','800x800','900x600','900x700','900x800','900x900','1000x600',
'1000x800','1000x1000','1100x600','1100x800','1100x1100','1200x600','1200x900',
'1200x1200','1350x600','1350x900','1350x1350','1500x600','1500x1000','1500x1500',
]
#フランジ片落管--------------------------------------------------------------------------------------
trct3=[
'100x075','150x100','200x100','200x150','250x100','250x150',
'250x200','300x100','300x150','300x200','300x250','350x150','350x200',
'350x250','350x300','400x150','400x200','400x250','400x300','400x350','450x200',
'450x250','450x300','450x300','450x400','500x250','500x300','500x350','500x400',
'500x450','600x300','600x350','600x400','600x450','600x500','700x400','700x450','700x500',
'700x600','800x450','800x500','800x600','800x700','900x500','900x600','900x700','900x800',
'1200x800','1200x900','1200x1000','1200x1100','1350x900','1350x1000','1350x1100','1350x1200',
'1500x1000','1500x1100','1500x1200','1500x1350'
]

#仕切弁副管B1--------------------------------------------------------------------------------------------------------------------------
gvsp=[
'400x100','450x100','500x100','600x100','700x150','800x150','900x200','1000x200',
'1100x200','1200x250','1350x250','1500x300','1600x300','1650x300','1800x350','2000x350',
'2100x400','2200x400','2400x450','2600x500'
]

#仕切弁副管B2--------------------------------------------------------------------------------------------------------------------------
gvspB=[
'400x100','450x100','500x100','600x100','700x150','800x150','900x200','1000x200',
'1100x200','1200x250','1350x250','1500x300'
]
#フランジ短管--------------------------------------------------------------------------------------------------------------------------
flgt=['075x100','075x150','075x250','075x300','075x400','075x500','100x100','100x150','100x250','100x300','100x400','100x500',
'150x100','150x150','150x250','150x300','150x400']

#人孔ふた--------------------------------------------------------------------------------------------------------------------------
mhlc=['600x075','600x100','600x150','600x200']

#三フランジT字管---------------------------------------------------------
#          B,    I,      L
trcts={
'075x075':(160,  140,    320),
'100x075':(180,  160,    360),
'100x100':(180,  160,    360),
'150x075':(190,  190,    380),
'150x100':(190,  190,    380),
'150x150':(190,  190,    380),
'200x100':(200,  230,    400),
'200x150':(250,  250,    500),
'200x200':(250,  250,    500),
'250x100':(230,  250,    460),
'250x150':(230,  250,    460),
'250x250':(280,  260,    560),
'300x100':(240,  280,    480),
'300x150':(240,  280,    480),
'300x200':(330,  300,    660),
'300x300':(330,  300,    660),
'350x250':(360,  340,    720),
'350x350':(360,  340,    720),
'400x300':(410,  390,    820),
'400x400':(410,  390,    820),
'450x300':(440,  420,    880),
'450x450':(440,  420,    880),
'500x300':(480,  460,    960),
'500x350':(480,  460,    960),
'500x500':(480,  460,    960),
'600x400':(550,  530,    1100),
'600x500':(550,  530,    1100),
'600x600':(550,  530,    1100),
'700x400':(620,  600,    1240),
'700x500':(620,  600,    1240),
'700x600':(620,  600,    1240),
'700x700':(620,  600,    1240),
'800x500':(690,  670,    1380),
'800x600':(690,  670,    1380),
'800x700':(690,  670,    1380),
'800x800':(690,  670,    1380),
'900x600':(600,  690,    1200),
'900x700':(770,  750,    1540),
'900x800':(770,  750,    1540),
'900x900':(770,  750,    1540),
'1000x600':(680,  770,   1360),
'1000x800':(840,  820,   1680),
'1000x1000':(840, 820,   1680),
'1100x600':(650,  800,   1300),
'1100x800':(740,  830,   1480),
'1100x1100':(910, 890,   1820),
'1200x600':(680,  860,   1360),
'1200x900':(810,  910,   1620),
'1200x1200':(970, 950,   1940),
'1350x600':(700,  950,   1400),
'1350x900':(860, 1000,   1720),
'1200x600':(680,  860,   1360),
'1200x900':(810,  910,   1620),
'1200x1200':(970, 950,   1940),
'1350x600':(700,  950,   1400),
'1350x900':(860, 1000,   1720),
'1350x1350':(1080,1050,  2160),
'1500x600':(730,  1050,  1460),
'1500x1000':(920, 1100,  1840),
'1500x1500':(1180,1150,  2360),
}
#二フランジT字管-------------------------
#          B,    I,    J,    L
trcts2={
'075x075':(160,  140,    480,  640),
'100x075':(180,  160,    530,  710),
'100x100':(180,  160,    530,  710),
'150x075':(190,  190,    600,  790),
'150x100':(190,  190,    600,  790),
'150x150':(190,  190,    600,  790),
'200x100':(200,  230,    560,  760),
'200x150':(250,  250,    630,  880),
'200x200':(250,  250,    630,  880),
'250x100':(230,  250,    600,  830),
'250x150':(230,  250,    600,  830),
'250x250':(280,  260,    670,  950),
'300x100':(240,  280,    600,  840),
'300x150':(240,  280,    600,  840),
'300x200':(330,  300,    700, 1030),
'300x300':(330,  300,    700, 1030),
'350x250':(360,  340,    750, 1110),
'350x350':(360,  340,    750, 1110),
'400x300':(410,  390,    780, 1190),
'400x400':(410,  390,    780, 1190),
'450x300':(440,  420,    820, 1260),
'450x450':(440,  420,    820, 1260),
'500x300':(480,  460,    850, 1330),
'500x350':(480,  460,    850, 1330),
'500x500':(480,  460,    850, 1330),
'600x400':(550,  530,    920, 1470),
'600x500':(550,  530,    920, 1470),
'600x600':(550,  530,    920, 1470),
'700x400':(620,  600,    980, 1600),
'700x500':(620,  600,    980, 1600),
'700x600':(620,  600,    980, 1600),
'700x700':(620,  600,    980, 1600),
'800x500':(690,  670,    1030,1720),
'800x600':(690,  670,    1030,1720),
'800x700':(690,  670,    1030,1720),
'800x800':(690,  670,    1030,1720),
'900x600':(600,  690,     940,1540),
'900x700':(770,  750,    1090,1860),
'900x800':(770,  750,    1090,1860),
'900x900':(770,  750,    1090,1860),
'1000x600':(680,  770,    990,1670),
'1000x800':(840,  820,   1140,1980),
'1000x1000':(840, 820,  1140, 1980),
'1100x600':(650,  800,  1000, 1650),
'1100x800':(740,  830,  1050, 1790),
'1100x1100':(910, 890,  1200, 2110),
'1200x600':(680,  860,  1000, 1680),
'1200x900':(810,  910,  1100, 1910),
'1200x1200':(970, 950,  1250, 2220),
'1350x600':(700,  950,  1000, 1700),
'1350x900':(860,  1000, 1150, 2010),
'1350x1350':(1080,1050, 1350, 2430),
'1500x600':(730,  1050, 1000, 1730),
'1500x1000':(920, 1100, 1200, 2120),
'1500x1500':(1180,1150, 1400, 2580),
}

#フランジ片落ち管----------------------------
#          A,    E,    L
trcts3={
'100x075':(50,  50,   400),
'150x100':(55,  50,   405),
'200x100':(60,  50,   410),
'200x150':(60,  55,   415),
'250x100':(70,  50,   520),
'250x150':(70,  55,   525),
'250x200':(70,  60,   530),
'300x100':(80,  50,   530),
'300x150':(80,  55,   535),
'300x200':(80,  60,   540),
'300x250':(80,  70,   550),
'350x150':(80,  55,   535),
'350x200':(80,  60,   540),
'350x250':(80,  70,   550),
'350x300':(80,  80,   560),
'400x150':(90,  55,   645),
'400x200':(90,  60,   650),
'400x250':(90,  70,   660),
'400x300':(90,  80,   670),
'400x350':(90,  80,   670),
'450x200':(100, 60,   660),
'450x250':(100, 70,   670),
'450x300':(100, 80,   680),
'450x350':(100, 80,   680),
'450x400':(100, 90,   690),
'500x250':(110, 70,   680),
'500x300':(110, 80,   690),
'500x350':(110, 80,   690),
'500x400':(110, 90,   700),
'500x450':(110, 100,  710),
'600x300':(120, 80,   700),
'600x350':(120, 80,   700),
'600x400':(120, 90,   710),
'600x450':(120, 100,  720),
'600x500':(120, 110,  730),
'700x400':(130, 90,   920),
'700x450':(130, 100,  930),
'700x500':(130, 110,  940),
'700x600':(130, 120,  950),
'800x450':(140, 100,  940),
'800x500':(140, 110,  950),
'800x600':(140, 120,  960),
'800x700':(140, 130,  970),
'900x500':(150, 110,  960),
'900x600':(150, 120,  970),
'900x700':(150, 130,  980),
'900x800':(150, 140,  990),
'1000x600':(170, 120, 990),
'1000x700':(170, 130, 1000),
'1000x800':(170, 140, 1010),
'1000x900':(170, 150, 1020),
'1100x700':(180, 130, 1110),
'1100x800':(180, 140, 1120),
'1100x900':(180, 150, 1130),
'1100x1000':(180, 170,  1150),
'1200x800':(190, 140,  1130),
'1200x900':(190, 150,  1140),
'1200x1000':(190, 170,  1160),
'1200x1100':(190, 180,  1170),
'1350x900':(210, 150,  1160),
'1350x1000':(210, 170,  1180),
'1350x1100':(210, 180,  1190),
'1350x1200':(210, 190,  1200),
'1500x1000':(230, 170,  1200),
'1500x1100':(230, 180,  1210),
'1500x1200':(230, 190,  1220),
'1500x1350':(230, 210,  1240)
}
#曲管-------------------------------------------------
#       R,    L1,   deg
elbows_90={
'075':(  250,  297, 90),
'100':(  250,  297, 90),
'150':(  300,  348, 90),
'200':(  400,  449, 90),
'250':(  400,  450, 90),
'300':(  550,  607, 90),
'350':(  550,  608, 90),
'400':(  600,  659, 90),
'450':(  600,  660, 90),
'500':(  700,  761, 90),
'600':(  800,  862, 90),
'700':(  900,  963, 90),
'800':(  1000,  1115,  90),
'900':(  1100,  1225,  90),
'1000':(  1150,  1285,  90),
'1100':(  1200,  1345,  90),
'1200':(  1200,  1355,  90),
'1350':(  1200,  1370,  90),
'1500':(  1200,  1385,  90)
}
elbows_45={
'075':(  400,  213,  45),
'100':(  400,  213,  45),
'150':(  500,  255,  45),
'200':(  600,  298,  45),
'250':(  600,  298,  45),
'300':(  700,  347,  45),
'350':(  800,  389,  45),
'400':(  900,  432,  45),
'450':(  1000,  474,  45),
'500':(  1100,  517,  45),
'600':(  1300,  601,  45),
'700':(  1500,  730,  45),
'800':(  1700,  820,  45),
'900':(  1900,  915,  45),
'1000':(  2100,  1005,  45),
'1100':(  2300,  1100,  45),
'1200':(  2300,  1110,  45),
'1350':(  2300,  1125,  45),
'1500':(  2300,  1140,  45)
}

#フランジ------------------------------------------------------------------------------------
#          d0,   d2,     d3,   d4,   d5,   K,   m,   n,   L2',  L(定尺),  T,   T1,   D1,  L0,  h
flngs={
'075':(    75,     93,   125,  168,  211,  21,  3,   4,   26,   3000,     8.5, 11,  110,  80, 19),
'100':(   100,    118,   152,  195,  238,  21,  3,   4,   26,   3000,     8.5, 11,  150,  90, 19),
'150':(   150,    169,   204,  247,  290,  22,  3,   6,   26,   4000,     9.0, 12,  230, 106, 19),
'200':(   200,    220,   256,  299,  342,  23,  3,   8,   26,   4000,    11.0, 14,  300, 125, 19),
'250':(   250,  271.6,   308,  360,  410,  24,  3,   8,   26,   4000,    12.0, 15,  375, 145, 23),
'300':(   300,  322.8,   362,  414,  464,  25,  3,  10,   26,   4000,    12.5, 16,  450, 170, 23),
'350':(   350,  374.0,   414,  472,  530,  26,  3,  10,   32,   4000,    13.0, 16,  530, 190, 25),
'400':(   400,  425.6,   466,  524,  582,  27,  3,  12,   32,   4000,    14.0, 17,  600, 210, 25),
'450':(   450,  476.8,   518,  585,  652,  28,  3,  12,   32,   4000,    14.5, 18,  680, 240, 27),
'500':(   500,  528.0,   572,  639,  706,  29,  4,  12,   32,   4000,    15.0, 19,  750, 260, 27),
'600':(   600,  630.8,   676,  743,  810,  30,  4,  16,   32,   4000,    16.0, 20,  900, 310, 27),
'700':(   700,  733.0,   780,  854,  928,  31,  4,  16,   32,   4000,    17.0, 21, 1050, 340, 33),
'800':(   800,  836.0,   886,  960, 1034,  32,  4,  20,   68,   4000,    18.0, 22,  980, 380, 33),
'900':(   900,  939.0,   990, 1073, 1156,  33,  4,  20,   77,   4000,    19.0, 23, 1095, 415, 33),
'1000':( 1000, 1041.0,  1096, 1179, 1262,  34,  4,  24,   84,   4000,    20.0, 25, 1210, 450, 33),
'1100':( 1100, 1144.0,  1200, 1283, 1366,  36,  4,  24,   90,   4000,    21.0, 26, 1325, 485, 33),
'1200':( 1200, 1246.0,  1304, 1387, 1470,  38,  4,  28,   96,   4000,    22.0, 28, 1440, 520, 33),
'1350':( 1350, 1400.0,  1462, 1552, 1642,  40,  4,  28,  110,   4000,    24.0, 30, 1610, 570, 39),
'1500':( 1500, 1554.0,  1620, 1710, 1800,  42,  5,  32,  115,   4000,    26.0, 33, 1785, 625, 39),
'1600':( 1600, 1650.0,  1760, 1820, 1915,  47,  5,  36,  120,      0,    26.0, 33, 1785, 625, 39),
'1650':( 1650, 1701.0,  1810, 1870, 1965,  48,  5,  40,  120,      0,    26.0, 33, 1785, 625, 39),
'1800':( 1800, 1848.0,  1960, 2020, 2115,  49,  5,  44,  120,      0,    26.0, 33, 1785, 625, 39),
'2000':( 2000, 2061.0,  2170, 2230, 2325,  51,  5,  48,  125,      0,    26.0, 33, 1785, 625, 46),
'2100':( 2100, 2164.0,  2270, 2335, 2430,  52,  5,  48,  125,      0,    26.0, 33, 1785, 625, 46),
'2200':( 2200, 2280.0,  2370, 2440, 2550,  54,  6,  52,  130,      0,    26.0, 33, 1785, 625, 46),
'2400':( 2400, 2458.0,  2570, 2650, 2760,  56,  6,  56,  140,      0,    26.0, 33, 1785, 625, 46),
'2600':( 2600, 2684.0,  2780, 2850, 2960,  58,  6,  56,  140,      0,    26.0, 33, 1785, 625, 52),
}

#仕切弁副管-----------------------------------------------------------
#          R,    L1,    L2
gvsps={
'400x100':(200,  250,  340),
'450x100':(200,  250,  365),
'500x100':(200,  250,  390),
'600x100':(200,  250,  435),
'700x150':(200,  250,  475),
'800x150':(200,  250,  535),
'900x200':(250,  310,  590),
'1000x200':(250,  310,  635),
'1100x200':(250,  310,  670),
'1200x250':(250,  310,  680),
'1350x250':(250,  310,  725),
'1500x300':(250,  310,  780),

'1600x300':(250,  310,  790),
'1650x300':(250,  310,  790),
'1800x350':(300,  370,  815),
'2000x350':(300,  370,  825),
'2100x400':(300,  370,  835),
'2200x400':(300,  370,  845),
'2400x450':(350,  420,  870),
'2600x500':(335,  420,  895),
}

#フランジ短管-----------------------------------------------------------
#          L
flgts={
'075x100':(100,0),
'075x150':(150,0),
'075x250':(250,0),
'075x300':(300,0),
'075x400':(400,0),
'075x500':(500,0),
'100x100':(100,0),
'100x150':(150,0),
'100x250':(250,0),
'100x300':(300,0),
'100x400':(400,0),
'100x500':(500,0),
'150x100':(100,0),
'150x150':(150,0),
'150x250':(250,0),
'150x400':(400,0)
}

#フランジふた------------------------------------------------
#        R1,   R2,    T,     K,    M
tnkns={
'075':(    0,    0,   18.0,  21,   3),
'100':(    0,    0,   18.0,  21,   3),
'150':(  150,  250,    9.0,  22,   3),
'200':(  200,  300,   11.0,  23,   3),
'250':(  250,  350,   12.0,  24,   3),
'300':(  300,  400,   12.5,  25,   3),
'350':(  350,  450,   13.0,  26,   3),
'400':(  400,  500,   14.0,  27,   3),
'450':(  450,  550,   14.5,  28,   3),
'500':(  500,  600,   15.0,  30,   4),
'600':(  600,  700,   17.0,  32,   4),
'700':(  700,  800,   19.0,  34,   4),
'800':(  800,  900,   22.0,  36,   4),
'900':(  900, 1000,   24.0,  38,   4),
'1000':( 1000,1100,   27.0,  40,   4),
'1100':( 1100,1200,   29.0,  42,   4),
'1200':( 1200,1300,   32.0,  44,   4),
'1350':( 1350,1450,   35.0,  48,   4),
'1500':( 1500,1600,   39.0,  50,   5)
}

#仕切弁------------------------------------------------
#         L,   H(内), H(外), w(ハンドル車)
gates={
'075':(  240,  330,   570,  224),
'100':(  250,  365,   670,  250),
'150':(  280,  455,   920,  300),
'200':(  300,  540,  1120,  355),
'250':(  380,  640,  1380,  400),
'300':(  400,  740,  1590,  450),
'350':(  430, 1110,  1800,  500),
'400':(  470, 1240,  1990,  560),
'450':(  500, 1350,  2210,  630),
'500':(  530, 1450,  2360,  710)
}

#人孔蓋-----------------------------------------------------------
#          H,     L
mhlcs={
'600x075':(81.5,  240),
'600x100':(81.5,  240),
'600x150':(81.5,  240),
'600x200':(81.5,  240)
}


class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self        

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(330, 350)
        Dialog.move(900, 0)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 60, 12))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(90, 10, 220, 22))
        self.comboBox.setObjectName("comboBox")
        self.lineEdit_1 = QtGui.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(90, 40, 50, 15))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label_5.setObjectName("label_5")
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 65, 90, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(190, 65, 75, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_1 = QtGui.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(150, 95, 115, 20))
        self.pushButton_1.setObjectName("pushButton_1")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(150, 40, 170, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 95, 65, 12))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(15, 125, 300, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "img","img_00.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(90, 95, 50, 15))
        self.lineEdit.setObjectName("lineEdit")
        self.retranslateUi(Dialog)
        self.comboBox.addItems(lst)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.on_lst)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_2.currentIndexChanged[int].connect(self.on_lst2)
        self.comboBox_2.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.fc_create)
        QtCore.QObject.connect(self.pushButton_1, QtCore.SIGNAL("pressed()"), self.license)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        try:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "F_type JDPA A300 v1.0", None, QtGui.QApplication.UnicodeUTF8))
            self.label.setText(QtGui.QApplication.translate("Dialog", "F形異形管", None, QtGui.QApplication.UnicodeUTF8))
            self.label_2.setText(QtGui.QApplication.translate("Dialog", "呼び径", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "ライセンスキーを記憶", None, QtGui.QApplication.UnicodeUTF8))
            self.label_3.setText(QtGui.QApplication.translate("Dialog", "", None, QtGui.QApplication.UnicodeUTF8))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "License_Key", None, QtGui.QApplication.UnicodeUTF8))
            self.label_5.setText(QtGui.QApplication.translate("Dialog", "切管長[mm]", None, QtGui.QApplication.UnicodeUTF8))
            #self.label_6.setText(QtGui.QApplication.translate("Dialog", "", None, QtGui.QApplication.UnicodeUTF8))
            self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", "", None, QtGui.QApplication.UnicodeUTF8))
            self.lineEdit.setText(QtGui.QApplication.translate("Dialog", "", None, QtGui.QApplication.UnicodeUTF8))
        except:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "F_type JDPA A300 v1.0"))
            self.label.setText(QtGui.QApplication.translate("Dialog", "F形異形管", None))
            self.label_2.setText(QtGui.QApplication.translate("Dialog", "呼び径", None))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "ライセンスキーを記憶", None))
            self.label_3.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "License_Key", None))
            self.label_5.setText(QtGui.QApplication.translate("Dialog", "切管長[mm]", None))
            #self.label_6.setText(QtGui.QApplication.translate("Dialog", "", None, QtGui.QApplication.UnicodeUTF8))
            self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.lineEdit.setText(QtGui.QApplication.translate("Dialog", "36C6", None))

    def on_lst2(self):
        if key=='00' or key=='01' :
            try:
                ta=strp
                a=self.comboBox_2.currentText()
                key_1=a
                sa=flngs[key_1]
                L=sa[9]
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass
    def license(self):
        x = self.lineEdit.text()
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"img","d_license.txt")
        with open(joined_path, mode='w') as ff:
            ff.write(x)
            ff.close()

    def on_lst(self):
        global d0
        global d1
        global d2
        global d3
        global d4
        global d5
        global L0
        global L1
        global L2
        global Lc
        global P
        global L
        global x
        global y
        global z
        global c1
        global c2
        global c3
        global c4
        global c5
        global c6
        global k
        global m
        global n
        global LL2
        global lck
        global L
        global key
        global ta
        global key_1
        global key_2
        global sa
        global a
        global xlc
        global FC
        self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", "", None))
        key = self.comboBox.currentText()[:2]
        FC=FC_type[key]
        try:
            self.label_3.setText(QtGui.QApplication.translate("Dialog", FC, None, QtGui.QApplication.UnicodeUTF8))
        except:
            self.label_3.setText(QtGui.QApplication.translate("Dialog", FC, None))
        self.comboBox_2.clear()
        pic='img_f' + key + '.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "img",pic)
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        xcf='215398765132966H5226586915547'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"img","d_license.txt")
        ff= open(joined_path)
        data1 = ff.read()  # ファイル終端まで全て読んだデータを返す
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", str(data1), None))
        ff.close()
        if key=='00' or key=='01' or key=='11':#------------------------------------------
            ta=strp
            a=self.comboBox_2.currentText()
            key_1=a
        elif key=='02':#三フランジT字管-----------------------------------------------------------
            ta=trct
        elif key=='03':#二受T字管--------------------------------------------------------------
            ta=trct2
        elif key=='04' :#片落ち管--------------------------------------------------
            ta=trct3
        elif key=='05' or key=='06' :#曲管----------------------------------------------------
            ta=strp
        elif key=='07' :#仕切弁副管------------------------------------------------------------
            ta=gvsp
        elif key=='08':#フランジ短管-------------------------------------------------------------
            ta=flgt
        elif key=='09':#フランジ蓋---------------------------------------------------------------
            ta=strp
        elif key=='10':#人孔蓋---------------------------------------------------------------
            ta=mhlc
        elif key=='12' or key=='13':#仕切弁 ---------------------------------------------
            ta=gate
        #xlc=xcf[13:18]
        xlc='***'
        self.comboBox_2.addItems(ta)
        self.comboBox_2.setCurrentIndex(0)
        if key=='00':
            a=self.comboBox_2.currentText()
            key_1=a
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None))
            sa=flngs[key_1]
            L=sa[9]

    def fc_create(self):
        global d0
        global d1
        global d2
        global d3
        global d4
        global d5
        global L0
        global L1
        global L2
        global Lc
        global P
        global L
        global x
        global y
        global z
        global c1
        global c2
        global c3
        global c4
        global c5
        global c6
        global k
        global m
        global n
        global LL2
        global b
        try:
            self.label_3.setText(QtGui.QApplication.translate("Dialog", FC, None, QtGui.QApplication.UnicodeUTF8))
        except:
            self.label_3.setText(QtGui.QApplication.translate("Dialog", FC, None))
        lsky=self.lineEdit.text()
        #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
        if lsky!=xlc:

            if key > '04':
               lsk='ライセンスキーを入力してください。'
               try:
                   self.label_3.setText(QtGui.QApplication.translate("Dialog", lsk, None, QtGui.QApplication.UnicodeUTF8))
               except:
                   self.label_3.setText(QtGui.QApplication.translate("Dialog", lsk, None))
               return
        if key=='00' or key=='01' or key=='09' or key=='11' or key=='12' or key=='13':#-----------------------------------------------------------
            a=self.comboBox_2.currentText()
            key_1=a


        elif key=='02' or key=='03':#3F 2F T字管-------------------------------------------------------------------------
            a=self.comboBox_2.currentText()
            if a[3]=='x':
                key_1=a[0:3]
                key_2=a[4:]
            else:
                key_1=a[0:4]
                key_2=a[5:]
            #sa=rcvd[key_1]
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
        elif key=='04' or  key=='10':#片落管-------------------------------------------------------------------------------------------
            a=self.comboBox_2.currentText()
            if a[3]=='x':
                key_1=a[:3]
                key_2=a[4:]
            else:
                key_1=a[:4]
                key_2=a[5:]
        elif key=='05' or key=='06' :#90 45 曲管-------------------------------------------------------------------------
            a=self.comboBox_2.currentText()
            key_1=a
            #sa=rcvd[key_1]
        elif key=='07' :#------------------------------------------------------------------------------------------------
            a=self.comboBox_2.currentText()
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(a[3]), None, QtGui.QApplication.UnicodeUTF8))
            if a[3]=='x':
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(a[3]), None, QtGui.QApplication.UnicodeUTF8))
                key_1=a[:3]
                key_2=a[4:]
            else:
                key_1=a[:4]
                key_2=a[5:]

        elif key=='08' :#------------------------------------------------------------------------------------------------
            a=self.comboBox_2.currentText()
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(a), None, QtGui.QApplication.UnicodeUTF8))
            if a[3]=='x':
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(a[3]), None, QtGui.QApplication.UnicodeUTF8))
                key_1=a[:3]
                key_2=a[4:]
            else:
                key_1=a[:4]
                key_2=a[5:]

            #a=self.comboBox_2.currentText()
        def flng(self):#フランジ---------------------------------------------------------------------------------------------
            global d0
            global d2
            global d3
            global d4
            global d5
            global c2
            global c3
            global k
            global m
            global n
            global LL2
            global c01
            global L
            global c20
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            LL2=sa[8]
            L=sa[9]
            h=sa[14]
            p1=(0,0,d0)
            p2=(0,0,d3)
            p3=(m,0,d3)
            p4=(m,0,d5)
            p5=(m+k,0,d5)
            p6=(m+k,0,d0)
            plst=[p1,p2,p3,p4,p5,p6,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
            C=d4
            for i in range(n):
                k0=math.pi*2/n
                if i==0:
                    x=C*math.cos(k0/2)
                    y=C*math.sin(k0/2)
                    c20 = Part.makeCylinder(h/2,1.5*k,Base.Vector(0,x,y),Base.Vector(1,0,0))
                    #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(x), None, QtGui.QApplication.UnicodeUTF8))
                    #Part.show(c20)
                else:
                    ks=i*k0+k0/2
                    x=C*math.cos(ks)
                    y=C*math.sin(ks)
                    c20 = Part.makeCylinder(h/2,1.5*k,Base.Vector(0,x,y),Base.Vector(1,0,0))
                    #Part.show(c20)
                if i==0:
                    c01=c01.cut(c20)
                    #Part.show(c00)
                else:
                    c01=c01.cut(c20)
        def socket(self):#ソケット-----------------------------------------------------------------------------------------------
            global d00
            global d0
            global d1
            global d2
            global d3
            global d4
            global d5
            global L0
            global L1
            global L2
            global Lc
            global P
            global P0
            global L
            global x
            global y
            global z
            global c00
            global c1
            global c2
            global c3
            global c4
            global c51
            d0=float(sa[0])/2
            d1=float(sa[1])/2
            d2=float(sa[2])/2
            d3=float(sa[3])/2
            L1=sa[4]
            x=sa[5]
            P=sa[6]
            #P0=P
            L=sa[7]
            Lc=sa[8]
            y=(d3-d2)
            L0=(L1+x+2*y)
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d1)
            p3=Base.Vector(L1,0,d1)
            p4=Base.Vector(L1,0,d3)
            p5=Base.Vector(P,0,d3)
            p6=Base.Vector(L0,0,d2)
            p7=Base.Vector(L0,0,d0)
            p8=Base.Vector(P,0,d0)
            p9=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        if key=='00' or key=='01' :#---------------------------------------------------------------
            sa=flngs[key_1]
            flng(self)
            c1=c01
            k0=m+k
            L=self.lineEdit_1.text()
            if key=='00':#フランジ長管
                label ='Flange Length Tube'
            elif key=='01':#片フランジ長管
                label ='Single Flange Length Tube'
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)        
            obj.addProperty("App::PropertyString", "key",label).key=key
            obj.addProperty("App::PropertyString", "key_1",label).key_1=key_1
            obj.addProperty("App::PropertyString", "L",'Length').L=L
            #obj.addProperty("App::PropertyEnumeration", "a",label)
            #obj.a=strp

            ParamFDuctile.f_ductile(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()  
            return    
     
        elif key=='02' :#3フランジT字管
            b='F3T_shaped tube'
            label=b
            #print(b)
            sa1=trcts[a]
            B=sa1[0]
            I=sa1[1]
            L0=sa1[2]
            sa=flngs[key_1]
            flng(self)
            c1=c01
            d02=d2
            d00=d0
            k00=m+k
            sa=flngs[key_1]
            flng(self)
            c2=c01
            k0=m+k
            c2.Placement=App.Placement(App.Vector(L0,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            sa=flngs[key_2]
            flng(self)
            c3=c01
            c3.Placement=App.Placement(App.Vector(B,I,0),App.Rotation(App.Vector(0,0,1),-90))
            c1=c1.fuse(c3)
            c4 = Part.makeCylinder(d02,L0-2*k00,Base.Vector(k00,0,0),Base.Vector(1,0,0))
            c5 = Part.makeCylinder(d00,L0-2*k00,Base.Vector(k00,0,0),Base.Vector(1,0,0))
            c6 = Part.makeCylinder(d2,I-k0,Base.Vector(B,0,0),Base.Vector(0,1,0))
            c7 = Part.makeCylinder(d0,I-k0,Base.Vector(B,0,0),Base.Vector(0,1,0))
            c1=c1.fuse(c4)
            c1=c1.fuse(c6)
            c1=c1.cut(c7)
            c1=c1.cut(c5)
            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='03' :#2フランジT字管
            b='F2T_shaped tube'
            label=b
            sa1=trcts2[a]
            B=sa1[0]
            I=sa1[1]
            L0=sa1[3]
            sa=flngs[key_1]
            flng(self)
            c1=c01
            d02=d2
            d00=d0
            k00=m+k
            sa=flngs[key_2]
            flng(self)
            c3=c01
            k0=m+k
            c3.Placement=App.Placement(App.Vector(B,I,0),App.Rotation(App.Vector(0,0,1),-90))
            c1=c1.fuse(c3)
            c4 = Part.makeCylinder(d02,L0-k00,Base.Vector(k00,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c4)
            c5 = Part.makeCylinder(d00,L0-k00,Base.Vector(k00,0,0),Base.Vector(1,0,0))
            c6 = Part.makeCylinder(d2,I-k0,Base.Vector(B,0,0),Base.Vector(0,1,0))
            c7 = Part.makeCylinder(d0,I-k0,Base.Vector(B,0,0),Base.Vector(0,1,0))

            c1=c1.fuse(c6)
            c1=c1.cut(c7)
            c1=c1.cut(c5)

            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='04' :#フランジ片落管---------------------------------------------------------------
            b='Flange Reducer'
            label=b
            sa1=trcts3[a]
            A00=sa1[0]
            E=sa1[1]
            Lf=sa1[2]

            sa=flngs[key_1]
            flng(self)
            c1=c01
            d00=d0
            d02=d2
            k00=m+k
            sa=flngs[key_2]
            flng(self)
            c2=c01
            k0=m+k
            c2.Placement=App.Placement(App.Vector(Lf,0,0),App.Rotation(App.Vector(0,0,1),180))

            L0=Lf-(k00+k0)
            A0=A00-k0
            E0=E-k0

            p1=(0,0,d00)
            p2=(0,0,d02)
            p3=(A0,0,d02)
            p4=(L0-E0,0,d2)
            p5=(L0,0,d2)
            p6=(L0,0,d0)
            p7=(L0-E0,0,d0)
            p8=(A0,0,d00)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c3=wface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c3.Placement=App.Placement(App.Vector(k00,0,0),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c2)
            c1=c1.fuse(c3)

            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='05' or key=='06' :#曲管-----------------------------------------
            if key=='05':#90
                sa1=elbows_90[key_1]
                label='F90Elbow_'
            elif key=='06':#45
                sa1=elbows_45[key_1]
                label='F45Elbow_'

            R=sa1[0]
            L1=sa1[1]
            deg=sa1[2]
            s=float(deg)/2
            sa=flngs[key_1]

            flng(self)
            c1=c01
            k0=m+k
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
            c1.Placement=App.Placement(App.Vector(0,-L1,0),App.Rotation(App.Vector(0,0,1),90))
            flng(self)

            a0=k0
            L0=R-k0
            x=R-R*math.cos(math.radians(s))
            y=R*math.sin(math.radians(s))
            x1=R-R*math.cos(math.radians(2*s))
            x2=L1*math.cos(math.radians(90-2*s))
            y1=R*math.sin(math.radians(2*s))
            y2=y1-R*math.tan(math.radians(s))
            y3=R*math.tan(math.radians(s))-y
            y4=L1*math.sin(math.radians(90-2*s))
            p1=(0,-(L1-a0),0)
            p2=(0,-R*math.tan(math.radians(s)),0)
            p3=(x,-y3,0)
            p4=(x1,y2,0)
            p5=((L1-a0)*math.cos(math.radians(90-2*s)),(L1-a0)*math.sin(math.radians(90-2*s)),0)
            edge1=Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(R, Base.Vector(R,-R*math.tan(math.radians(s)),0), Base.Vector(0,0,1), 180-2*s, 180)
            edge3=Part.makeLine(p4,p5)
            aWire = Part.Wire([edge1,edge2,edge3])
            edge7 = Part.makeCircle(d2, Base.Vector(0,-(L1-a0),0), Base.Vector(0,1,0), 0, 360)
            edge8 = Part.makeCircle(d0, Base.Vector(0,-(L1-a0),0), Base.Vector(0,1,0), 0, 360)
            c11=c01
            c11.Placement=App.Placement(App.Vector((L1)*math.cos(math.radians(90-2*s)),(L1)*math.sin(math.radians(90-2*s)),0),App.Rotation(App.Vector(0,0,1),270-2*s))
            c1=c1.fuse(c11)
            profile = Part.Wire([edge7])
            profile1 = Part.Wire([edge8])
            makeSolid=True
            isFrenet=True
            c2 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c3 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
            c1=c1.fuse(c2)
            c1=c1.cut(c3)

            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
        elif key=='07' :#-----------------------------------------------------------------------------------
            sa1=gvsps[a]
            R=sa1[0]
            L1=sa1[1]
            L2=sa1[2]
            label='F_Gate Valve Secondary PipeB1_'
            sa=flngs[key_2]
            flng(self)
            c1=c01
            k0=m+k
            c1.Placement=App.Placement(App.Vector(0,-L1,0),App.Rotation(App.Vector(0,0,1),90))
            sa=flngs[key_2]
            flng(self)
            c2=c01
            c2.Placement=App.Placement(App.Vector(L2,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)

            L0=L1-(R+k0)
            L01=L2-(R+k0)

            p1=(0,-(R+L0),0)
            p2=(0,-R,0)
            p3=(R,0,0)
            p4=(R+L01,0,0)
            p5=(R,-R,0)
            edge1=Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(R, Base.Vector(R,-R,0), Base.Vector(0,0,1), 90, 180)
            edge3=Part.makeLine(p3,p4)
            edge4 = Part.makeCircle(d2, Base.Vector(0,-R,0), Base.Vector(0,1,0), 0, 360)
            edge5 = Part.makeCircle(d0, Base.Vector(0,-R,0), Base.Vector(0,1,0), 0, 360)
            aWire = Part.Wire([edge1,edge2,edge3])
            profile = Part.Wire([edge4])
            profile1 = Part.Wire([edge5])
            makeSolid=True
            isFrenet=True
            c3 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c4 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
            c3=c3.cut(c4)
            c1=c1.fuse(c3)
            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
        elif key=='08':#-----------------------------------------------------------------------------------
            sa1=flgts[a]
            L0=sa1[0]
            label='Flange Short Tube'
            sa=flngs[key_1]
            flng(self)
            c1=c01
            k0=m+k
            x=L0-2*k0
            c2 = Part.makeCylinder(d2,x,Base.Vector(k0,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,x,Base.Vector(k0,0,0),Base.Vector(1,0,0))
            c2=c2.cut(c3)
            sa=flngs[key_1]
            flng(self)
            c4=c01
            c4.Placement=App.Placement(App.Vector(L0,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            c1=c1.fuse(c4)
            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
        elif key=='09':#フランジ蓋-----------------------------------------------------
            sa=flngs[key_1]
            label='Flange Lid'
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            LL2=sa[8]
            L=sa[9]
            h=sa[14]

            p1=(0,0,0)
            p2=(0,0,d3)
            p3=(m,0,d3)
            p4=(m,0,d5)
            p5=(m+k,0,d5)
            p6=(m+k,0,0)
            plst=[p1,p2,p3,p4,p5,p6,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c1=pface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
            sa1=tnkns[a]
            R1=sa1[0]
            R2=sa1[1]
            T=sa1[2]
            k0=k+m
            R=R1+T
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            
            if key_1>='150':
                s=math.acos(d0/R)
                y=R*math.sin(s)
                c2 = Part.makeSphere(R)
                c22 = Part.makeSphere(R-T)
                c2.Placement=App.Placement(App.Vector(0,-y+T+k0,0),App.Rotation(App.Vector(0,1,0),0))
                c22.Placement=App.Placement(App.Vector(0,-y+k0,0),App.Rotation(App.Vector(0,1,0),0))
                c3 = Part.makeCylinder(1.1*R,2*R,Base.Vector(0,-2*R+k0,0),Base.Vector(0,1,0))
                c2=c2.cut(c3)
                c1=c1.fuse(c2)
                c1=c1.cut(c22)

            C=d4 
            
            for i in range(n):
                k0=math.pi*2/n
                if i==0:
                    x=C*math.cos(k0/2)
                    y=C*math.sin(k0/2)
                    c20 = Part.makeCylinder(h/2,1.5*k,Base.Vector(x,0,y),Base.Vector(0,1,0))
                    c1=c1.cut(c20)
                else:
                    ks=i*k0+k0/2
                    x=C*math.cos(ks)
                    y=C*math.sin(ks)
                    c20 = Part.makeCylinder(h/2,1.5*k,Base.Vector(x,0,y),Base.Vector(0,1,0))
                    c1=c1.cut(c20)
            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
        elif key=='10':#人孔蓋---------------------------------------------------

            sa=flngs[key_1]

            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            LL2=sa[8]
            L=sa[9]

            p1=(0,0,0)
            p2=(0,0,d3)
            p3=(m,0,d3)
            p4=(m,0,d5)
            p5=(m+k,0,d5)
            p6=(m+k,0,0)
            plst=[p1,p2,p3,p4,p5,p6,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c1=pface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
            sa1=mhlcs[a]
            H=sa1[0]
            L0=sa1[1]
            T=24
            k0=k+m
            R1=float(key_1)
            R=R1+T
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            s=math.acos(d0/R)
            y=R*math.sin(s)
            c2 = Part.makeSphere(R)
            c22 = Part.makeSphere(R-T)
            c2.Placement=App.Placement(App.Vector(0,-y+T+k0,0),App.Rotation(App.Vector(0,1,0),0))
            c22.Placement=App.Placement(App.Vector(0,-y+k0,0),App.Rotation(App.Vector(0,1,0),0))
            c3 = Part.makeCylinder(1.1*R,2*R,Base.Vector(0,-2*R+k0,0),Base.Vector(0,1,0))
            c2=c2.cut(c3)
            c1=c1.fuse(c2)

            sa=flngs[key_2]
            flng(self)
            c4=c01
            k1=m+k
            x=L0-k1
            c4.Placement=App.Placement(App.Vector(0,L0,0),App.Rotation(App.Vector(0,0,1),-90))
            c5 = Part.makeCylinder(d2,x,Base.Vector(0,0,0),Base.Vector(0,1,0))
            c6 = Part.makeCylinder(d0,x,Base.Vector(0,0,0),Base.Vector(0,1,0))
            c4=c4.fuse(c5)
            c1=c1.fuse(c4)
            c1=c1.cut(c22)
            c1=c1.cut(c6)

            label='Manhole Cover'

            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
        elif key=='11':#らっぱ口----------------------------------------------------------------
            sa=flngs[key_1]
            flng(self)
            c1=c01
            k0=m+k
            T=sa[10]
            T1=sa[11]
            D1=sa[12]
            L0=sa[13]
            R2=float(D1)/2
            r1=float(T1)/2
            R=R2-d0
            y2=L0-R

            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))

            p1=(d0,k0,0)
            p2=(d0,y2,0)
            p3=(R2,L0,0)
            p4=(R2,L0-T,0)
            p5=(d0+T,y2,0)
            p6=(d0+T,k0,0)
            p7=(R2,L0-R,0)

            edge1=Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(R, Base.Vector(R2,L0-R,0), Base.Vector(0,0,1), 90, 180)
            edge3=Part.makeLine(p3,p4)
            edge4 = Part.makeCircle(R-T, Base.Vector(R2,L0-R,0), Base.Vector(0,0,1), 90, 180)
            edge5=Part.makeLine(p5,p6)
            edge6=Part.makeLine(p6,p1)

            aWire = Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6])
            pface = Part.Face(aWire)
            c2=pface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0,1,0),360)
            c1=c1.fuse(c2)
            c3=Part.makeTorus(R2,r1,Base.Vector(0,L0-r1,0.0),Base.Vector(0,1,0),0,360)
            c1=c1.fuse(c3)
            label='Bell_mouth'
            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
        elif key=='12' or key=='13':#gate valve(Internal)---------------------------------------------------
            global M
            sa=flngs[key_1]
            M=sa[5]
            flng(self)
            c1=c01
            sa=flngs[key_1]
            flng(self)
            c2=c01
            sa1=gates[key_1]
            L1=sa1[0]
            L=sa1[0]
            H=sa1[1]
            L0=m+k
            c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)

            c3 = Part.makeCylinder(d2,L1-2*L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c3)

            x2=0.3

            if key_1<='150':
                x3=0.4
            elif key_1<='300':
                x3=0.425
            else:
                x3=0.5
            w0=x2*L
            h0=2*d2+20
            LL=(L1-w0)/2
            p1=(0,d2,0)
            p2=(10,h0/2,0)
            p3=(10,d2,0)
            p4=(w0-10,h0/2,0)
            p5=(w0,d2,0)
            p6=(w0,-d2,0)
            p7=(w0,-d2,0)
            p8=(w0-10,-h0/2,0)
            p9=(w0-10,-d2,0)
            p10=(10,-h0/2,0)
            p11=(0,-d2,0)
            p12=(10,0,0)
            p13=(w0,0,0)
            p14=(0,0,0)
            edge1 = Part.makeCircle(10, Base.Vector(10,d2,0), Base.Vector(0,0,1), 90, 180)
            edge2 = Part.makeLine(p2,p4)
            edge3 = Part.makeCircle(10, Base.Vector(w0-10,d2,0), Base.Vector(0,0,1), 0, 90)
            edge4 = Part.makeLine(p5,p7)
            edge5 = Part.makeCircle(10, Base.Vector(w0-10,-d2,0), Base.Vector(0,0,1), 270, 360)
            edge6 = Part.makeLine(p8,p10)
            edge7 = Part.makeCircle(10, Base.Vector(10,-d2,0), Base.Vector(0,0,1), 180, 270)
            edge8 = Part.makeLine(p11,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface = Part.Face(aWire)
            wface.Placement=App.Placement(App.Vector(LL,0,0),App.Rotation(App.Vector(1,0,0),0))
            c2=wface.extrude(Base.Vector(0,0,x3*H))#角柱下
            c1=c1.fuse(c2)
            edge1 = Part.makeCircle(10, Base.Vector(10,-d2,0), Base.Vector(0,0,1), 180, 270)
            edge2 = Part.makeLine(p10,p8)
            edge3 = Part.makeCircle(10, Base.Vector(w0-10,-d2,0), Base.Vector(0,0,1), 270, 360)
            edge4 = Part.makeLine(p11,p7)
            edge5 = Part.makeLine(p13,p7)
            edge6 = Part.makeLine(p13,p4)
            edge7 = Part.makeLine(p11,p14)
            edge8 = Part.makeLine(p13,p14)
            aWire1=Part.Wire([edge1,edge2,edge3,edge4])
            aWire11=Part.Wire([edge1,edge2,edge3,edge5,edge7,edge8])
            wface1 = Part.Face(aWire1)
            wface1.Placement=App.Placement(App.Vector(LL,0,0),App.Rotation(App.Vector(1,0,0),0))
            c3=wface1.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),180)
            c1=c1.fuse(c3)
            #フランジ
            x=25
            x1=(h0+2*x)/2
            p1=(-x,d2,0)
            p2=(10,x1,0)
            p3=(10,d2,0)
            p4=(w0-10,x1,0)
            p5=(w0+x,d2,0)
            p6=(w0-10,d2,0)
            p7=(w0+x,-d2,0)
            p8=(w0-10,-x1,0)
            p9=(w0-10,-d2,0)
            p10=(10,-x1,0)
            p11=(-x,-d2,0)
            p12=(10,-d2,0)
            edge1 = Part.makeCircle(35, Base.Vector(10,d2,0), Base.Vector(0,0,1), 90, 180)
            edge2 = Part.makeLine(p2,p4)
            edge3 = Part.makeCircle(35, Base.Vector(w0-10,d2,0), Base.Vector(0,0,1), 0, 90)
            edge4 = Part.makeLine(p5,p7)
            edge5 = Part.makeCircle(35, Base.Vector(w0-10,-d2,0), Base.Vector(0,0,1), 270, 360)
            edge6 = Part.makeLine(p8,p10)
            edge7 = Part.makeCircle(35, Base.Vector(10,-d2,0), Base.Vector(0,0,1), 180, 270)
            edge8 = Part.makeLine(p11,p1)
            aWire2=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface2 = Part.Face(aWire2)
            wface2.Placement=App.Placement(App.Vector(LL,0,x3*H),App.Rotation(App.Vector(0,0,1),0))
            c4=wface2.extrude(Base.Vector(0,0,0.7*M))#フランジ下
            c1=c1.fuse(c4)
            aWire3=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface3 = Part.Face(aWire3)
            wface3.Placement=App.Placement(App.Vector(LL,0,x3*H+0.7*M+3),App.Rotation(App.Vector(0,0,1),0))
            c5=wface3.extrude(Base.Vector(0,0,0.7*M))#フランジ上
            c1=c1.fuse(c5)
            wface4 = Part.Face(aWire11)
            wface4.Placement=App.Placement(App.Vector(LL,0,x3*H+2*0.7*M+3),App.Rotation(App.Vector(0,0,1),0))
            c6=wface4.revolve(Base.Vector(0,0,x3*H+2*0.7*M+3),Base.Vector(1,0,0),-180)
            c1=c1.fuse(c6)
            L0=h0
            if key_1<='075':
                L0=1.0*L0
                z1=x3*H+2*0.7*M+3+h0/2+10
            elif key_1<='200':
                L0=0.9*L0
                z1=x3*H+2*0.7*M+3+h0/2+10
            elif key_1<='250':
                L0=0.8*L0
                z1=x3*H+2*0.7*M+3+h0/2+20
            elif key_1<='300':
                L0=0.7*L0
                z1=x3*H+2*0.7*M+3+h0/2+50
            elif key_1<='500':
                L0=0.7*L0
                z1=x3*H+2*0.75*M+3+h0/2+60
            else:
                L0=0.5*L0
                z1=x3*H+2*0.7*M+3+h0/2+60
            w0=w0-0.1
            w1=w0-20
            h1=L0-20
            p1=(0,h1/2,0)
            p2=(10,L0/2,0)
            p3=(w0-10,L0/2,0)
            p4=(w0,h1/2,0)
            p5=(w0,-h1/2,0)
            p6=(w0-10,-L0/2,0)
            p7=(10,-L0/2,0)
            p8=(0,-h1/2,0)
            p9=(10,h1/2,0)
            p10=(w0-10,h1/2,0)
            p11=(w0-10,-h1/2,0)
            p12=(10,-h1/2,0)
            edge1 = Part.makeCircle(10, Base.Vector(10,h1/2,0), Base.Vector(0,0,1), 90, 180)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeCircle(10, Base.Vector(w0-10,h1/2,0), Base.Vector(0,0,1), 0, 90)
            edge4 = Part.makeLine(p4,p5)
            edge5 = Part.makeCircle(10, Base.Vector(w0-10,-h1/2,0), Base.Vector(0,0,1), 270, 0)
            edge6 = Part.makeLine(p6,p7)
            edge7 = Part.makeCircle(10, Base.Vector(10,-h1/2,0), Base.Vector(0,0,1), 180, 270)
            edge8 = Part.makeLine(p8,p1)
            aWire5=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface5 = Part.Face(aWire5)
            wface5.Placement=App.Placement(App.Vector((L1-w0)/2,0,0),App.Rotation(App.Vector(0,0,1),0))
            c7=wface5.extrude(Base.Vector(0,0,z1))#z1角柱
            c1=c1.fuse(c7)
            wface6 = Part.Face(aWire5)
            wface6.Placement=App.Placement(App.Vector((L1-w0)/2,0,z1+1),App.Rotation(App.Vector(0,0,1),0))
            c8=wface6.extrude(Base.Vector(0,0,0.7*M))
            c1=c1.fuse(c8)
            

            if key=='12':
                if key_1<='100':
                    Lb=20
                    B=20
                    C=25
                elif key_1<='150':
                    Lb=35
                    B=20
                    C=25
                elif key_1<='200':
                    Lb=40
                    B=25
                    C=30
                elif key_1<='250':
                    Lb=42
                    B=35
                    C=40
                elif key_1<='300':
                    Lb=45
                    B=35
                    C=45
                elif key_1<='400':
                    Lb=70
                    B=35
                    C=45
                elif key_1<='500':
                    Lb=100
                    B=35
                    C=45
                c9=Part.makeBox(32,32,50,Base.Vector((L1-32)/2,-16,H-50),Base.Vector(0,0,1))
                c1=c1.fuse(c9)
                c10= Part.makeCylinder(C,3,Base.Vector(L1/2,0,H-50-3),Base.Vector(0,0,1))
                c1=c1.fuse(c10)
                c11= Part.makeCylinder(B,Lb-3,Base.Vector(L1/2,0,H-50-Lb),Base.Vector(0,0,1))
                c1=c1.fuse(c11)
                c12= Part.makeCylinder(B,Lb,Base.Vector(L1/2,0,z1+10),Base.Vector(0,0,1))
                c1=c1.fuse(c12)
                c13= Part.makeCylinder(15,(H-(z1+50+Lb)),Base.Vector(L1/2,0,z1+Lb-3),Base.Vector(0,0,1))
                c1=c1.fuse(c13)
                c14= Part.makeCylinder(d0,L1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c14)

            elif key=='13':
                H=sa1[2]
                w=sa1[3]
                if key_1<='150':
                    Lb1=40
                    Lb2=50
                    B1=20
                    C=10
                elif key_1<='200':
                    Lb1=40
                    Lb2=50
                    B1=30
                    C=15
                elif key_1<='250':
                    Lb1=40
                    Lb2=50
                    B1=40
                    C=15
                elif key_1<='300':
                    Lb1=50
                    Lb2=60
                    B1=40
                    C=15
                elif key_1<='500':
                    Lb1=50
                    Lb2=60
                    B1=40
                    C=15
                h0=2*B1*2
                R=10
                t1=5
                z1=z1+1+0.7*M
                z2=z1+t1
                z3=H-d2*2
                z4=z3-Lb1
                z5=z4-(1+Lb2)
                LB3=z5-z1
                #シャフト
                cc1= Part.makeCylinder(C,(H-z1),Base.Vector(L1/2,0,z1),Base.Vector(0,0,1))
                cc2= Part.makeCylinder(B1,Lb1,Base.Vector(L1/2,0,z4+2*R),Base.Vector(0,0,1))
                cc3= Part.makeCylinder(B1,Lb2,Base.Vector(L1/2,0,z5+2*R),Base.Vector(0,0,1))
                cc1=cc1.fuse(cc2)
                cc1=cc1.fuse(cc3)
                cb1= Part.makeBox(1.6*B1,0.8*B1,t1,Base.Vector(L1/2-1.6*B1/2,h0/2,z1),Base.Vector(0,0,1))
                cb2= Part.makeBox(1.6*B1,0.8*B1,t1,Base.Vector(L1/2-1.6*B1/2,-h0/2-0.8*B1,z1),Base.Vector(0,0,1))
                p1=(L1/2,h0/2-B1/2,z2)
                p2=(L1/2,h0/2-B1/2,z5+Lb2/2-R)
                p3=(L1/2,h0/2-(R+B1/2),z5+Lb2/2)
                p4=(L1/2,-(h0/2-(R+B1/2)),z5+Lb2/2)
                p5=(L1/2,-(h0/2-B1/2),z5+Lb2/2-R)
                p6=(L1/2,-(h0/2-B1/2),z2)
                p7=(L1/2,-(h0/2+R),z5+Lb2/2-R)
                p8=(L1/2,-(h0/2+R),z5+Lb2/2-R)
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeCircle(R, Base.Vector(L1/2,h0/2-(R+B1/2),z5+Lb2/2-R), Base.Vector(1,0,0), 0, 90)
                edge3 = Part.makeLine(p3,p4)
                edge4 = Part.makeCircle(R, Base.Vector(L1/2,-(h0/2-(R+B1/2)),z5+Lb2/2-R), Base.Vector(1,0,0), 90, 180)
                edge5 = Part.makeLine(p5,p6)
                aWire1=Part.Wire([edge1,edge2,edge3,edge4,edge5])
                p1=(L1/2-0.8*B1,h0/2,z2)
                p2=(L1/2-0.8*B1,h0/2+t1/2,z2)
                p3=(L1/2-t1/2,h0/2+t1/2,z2)
                p4=(L1/2-t1/2,h0/2+B1/2,z2)
                p5=(L1/2+t1/2,h0/2+B1/2,z2)
                p6=(L1/2+t1/2,h0/2+t1/2,z2)
                p7=(L1/2+0.8*B1,h0/2+t1/2,z2)
                p8=(L1/2+0.8*B1,h0/2,z2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                w10=Part.makePolygon(plist)
                makeSolid=True
                isFrenet=True
                cb3 = Part.Wire(aWire1).makePipeShell([w10],makeSolid,isFrenet)#サポート
                cb1=cb1.fuse(cb2)
                cb1=cb1.fuse(cb3)
                torus=Part.makeTorus(w/2,15,Base.Vector(L1/2,0,z4+Lb1))
                c1=c1.fuse(cc1)
                c1=c1.fuse(cb1)
                c1=c1.fuse(torus)
                cc4= Part.makeCylinder(10,w,Base.Vector((L1-w)/2,0,z4+Lb1),Base.Vector(1,0,0))
                cc5= Part.makeCylinder(10,w,Base.Vector(L1/2,-w/2,z4+Lb1),Base.Vector(0,1,0))
                cc4=cc4.fuse(cc5)
                c1=c1.fuse(cc4)
                c14= Part.makeCylinder(d0,L1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c14)
            label='Gate Valve'    
            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
class JIS_Screw():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.show()
        

