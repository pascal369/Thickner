# -*- coding: utf-8 -*-
from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import US_Data

class us_ductile:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        Fittings=App.ActiveDocument.getObject(label).Fittings
        key=Fittings[:2]
        dia=App.ActiveDocument.getObject(label).dia
        
        try:
            if dia[3]=='x':
                key_1=dia[:3]
                key_2=dia[4:]
            else:
                key_1=dia[:4]
                key_2=dia[5:]
        except:
            key_1=dia
            pass   

        def socket(self):#ソケット ---------------------------------------------------------------------------------------
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            global c00
            d0=sa[0]/2
            d5=sa[1]/2
            d2=sa[2]/2
            P=sa[4]
            Y=sa[3]
            L=sa[5]
            s1=0.2*P
            d3=0.98*d5
            y1=d5-d3
            y2=d3-d2
            x=y1*math.sqrt(3)
            x1=y2*math.sqrt(3)
            L0=P+x1
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(s1,0,d5)
            p4=Base.Vector(s1+x,0,d3)
            p5=Base.Vector(P,0,d3)
            p6=Base.Vector(P+x1,0,d2)
            p7=Base.Vector(P+x1,0,d0)
            p8=Base.Vector(P,0,d0)
            p9=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)
        if key=='00':#------------------------------------------------------------------------------------------------
            b='US_Straight tube'
            sa=US_Data.rcvd[key_1]
            socket(self)
            d0=sa[0]/2
            d5=sa[1]/2
            d2=sa[2]/2
            P=sa[4]
            Y=sa[3]
            #Lx=sa[5]
            s1=0.2*P
            d3=0.98*d5
            y1=d5-d3
            y2=d3-d2
            x=y1*math.sqrt(3)
            x1=y2*math.sqrt(3)
            L0=P+x1
            c1=c00
            L=App.ActiveDocument.getObject(label).L
            L=float(L)
            c2 = Part.makeCylinder(d2,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            c1=c1.cut(c3)

        elif key=='01':
            b='US_Coller'
            sa=US_Data.rcvd[key_1]
            d0=sa[0]/2
            d5=sa[1]/2
            d2=sa[2]/2

            Y=sa[3]
            P=sa[4]
            L=sa[6]
            J=sa[8]

            d9=sa[9]/2
            x=0.11*L
            x1=(L-J)/2
            d3=0.93*d5

            p1=(0,0,d2)
            p2=(0,0,d5)
            p3=(x,0,d5)
            p4=(x,0,d3)
            p5=(L-x,0,d3)
            p6=(L-x,0,d5)
            p7=(L,0,d5)
            p8=(L,0,d2)
            p9=(L-x1,0,d2)
            p10=(L-x1,0,d9)
            p11=(x1,0,d9)
            p12=(x1,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        label='mass[kg]'
        try:
            #obj.addProperty("App::PropertyFloat", "body",label)
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass  
        obj.Shape=c1
