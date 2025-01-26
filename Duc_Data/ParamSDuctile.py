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
from . import S_Data

doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
#JWWA G 113

class s_ductile:
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

        def socket(self):#ソケット 直管500～2200---------------------------------------------------------------------------------------
            global c00

            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            Y=float(sa[3])
            P=float(sa[4])
            s1=0.23*P
            d3=(d2+d5)/2
            y1=d5-d3
            x=y1*math.sqrt(3)
            L0=P+x
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(s1,0,d5)
            p4=Base.Vector(s1+x,0,d3)
            p5=Base.Vector(P,0,d3)
            p6=Base.Vector(P+x,0,d2)
            p7=Base.Vector(P+x,0,d0)
            p8=Base.Vector(P,0,d0)
            p9=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)
        if key=='00':#------------------------------------------------------------------------------------------------
            sa=S_Data.rcvd[key_1]
            socket(self)
            c1=c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            Y=float(sa[3])
            P=float(sa[4])
            s1=0.23*P
            d3=(d2+d5)/2
            y1=d5-d3
            x=y1*math.sqrt(3)
            L0=P+x
            L=App.ActiveDocument.getObject(label).L
            L=float(L)
            c2 = Part.makeCylinder(d2,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
            #Part.show(c2)
            c1=c1.fuse(c2)
            c1=c1.cut(c3)
        
        elif key=='01' or key=='02':
            b='S_Coller'
            sa=S_Data.rcvd[key_1]
            d5=sa[1]/2
            d2=sa[2]/2

            if key=='01':
                b='S_Coller'
                L=sa[6]
                y1=sa[8]
                M = 2*sa[10]

            elif key=='02':
                b='S_Long coller'
                L=sa[7]
                y1=sa[9]
                M = 2*sa[10]

            d3=(d2+d5)/2
            d4=d5*0.98
            x=0.2*sa[6]
            x1=L-(x+M)
            x2=d4-d3

            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d2), None, QtGui.QApplication.UnicodeUTF8))
            p1=(0,0,d2)
            p2=(0,0,d5)
            p3=(M,0,d5)
            p4=(M,0,d4)
            p5=(x,0,d4)
            p6=(x+x2*math.sqrt(3),0,d3)
            p7=(L-(x+x2*math.sqrt(3)),0,d3)
            p8=(L-x,0,d4)
            p9=(L-M,0,d4)
            p10=(L-M,0,d5)
            p11=(L,0,d5)
            p12=(L,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        
        elif key=='03':
            b='S_Retainer gland'
            sa=S_Data.rcvd[key_1]
            d5=sa[1]/2
            R=sa[14]
            M1=sa[10]
            M2=sa[12]
            A=sa[11]
            H=sa[13]
            d3=R-H
            x=M2-A
            L=M1+x
            p1=(0,0,d3)
            p2=(0,0,d5)
            p3=(M1,0,d5)
            p4=(M1,0,R)
            p5=(L,0,R)
            p6=(L,0,d3)
            plist=[p1,p2,p3,p4,p5,p6,p1]
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
