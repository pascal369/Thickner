lst=('00_US_Straight tube','01_US_Coller')

FC_type={'00':'直管','01':'継ぎ輪'}

#直管-------------------------------------------------------------------------------------------------------------------------
strp=['800','900','1000','1100','1200','1350','1500','1600','1650','1800','2000','2100','2200','2400','2600']

#受口直管-------------------------------------------------------------------------------------------------------------------
#                              胴付               継輪
#         d0,    ｄ5,    ｄ2,    Y,   P,  L(有効長), L,  L(長),  J,   d9
rcvd={
'800':(   800,   973,  836.0, 105,  405,  4000,   840, 1960,  30,  794),
'900':(   900,  1077,  939.0, 105,  405,  4000,   840, 1960,  30,  897),
'1000':( 1000,  1183, 1041.0, 105,  430,  4000,   890, 1870,  30,  999),
'1100':( 1100,  1288, 1144.0, 105,  430,  4000,   890, 1870,  30, 1102),
'1200':( 1200,  1390, 1246.0, 105,  430,  4000,   890, 1870,  30, 1204),
'1350':( 1350,  1546, 1400.0, 105,  450,  4000,   930, 1790,  30, 1358),
'1500':( 1500,  1705, 1554.0, 105,  475,  4000,   980, 1900,  30, 1512),
'1600':( 1600,  1805, 1650.0, 115,  465,  4000,   960, 1860,  30, 1600),
'1650':( 1650,  1856, 1701.0, 115,  465,  4000,   960, 1860,  30, 1651),
'1800':( 1800,  2003, 1848.0, 115,  465,  4000,   960, 1860,  30, 1798),
'2000':( 2000,  2220, 2061.0, 115,  490,  4000,  1010, 1990,  30, 2011),
'2100':( 2100,  2326, 2164.0, 115,  500,  4000,  1030, 1830,  30, 2114),
'2200':( 2200,  2445, 2280.0, 115,  510,  4000,  1050, 1910,  30, 2230),
'2400':( 2400,  2630, 2458.0, 115,  530,  4000,  1090, 1750,  30, 2408),
'2600':( 2600,  2874, 2684.0, 130,  560,  4000,  1150, 1890,  30, 2624)
}