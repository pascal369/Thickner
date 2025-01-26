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
from . import NSE_Data

doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
#JDPA G 1042
class nse_ductile:
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

        def flng(self):#フランジ-----------------------------------------------------------------------------------------------
            global c01
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            LL2=sa[8]
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
                else:
                    ks=i*k0+k0/2
                    x=C*math.cos(ks)
                    y=C*math.sin(ks)
                    c20 = Part.makeCylinder(h/2,1.5*k,Base.Vector(0,x,y),Base.Vector(1,0,0))
                c01=c01.cut(c20) 
        def socket(self):#ソケット 直管75～150---------------------------------------------------------------------------------------
            global c00
            global d2
            global d0
            global Y
            global L0
            global P
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            Y=float(sa[3])
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            P=sa[4]
            d4=0.95*d5
            y=d5-d4
            x=(d5-d2)*math.sqrt(3)
            L0=P+x
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(20,0,d5)
            p4=Base.Vector(40,0,d5-y)
            p5=Base.Vector(P,0,d5-y)
            p6=Base.Vector(L0,0,d2)
            p7=Base.Vector(L0,0,d0)
            p8=Base.Vector(P,0,d0)
            p9=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)
        def socket1(self):#ソケット 異形管75～150---------------------------------------------------------------------------------------
            global c00
            global P
            global d2
            global d0
            global L0
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            if float(d0*2)<=100:
                p1=Base.Vector(0,-x1,-x1)
                p2=Base.Vector(0,-x1,x1)
                p3=Base.Vector(0,x1,x1)
                p4=Base.Vector(0,x1,-x1)
                p5=Base.Vector(0,-L,-x1)
                p6=Base.Vector(0,-L,x1)
                p7=Base.Vector(0,-x1,L)
                p8=Base.Vector(0,x1,L)
                p9=Base.Vector(0,L,x1)
                p10=Base.Vector(0,L,-x1)
                p11=Base.Vector(0,x1,-L)
                p12=Base.Vector(0,-x1,-L)
                p13=Base.Vector(0,0,0)
                edge1 = Part.makeCircle(E, p1, Base.Vector(1,0,0))
                edge2 = Part.makeCircle(E, p2, Base.Vector(1,0,0))
                edge3 = Part.makeCircle(E, p3, Base.Vector(1,0,0))
                edge4 = Part.makeCircle(E, p4, Base.Vector(1,0,0))
                edge5=Part.makeLine(p5,p6)
                edge6 = Part.makeCircle(y, p2, Base.Vector(1,0,0),90,180)
                edge7=Part.makeLine(p7,p8)
                edge8 = Part.makeCircle(y, p3, Base.Vector(1,0,0),0,90)
                edge9=Part.makeLine(p9,p10)
                edge10= Part.makeCircle(y, p4, Base.Vector(1,0,0),270,0)
                edge11=Part.makeLine(p11,p12)
                edge12= Part.makeCircle(y, p1, Base.Vector(1,0,0),180,270)
                edge13= Part.makeCircle(d2, p13, Base.Vector(1,0,0),0,360)
                aWire = Part.Wire([edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
                wface = Part.Face(aWire)
                c01 = Part.makeCylinder(d2,k,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c00 = wface.extrude(Base.Vector(k,0,0))
                c00=c00.cut(c01)
            elif float(d0*2)==150:
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                r=d4
                s=(d5-d4)
                x3=s*math.cos(math.radians(30))
                x31=s*math.sin(math.radians(30))
                x32=r*math.sin(math.radians(30))
                x33=r*math.cos(math.radians(30))
                x2=r+x3
                x20=x32+x3
                x21=x33+x31
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                p1=Base.Vector(0,-r,0)
                p2=Base.Vector(0,-x32,x33)
                p3=Base.Vector(0,x32,x33)
                p4=Base.Vector(0,r,0)
                p5=Base.Vector(0,x32,-x33)
                p6=Base.Vector(0,-x32,-x33)
                p7=Base.Vector(0,-(r+x3),-x31)
                p8=Base.Vector(0,-(r+x3),x31)
                p9=Base.Vector(0,-x20,x21)
                p10=Base.Vector(0,-x32,x33+s)
                p11=Base.Vector(0,x32,x33+s)
                p12=Base.Vector(0,x20,x21)
                p13=Base.Vector(0,r+x3,x31)
                p14=Base.Vector(0,r+x3,-x31)
                p15=Base.Vector(0,x20,-x21)
                p16=Base.Vector(0,x32,-(x33+s))
                p17=Base.Vector(0,-x32,-(x33+s))
                p18=Base.Vector(0,-x20,-x21)
                edge1 = Part.makeCircle(s, p1, Base.Vector(1,0,0),150,210)
                edge2=Part.makeLine(p8,p9)
                edge3 = Part.makeCircle(s, p2, Base.Vector(1,0,0),90,150)
                edge4=Part.makeLine(p10,p11)
                edge5 = Part.makeCircle(s, p3, Base.Vector(1,0,0),30,90)
                edge6=Part.makeLine(p12,p13)
                edge7 = Part.makeCircle(s, p4, Base.Vector(1,0,0),330,30)
                edge8=Part.makeLine(p14,p15)
                edge9 = Part.makeCircle(s, p5, Base.Vector(1,0,0),270,330)
                edge10=Part.makeLine(p16,p17)
                edge11 = Part.makeCircle(s, p6, Base.Vector(1,0,0),210,270)
                edge12=Part.makeLine(p18,p7)
                aWire = Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
                wface = Part.Face(aWire)
                c00 = wface.extrude(Base.Vector(k,0,0))
                c01 = Part.makeCylinder(d2,k,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c00=c00.cut(c01)
                c00.Placement=App.Placement(Base.Vector(0,0.0,0.0),App.Rotation(App.Vector(1,0,0),30))
                #Part.show(c00)
            p1=Base.Vector(k,0,d2)
            p2=Base.Vector(k,0,d3)
            p3=Base.Vector(P,0,d3)
            p4=Base.Vector(L0,0,d2)
            p5=Base.Vector(L0,0,d0)
            p6=Base.Vector(P,0,d0)
            p7=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c02=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            c00=c00.fuse(c02)
            c00=c00.cut(c01)

        def socketk(self):#ソケット 継輪 N-Link 075～450----------------------------------------------------------------------------------
            global c00
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            if key=='16':
                k=float(sa[9])
            else:
                k=float(sa[6])
            T1=float(sa[9])
            L=float(sa[10])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            L0=k
            if float(d0*2)<=100:
                p1=Base.Vector(0,-x1,-x1)
                p2=Base.Vector(0,-x1,x1)
                p3=Base.Vector(0,x1,x1)
                p4=Base.Vector(0,x1,-x1)
                p5=Base.Vector(0,-L,-x1)
                p6=Base.Vector(0,-L,x1)
                p7=Base.Vector(0,-x1,L)
                p8=Base.Vector(0,x1,L)
                p9=Base.Vector(0,L,x1)
                p10=Base.Vector(0,L,-x1)
                p11=Base.Vector(0,x1,-L)
                p12=Base.Vector(0,-x1,-L)
                p13=Base.Vector(0,0,0)
                edge1 = Part.makeCircle(E, p1, Base.Vector(1,0,0))
                edge2 = Part.makeCircle(E, p2, Base.Vector(1,0,0))
                edge3 = Part.makeCircle(E, p3, Base.Vector(1,0,0))
                edge4 = Part.makeCircle(E, p4, Base.Vector(1,0,0))
                edge5=Part.makeLine(p5,p6)
                edge6 = Part.makeCircle(y, p2, Base.Vector(1,0,0),90,180)
                edge7=Part.makeLine(p7,p8)
                edge8 = Part.makeCircle(y, p3, Base.Vector(1,0,0),0,90)
                edge9=Part.makeLine(p9,p10)
                edge10= Part.makeCircle(y, p4, Base.Vector(1,0,0),270,0)
                edge11=Part.makeLine(p11,p12)
                edge12= Part.makeCircle(y, p1, Base.Vector(1,0,0),180,270)
                edge13= Part.makeCircle(d2, p13, Base.Vector(1,0,0),0,360)
                aWire = Part.Wire([edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
                wface = Part.Face(aWire)
                c01 = Part.makeCylinder(d2,k,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c00 = wface.extrude(Base.Vector(k,0,0))
                c00=c00.cut(c01)
                #Part.show(c00)
            elif float(d0*2)==150:
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                r=d4
                s=(d5-d4)
                x3=s*math.cos(math.radians(30))
                x31=s*math.sin(math.radians(30))
                x32=r*math.sin(math.radians(30))
                x33=r*math.cos(math.radians(30))
                x2=r+x3
                x20=x32+x3
                x21=x33+x31

                p1=Base.Vector(0,-r,0)
                p2=Base.Vector(0,-x32,x33)
                p3=Base.Vector(0,x32,x33)
                p4=Base.Vector(0,r,0)
                p5=Base.Vector(0,x32,-x33)
                p6=Base.Vector(0,-x32,-x33)
                p7=Base.Vector(0,-(r+x3),-x31)
                p8=Base.Vector(0,-(r+x3),x31)
                p9=Base.Vector(0,-x20,x21)
                p10=Base.Vector(0,-x32,x33+s)
                p11=Base.Vector(0,x32,x33+s)
                p12=Base.Vector(0,x20,x21)
                p13=Base.Vector(0,r+x3,x31)
                p14=Base.Vector(0,r+x3,-x31)
                p15=Base.Vector(0,x20,-x21)
                p16=Base.Vector(0,x32,-(x33+s))
                p17=Base.Vector(0,-x32,-(x33+s))
                p18=Base.Vector(0,-x20,-x21)
                edge1 = Part.makeCircle(s, p1, Base.Vector(1,0,0),150,210)
                edge2=Part.makeLine(p8,p9)
                edge3 = Part.makeCircle(s, p2, Base.Vector(1,0,0),90,150)
                edge4=Part.makeLine(p10,p11)
                edge5 = Part.makeCircle(s, p3, Base.Vector(1,0,0),30,90)
                edge6=Part.makeLine(p12,p13)
                edge7 = Part.makeCircle(s, p4, Base.Vector(1,0,0),330,30)
                edge8=Part.makeLine(p14,p15)
                edge9 = Part.makeCircle(s, p5, Base.Vector(1,0,0),270,330)
                edge10=Part.makeLine(p16,p17)
                edge11 = Part.makeCircle(s, p6, Base.Vector(1,0,0),210,270)
                edge12=Part.makeLine(p18,p7)
                aWire = Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
                #Part.show(aWire)
                wface = Part.Face(aWire)
                c00 = wface.extrude(Base.Vector(k,0,0))
                c01 = Part.makeCylinder(d2,k,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c00=c00.cut(c01)
                c00.Placement=App.Placement(Base.Vector(0,0.0,0.0),App.Rotation(App.Vector(1,0,0),30))

        if key=='00' or key=='15'  or key=='17':#---------------------------------------------------------------
            if key=='00':
                #b='NSE_Straight tube'
                sa=NSE_Data.rcvd[key_1]
                socket(self)
                c1=c00
                L=App.ActiveDocument.getObject(label).L
                L = float(L)
                d0=float(sa[0])/2
                d2=float(sa[2])/2
                Y=float(sa[3])
                P=sa[4]
                d5=float(sa[1])/2
                x=(d5-d2)*math.sqrt(3)
                L0=P+x
                c2 = Part.makeCylinder(d2,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d0,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
                c1=c1.cut(c3)

            elif key=='15':
                sa=NSE_Data.rcvd[key_1]
                socket(self)
                L=App.ActiveDocument.getObject(label).L
                L = float(L)
                d0=float(sa[0])/2
                d2=float(sa[2])/2
                c1 = Part.makeCylinder(d2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
            elif key=='17':
                sa=NSE_Data.rcvd[key_1]
                d0=sa[0]/2
                d2=sa[2]/2
                Lx=sa[7]
                c1 = Part.makeCylinder(d2,Lx,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,Lx,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
        
        elif key=='01':
            sa=NSE_Data.trcts2[dia]
            H=sa[0]
            I=sa[1]
            J=sa[2]
            LL=sa[3]
            sa=NSE_Data.rcvd1[key_1]
            socket1(self)
            c1=c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            P0=P
            d02=d2
            d00=d0
            L00=L0
            sa=NSE_Data.rcvd1[key_2]
            if float(d0*2)<=100:
                socket1(self)
            elif float(d0*2)>100:
                socket1(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x    
            c2=c00
            c2.Placement=App.Placement(App.Vector(P0+H,P+I,0),App.Rotation(App.Vector(0,0,1),-90))
            c11 = Part.makeCylinder(d02,P0+LL-L00,Base.Vector(L00,0,0),Base.Vector(1,0,0))
            c12 = Part.makeCylinder(d00,P0+LL-L00,Base.Vector(L00,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            c1=c1.fuse(c11)
            c4 = Part.makeCylinder(d2,I,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
            c5 = Part.makeCylinder(d0,I,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
            c1=c1.fuse(c4)
            c1=c1.cut(c5)
            c1=c1.cut(c12)
        
        elif key=='02':#---------------------------------------------------------------
            #sa=NSE_Data.trcts3[dia]
            sa=NSE_Data.rcvd1[key_1]
            socket1(self)
            c1=c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            d00=d0
            d02=d2
            L00=L0
            P0=P
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(L), None, QtGui.QApplication.UnicodeUTF8))
            sa=NSE_Data.rcvd1[key_2]
            socket1(self)
            c2=c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            L=180
            x1=L00-P0
            x2=L0-P
            Lr=L-(x1+x2)
            c2.Placement=App.Placement(App.Vector(L+P0+P,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            p1=(L00,0,d00)
            p2=(L00,0,d02)
            p3=(L00+Lr,0,d2)
            p4=(L00+Lr,0,d0)
            plist=[p1,p2,p3,p4,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c5=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
            c1=c1.fuse(c5)

        
        elif key=='03' or key=='04' or key=='05' or key=='06' or key=='07':#曲管-----------------------------------------
            sa=NSE_Data.rcvd1[key_1]
            socket1(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            if key=='03':#90
                sa1=NSE_Data.elbows_90[key_1]
                b='NSE_90Bent tube'
            elif key=='04':#45
                sa1=NSE_Data.elbows_45[key_1]
                b='NSE_45Bent tube'
            elif key=='05':#22 1/2
                sa1=NSE_Data.elbows_22[key_1]
                b='NSE_22Bent tube'
            elif key=='06':#11 1/4
                sa1=NSE_Data.elbows_11[key_1]
                b='NSE_11Bent tube'
            elif key=='07':#5 5/8
                sa1=NSE_Data.elbows_5[key_1]
                b='NSE_5Bent tube'
            R=sa1[0]
            L1=sa1[1]
            L2=sa1[2]
            s=float(sa1[3])/2
            a0=L0-P
            x=R-R*math.cos(math.radians(s))
            y=R*math.sin(math.radians(s))
            x1=R-R*math.cos(math.radians(2*s))
            x2=L2*math.cos(math.radians(90-2*s))
            y1=R*math.sin(math.radians(2*s))
            y2=y1-R*math.tan(math.radians(s))
            y3=R*math.tan(math.radians(s))-y
            y4=L2*math.sin(math.radians(90-2*s))
            c11 = Part.makeCylinder(d2,P,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c12 = Part.makeCylinder(d0,L0,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c11)
            c1=c1.cut(c12)
            c1.Placement=App.Placement(App.Vector(0,-(P+L1),0),App.Rotation(App.Vector(0,0,1),90))
            p1=(0,-(L1-a0),0)
            p2=(0,-R*math.tan(math.radians(s)),0)
            p3=(x,-y3,0)
            p4=(x1,y2,0)
            p5=(L2*math.cos(math.radians(90-2*s)),L2*math.sin(math.radians(90-2*s)),0)
            edge1=Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(R, Base.Vector(R,-R*math.tan(math.radians(s)),0), Base.Vector(0,0,1), 180-2*s, 180)
            edge3=Part.makeLine(p4,p5)
            aWire = Part.Wire([edge1,edge2,edge3])
            edge7 = Part.makeCircle(d2, Base.Vector(0,-(L1-a0),0), Base.Vector(0,1,0), 0, 360)
            edge8 = Part.makeCircle(d0, Base.Vector(0,-(L1-a0),0), Base.Vector(0,1,0), 0, 360)
            profile = Part.Wire([edge7])
            profile1 = Part.Wire([edge8])
            makeSolid=True
            isFrenet=True
            c2 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c3 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
            c1=c1.fuse(c2)
            c1=c1.cut(c3)
        
        elif key=='08' or key=='09':#両受曲管-----------------------------------------
            sa=NSE_Data.rcvd1[key_1]
            socket1(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            #Part.show(c1)
            #sa=NSE_Data.rcvd1[key_1]
            socket1(self)
            c2=c00

            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(L1), None, QtGui.QApplication.UnicodeUTF8))
            if key=='08':#45
                b='NSE_45Two-track tube'
                sa1=NSE_Data.two_t_45[key_1]
                s=22.5
            elif key=='09':
                b='NSE_22Two-track tube'
                sa1=NSE_Data.two_t_22[key_1]
                s=11.25
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            s2=float(s*2)
            R=sa1[0]
            L1=sa1[1]
            y=R*math.tan(math.radians(s))
            x=P+L1
            p1=(R,0,x-y)
            p2=(0,L0,0)
            p3=(0,x-y,0)
            p4=(y*math.cos(math.radians(90-s2)),x+y*math.sin(math.radians(90-s2)),0)
            p5=((x-L0)*math.cos(math.radians(90-s2)),x+(x-L0)*math.sin(math.radians(90-s2)),0)
            x1=(P+L1)*math.cos(math.radians(90-s2))
            y1=x+x*math.sin(math.radians(90-s2))
            c2.Placement=App.Placement(App.Vector(x1,y1,0),App.Rotation(App.Vector(0,0,1),(270-s2)))
            edge1=Part.makeLine(p2,p3)
            edge2 = Part.makeCircle(R, Base.Vector(R,x-y,0), Base.Vector(0,0,1), (180-s2), 180)
            edge3=Part.makeLine(p4,p5)
            edge4 = Part.makeCircle(d2, Base.Vector(0,x-y,0), Base.Vector(0,1,0))
            edge5 = Part.makeCircle(d0, Base.Vector(0,x-y,0), Base.Vector(0,1,0))
            aWire=Part.Wire([edge1,edge2,edge3])
            profile2=Part.Wire([edge4])
            profile3=Part.Wire([edge5])
            makeSolid=True
            isFrenet=True
            c3 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
            c4 = Part.Wire(aWire).makePipeShell([profile3],makeSolid,isFrenet)
            c3=c3.cut(c4)
            c2=c2.fuse(c3)
            c1=c1.fuse(c2)
        
        elif key=='10' :#浅層埋設形フランジ付きT字管------------------------------
            sa1=NSE_Data.sttfs[dia]
            H=sa1[0]
            I=sa1[1]
            J=sa1[2]
            L=sa1[3]
            #b='NSE_T-shaped pipe with shallow buried Flange'
            sa=NSE_Data.rcvd1[key_1]
            socket1(self)
            c1=c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            d00=d0
            d02=d2
            P0=P
            L00=L0
            x=P0+H+J-L00
            c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            sa=NSE_Data.flngs[key_2]
            h=sa[14]
            flng(self)
            c2=c01
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            LL2=sa[8]
            
            x1=m+k
            c2.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
            c4 = Part.makeCylinder(d2-0.1,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
            c2=c2.fuse(c4)
            c5 = Part.makeCylinder(d0,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
            c2=c2.cut(c5)
            c1=c1.fuse(c2)
            c1=c1.fuse(c3)
            c1=c1.cut(c6)
        
        elif key=='11':#受挿し短管---------------------------------------------------
            sa=NSE_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            L=float(sa[7])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            x=(d3-d2)*math.sqrt(2)
            L0=P+x
            sa1=NSE_Data.tnkns[dia]
            L1=sa1[0]
            Lx=P+L1-L0
            c1=c00
            c3 = Part.makeCylinder(d2,Lx,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d0,Lx,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.fuse(c3)
        
        elif key=='12':#継輪-----------------------------------------------------
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            sa=NSE_Data.rcvdk[key_1]
            socketk(self)
            LL=sa[7]
            y1=sa[8]
            c1=c00
            socketk(self)
            c2=c00
            d2=float(sa[2])/2
            d4=float(sa[4])/2
            E=float(sa[5])/2
            d3=d4-(E+5)
            k=float(sa[6])
            L0=k
            if key_1=='150':
                c2.Placement=App.Placement(Base.Vector(LL-L0,0.0,0.0),App.Rotation(App.Vector(1,0,0),30))
            else:
                c2.Placement=App.Placement(Base.Vector(LL-L0,0.0,0.0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #y11='胴付寸法y1[mm]=' + str(y1)
            #self.label_7.setText(QtGui.QApplication.translate("Dialog", y11, None, QtGui.QApplication.UnicodeUTF8))

            c3 = Part.makeCylinder(d3,LL-2*L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d2,LL-2*L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
            c3=c3.cut(c4)
            c1=c1.fuse(c3)
          
        elif key=='13':#帽---------------------------------------------------
            sa=NSE_Data.rcvdk[key_1]
            socketk(self)
            T1=sa[9]
            c1=c00
            d2=float(sa[2])/2
            P=sa[3]
            d4=float(sa[4])/2
            E=float(sa[5])/2
            k=float(sa[6])
            T1=float(sa[9])
            L=float(sa[10])/2
            x1=d4/math.sqrt(2)
            y=L-x1
            d3=d4-(E+5)
            L0=k
            if key_1=='150':
               c1.Placement=App.Placement(Base.Vector(0,0.0,0.0),App.Rotation(App.Vector(1,0,0),0))
            p1=(L0,0,d2)
            p2=(L0,0,d3)
            p3=(P+T1,0,d3)
            p4=(P+T1,0,0)
            p5=(P,0,0)
            p6=(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(L0,0.0,0.0),Base.Vector(1,0,0),360)
            c1=c1.fuse(c2)
        
        elif key=='14':#押輪---------------------------------------------------
            sa=NSE_Data.rcvd1[dia]
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            d4=float(sa[4])/2
            E=float(sa[5])/2
            M=sa[9]
            L=sa[10]
            d3=d4-(E+5)
            p1=(0,0,d2)
            p2=(0,0,d3)
            p3=(L-M,0,d3)
            p4=(L-M,0,d5)
            p5=(L,0,d5)
            p6=(L,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
        
        elif key=='16':#N-Link---------------------------------------------------
            if key_1=='150':
                sa=NSE_Data.rcvd1[dia]
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                d4=float(sa[4])/2
                E=float(sa[5])/2
                M=sa[9]
                L=sa[10]
                B=sa[11]
                d3=d4-(E+5)
                p1=(0,0,d2)
                p2=(0,0,d3)
                p3=(B-M,0,d3)
                p4=(B-M,0,d5)
                p5=(B,0,d5)
                p6=(B,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
            else:
                sa=NSE_Data.rcvd1[dia]
                d2=float(sa[2])/2
                d4=float(sa[4])/2
                E=float(sa[5])/2
                d3=d4-(E+5)
                B=sa[11]
                M=sa[9]
                sa=NSE_Data.rcvdk[key_1]
                socketk(self)
                c1=c00
                c1.Placement=App.Placement(Base.Vector(B-M,0.0,0.0),App.Rotation(App.Vector(1,0,0),0))
                p1=(0,0,d2)
                p2=(0,0,d3)
                p3=(B-M,0,d3)
                p4=(B-M,0,d2)
                plist=[p1,p2,p3,p4,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
                c1=c1.fuse(c2)
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

