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
from . import T_Data

doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
#JDPA G 3005
class t_ductile:
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
            global d0
            global d2
            global m
            global k
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
        def socket(self):#ソケット-----------------------------------------------------------------------------------------------
            global c00
            global d2
            global d0
            global L0
            global P

            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            k=sa[5]
            L=sa[6]
            if float(key_1)<=250:
                d3=d5-4
                d4=d3-P*math.tan(math.radians(3))
                x=(d4-d2)*math.sqrt(3)
                L0=P+x

                p1=Base.Vector(0,0,d2)
                p2=Base.Vector(0,0,d5)
                p3=Base.Vector(10,0,d5)
                p4=Base.Vector(10,0,d3)
                p5=Base.Vector(P,0,d4)
                p6=Base.Vector(L0,0,d2)
                p7=Base.Vector(L0,0,d0)
                p8=Base.Vector(P,0,d0)
                p9=Base.Vector(P,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]

            elif float(key_1)<=600:
                d3=d5-5
                d4=d3-(0.6*P-25)*math.tan(math.radians(3))
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d4), None, QtGui.QApplication.UnicodeUTF8))
                d6=d4-0.4*P*math.tan(math.radians(6))
                x=(d6-d2)*math.sqrt(3)
                L0=P+x

                p1=Base.Vector(0,0,d2)
                p2=Base.Vector(0,0,d5)
                p3=Base.Vector(25,0,d5)
                p4=Base.Vector(25,0,d3)
                p5=Base.Vector(0.6*P,0,d4)
                p6=Base.Vector(P,0,d6)
                p7=Base.Vector(L0,0,d2)
                p8=Base.Vector(L0,0,d0)
                p9=Base.Vector(P,0,d0)
                p10=Base.Vector(P,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]

            elif float(key_1)<=2000:
                d3=d5-10
                d4=d3-0.4*P*math.tan(math.radians(3))
                x=(d4-d2)*math.sqrt(3)
                L0=P+x

                p1=Base.Vector(0,0,d2)
                p2=Base.Vector(0,0,d5)
                p3=Base.Vector(P/4,0,d5)
                p4=Base.Vector(P/4+10,0,d3)
                p5=Base.Vector(0.6*P,0,d3)
                p6=Base.Vector(P,0,d4)
                p7=Base.Vector(L0,0,d2)
                p8=Base.Vector(L0,0,d0)
                p9=Base.Vector(P,0,d0)
                p10=Base.Vector(P,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]

            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)

        def socket1(self):#ソケット-----------------------------------------------------------------------------------------------
            global c00
            global d2
            global d0
            global L0
            global P

            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            #k=sa[5]
            #L=sa[6]

            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x

            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(10,0,d5)
            p4=Base.Vector(10,0,d3)
            p5=Base.Vector(0.6*P,0,d4)
            p6=Base.Vector(0.6*P+x1,0,d6)
            p7=Base.Vector(P,0,d6)
            p8=Base.Vector(L0,0,d2)
            p9=Base.Vector(L0,0,d0)
            p10=Base.Vector(P,0,d0)
            p11=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p1]

            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)
        def socketk(self):#ソケット 異形管-----------------------------------------------------------------------------------------------
            global c00
            global d0
            global d5
            global d2
            global d3
            global L1
            global d4
            global E0
            global d6

            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            d3=float(sa[3])/2
            L1=float(sa[4])
            x=sa[5]
            P=sa[6]
            #P0=P
            L=sa[7]
            Lc=sa[8]
            y=(d3-d2)
            L0=(L1+x+2*y)
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(L1,0,d5)
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

        if key=='00' or key=='17':#---------------------------------------------------------------
            if key=='00':
                b='T_Straight tube'
                sa=T_Data.rcvd[key_1]
                socket(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d5=float(sa[3])/2
                P=sa[4]
                k=sa[5]
                L=sa[6]
                if float(key_1)<=250:
                    d3=d5-4
                    d4=d3-P*math.tan(math.radians(3))
                    x=(d4-d2)*math.sqrt(3)
                    L0=P+x
                elif float(key_1)<=600:
                    d3=d5-5
                    d4=d3-(0.6*P-25)*math.tan(math.radians(3))
                    #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d4), None, QtGui.QApplication.UnicodeUTF8))
                    d6=d4-0.4*P*math.tan(math.radians(6))
                    x=(d6-d2)*math.sqrt(3)
                    L0=P+x
                c1=c00
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                c2 = Part.makeCylinder(d2,L-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d0,L-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
                c1=c1.cut(c3)
            elif key=='17':
                b='Straight tube'
                sa=T_Data.rcvd[key_1]
                socket(self)
                d2=float(sa[1])/2
                d0=float(sa[0])/2
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                c1 = Part.makeCylinder(d2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
        
        elif key=='01' or key=='02':
            if key=='01':
                sa=T_Data.trcts[dia]
            elif key=='02':
                sa=T_Data.trcts2[dia]
            H=sa[0]
            I=sa[1]
            J=sa[2]
            LL=sa[3]

            sa=T_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            c1=c00
            P0=P
            d02=d2
            d00=d0
            sa=T_Data.rcvd1[key_2]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            c2=c00
            c2.Placement=App.Placement(App.Vector(P0+H,P+I,0),App.Rotation(App.Vector(0,0,1),-90))

            c11 = Part.makeCylinder(d02,P0+LL-L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c12 = Part.makeCylinder(d00,P0+LL-L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            c1=c1.fuse(c11)

            if key=='01':
                c3=c00
                c3.Placement=App.Placement(App.Vector(P0+H,-(P+I),0),App.Rotation(App.Vector(0,0,1),90))
                c1=c1.fuse(c3)
            if key=='02':
                c4 = Part.makeCylinder(d2-0.1,I,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c5 = Part.makeCylinder(d0,I,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c1=c1.fuse(c4)
                c1=c1.cut(c5)
                c1=c1.cut(c12)

            elif key=='01':
                #Part.show(c1)
                c4 = Part.makeCylinder(d2,2*I,Base.Vector(P0+H,-I,0),Base.Vector(0,1,0))
                c5 = Part.makeCylinder(d0,2*I,Base.Vector(P0+H,-I,0),Base.Vector(0,1,0))
                c1=c1.fuse(c4)
                c1=c1.cut(c5)
                c1=c1.cut(c12)

        
        elif key=='03' or key=='04':#---------------------------------------------------------------
            sa=T_Data.rcvd1[key_1]
            if key=='04':
                sa=T_Data.rcvd1[key_2]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            c1=c00
            d00=d0
            d02=d2
            L00=L0
            P0=P
            sa=T_Data.rcvd1[key_2]
            if key=='04':
                sa=T_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            sa1=T_Data.trcts3[dia]
            A0=sa1[0]
            B=sa1[1]
            C=sa1[2]
            E=sa1[3]
            L1=sa1[4]

            if key=='03':
                x0=L1-(A0+B)
                p1=(L00,0,d00)
                p2=(L00,0,d02)
                p3=(P0+A0,0,d02)
                p4=(P0+A0+x0,0,d2)
                p5=(P0+A0+x0+B,0,d2)
                p6=(P0+L1,0,d0)
                p7=(P0+A0+x0,0,d0)
                p8=(P0+A0,0,d00)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c5=wface.revolve(Base.Vector(0,0,0),Base.Vector(1.0,0.0,0.0),360)
                c1=c1.fuse(c5)

            elif key=='04':
                x0=L1-(E+C)
                p1=(L00,0,d00)
                p2=(L00,0,d02)
                p3=(P0+E,0,d02)
                p4=(P0+E+x0,0,d2)
                p5=(P0+E+x0+C,0,d2)
                p6=(P0+L1,0,d0)
                p7=(P0+E+x0,0,d0)
                p8=(P0+E,0,d00)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c5=wface.revolve(Base.Vector(0,0,0),Base.Vector(1.0,0.0,0.0),360)
                c1=c1.fuse(c5)

        
        elif key=='05' or key=='06' or key=='07' or key=='08':#曲管-----------------------------------------
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            sa=T_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
            if key=='05':#90
                sa1=T_Data.elbows_90[key_1]
                b='T_90Elbow_'
            elif key=='06':#45
                sa1=T_Data.elbows_45[key_1]
                b='T_45Elbow_'
            elif key=='07':#22 1/2
                sa1=T_Data.elbows_22[key_1]
                b='T_22Elbow_'
            elif key=='08':#11 1/4
                sa1=T_Data.elbows_11[key_1]
                b='T_11Elbow_'
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

        elif key=='09' or key=='10' or key=='11' :#-----------------------------------------------------------------------------------
            if key=='09':
                sa1=T_Data.ttfs[dia]
                H=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L=sa1[3]
                b='T_T-shaped tube with flange'
                sa=T_Data.rcvd1[key_1]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d5=float(sa[3])/2
                P=sa[4]
                d3=d5-4
                d4=d3-(0.6*P-10)*math.tan(math.radians(3))
                d6=d4-10
                x1=(d4-d6)*math.sqrt(2)
                x=(d6-d2)*math.sqrt(3)
                L0=P+x
                c1=c00
                d00=d0
                d02=d2
                P0=P
                L00=L0
                x=P0+H+J-L00
                c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                sa=T_Data.flngs[key_2]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                c2=c01
                x1=m+k
                c2.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c4 = Part.makeCylinder(d2-0.1,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.fuse(c4)
                c5 = Part.makeCylinder(d0,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.cut(c5)
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)
                c1=c1.cut(c6)
            if key=='10':
                sa1=T_Data.ttfs3[dia]
                H=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L=sa1[3]
                b='T_T-shaped tube with flange'
                sa=T_Data.rcvd1[key_1]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d5=float(sa[3])/2
                P=sa[4]
                d3=d5-4
                d4=d3-(0.6*P-10)*math.tan(math.radians(3))
                d6=d4-10
                x1=(d4-d6)*math.sqrt(2)
                x=(d6-d2)*math.sqrt(3)
                L0=P+x
                c1=c00
                d00=d0
                d02=d2
                P0=P
                L00=L0
                x=P0+H+J-L00
                c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                sa=T_Data.flngs[key_2]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                c2=c01
                x1=m+k
                c2.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c4 = Part.makeCylinder(d2-0.1,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.fuse(c4)
                c5 = Part.makeCylinder(d0,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.cut(c5)
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)
                c1=c1.cut(c6)
            elif key=='11':
                sa1=T_Data.ttfs2[dia]
                H=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L=sa1[3]
                b='T_T-shaped pipe with a spiral flange'
                sa=T_Data.rcvd1[key_1]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d5=float(sa[3])/2
                P=sa[4]
                d3=d5-4
                d4=d3-(0.6*P-10)*math.tan(math.radians(3))
                d6=d4-10
                x1=(d4-d6)*math.sqrt(2)
                x=(d6-d2)*math.sqrt(3)
                L0=P+x
                c1=c00
                d00=d0
                d02=d2
                P0=P
                L00=L0
                x=P0+H+J-L00
                c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                sa=T_Data.flngs[key_2]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                c2=c01
                x1=m+k
                c2.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c4 = Part.makeCylinder(d2-0.1,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.fuse(c4)
                c5 = Part.makeCylinder(d0,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.cut(c5)
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)
                c1=c1.cut(c6)
                R0=d02+d0
                R1=d00-float(d0)/4
                edge10 = Part.makeCircle(R0, Base.Vector(P0+H,0,0), Base.Vector(1,0,0), 270, 0)
                x=P0+H
                p1=(x-d2,0,-d02)
                p2=(x-d2,0,-(d02+d2))
                p3=(x+d2,0,-(d02+d2))
                p4=(x+d2,0,-(d02))
                p5=(x,0,-(d02+d2))
                edge1=Part.makeLine(p1,p2)
                edge2 = Part.makeCircle(d2, Base.Vector(x,0,-(d02+d2)), Base.Vector(0,1,0), 0, 180)
                edge3=Part.makeLine(p3,p4)
                edge4=Part.makeLine(p4,p1)
                aWire=Part.Wire([edge1,edge2,edge3,edge4])
                makeSolid=True
                isFrenet=True
                c7 = Part.Wire(edge10).makePipeShell([aWire],makeSolid,isFrenet)
                c1=c1.fuse(c7)
                p1=(x,-R1,0)
                p2=(x,-R1,-(R0-R1))
                p3=(x,0,-(R0-R1))
                edge1=Part.makeLine(p1,p2)
                edge2 = Part.makeCircle(R1, Base.Vector(x,0,-(R0-R1)), Base.Vector(1,0,0), 180, 270)
                aWire1=Part.Wire([edge1,edge2])

                if d00==37.5:
                    xx=0.8
                    yy=1.0
                    p1=(x+xx*d2/2,-(R1-xx*d2/2),0)
                    p2=(x-xx*d2/2,-(R1-xx*d2/2),0)
                    p3=(x-xx*d2/2,-yy*R1,0)
                    p4=(x+xx*d2/2,-yy*R1,0)
                    p5=(x,-yy*R1,0)
                    edge1=Part.makeLine(p1,p2)
                    edge2=Part.makeLine(p2,p3)
                    edge3 = Part.makeCircle(xx*d2/2, Base.Vector(x,-yy*R1,0), Base.Vector(0,0,1), 180, 0)

                elif d00>=50:
                    p1=(x+0.8*d2/2,-(R1-0.8*d2/2),0)
                    p2=(x-0.8*d2/2,-(R1-0.8*d2/2),0)
                    p3=(x-0.8*d2/2,-R1,0)
                    p4=(x+0.8*d2/2,-R1,0)
                    p5=(x,-R1,0)
                    edge1=Part.makeLine(p1,p2)
                    edge2=Part.makeLine(p2,p3)
                    edge3 = Part.makeCircle(0.8*d2/2, Base.Vector(x,-R1,0), Base.Vector(0,0,1), 180, 0)

                edge4=Part.makeLine(p4,p1)
                makeSolid=True
                isFrenet=True
                aWire2=Part.Wire([edge1,edge2,edge3,edge4])

                c8 = Part.Wire(aWire1).makePipeShell([aWire2,aWire],makeSolid,isFrenet)
                c1=c1.fuse(c8)
                c1=c1.cut(c6)
        
        elif key=='12':#排水T字管---------------------------------------------------
            b ='T_Drainage T-shaped pipe'
            sa=T_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            c1=c00
            #Part.show(c1)
            P0=P
            d00=d0
            d02=d2
            socket1(self)
            c2=c00
            sa1=T_Data.dtps[dia]
            H=sa1[0]
            I=sa1[1]
            Lx=sa1[2]
            x=2*P0+Lx
            x1=Lx+2*P0-2*L0
            c2.Placement=App.Placement(App.Vector(x,0,0),App.Rotation(App.Vector(0,0,1),180))
            c3 = Part.makeCylinder(d02,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d00,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            #Part.show(c1)
            sa=T_Data.rcvd1[key_2]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            c5=c00
            c5.Placement=App.Placement(App.Vector(P0+H,I+P,-(d02-d2)),App.Rotation(App.Vector(0,0,1),-90))
            c1=c1.fuse(c5)
            x=I+P-L0
            c6 = Part.makeCylinder(d2,x,Base.Vector(P0+H,0,-(d02-d2)),Base.Vector(0,1,0))
            c61 = Part.makeCylinder(d0,x,Base.Vector(P0+H,0,-(d02-d2)),Base.Vector(0,1,0))
            c6=c6.cut(c61)
            c1=c1.fuse(c6)
            c1=c1.fuse(c3)
            c1=c1.cut(c4)
            c1=c1.cut(c61)
        
        elif key=='13':#継輪-----------------------------------------------------
            sa=T_Data.rcvdk[key_1]
            socketk(self)

            #d0=sa[0]/2
            d5=sa[1]/2
            d2=sa[2]/2
            d3=sa[3]/2
            L1=sa[4]
            Lx=sa[8]
            d6=(Lx/2-L1)*math.tan(math.radians(3))+d3
            
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(L1,0,d5)
            p4=Base.Vector(L1,0,d3)
            p5=Base.Vector(Lx/2,0,d6)
            p6=Base.Vector(Lx-L1,0,d3)
            p7=Base.Vector(Lx-L1,0,d5)
            p8=Base.Vector(Lx,0,d5)
            p9=Base.Vector(Lx,0,d2)
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d5), None, QtGui.QApplication.UnicodeUTF8))
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plst)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        
        elif key=='14':#短管１号---------------------------------------------------
            sa=T_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d5=float(sa[3])/2
            P=sa[4]
            d3=d5-4
            d4=d3-(0.6*P-10)*math.tan(math.radians(3))
            d6=d4-10
            x1=(d4-d6)*math.sqrt(2)
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            c1=c00
            sa=T_Data.flngs[key_1]
            flng(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            c2=c01
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            k=sa[5]-sa[6]
            x1=m+k
            sa1=T_Data.tnkns[dia]
            L1=sa1[0]
            c2.Placement=App.Placement(App.Vector(P+L1,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            x=P+L1-x1-L0

            c3 = Part.makeCylinder(d2,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d0,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.fuse(c3)

        
        elif key=='15':#短管2号---------------------------------------------------
            sa=T_Data.flngs[key_1]
            flng(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            c1=c01
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            x1=m+k
            sa1=T_Data.tnkns[dia]
            L2=sa1[1]
            x=L2-x1

            c2 = Part.makeCylinder(d2,x,Base.Vector(x1,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,x,Base.Vector(x1,0,0),Base.Vector(1,0,0))
            c2=c2.cut(c3)
            c1=c1.fuse(c2)
        
        elif key=='16':#栓 プラグ---------------------------------------------------
            sa1=T_Data.tnkns[dia]
            k=sa1[2]
            Lx=sa1[3]
            d0=float(sa1[4])/2
            d2=float(sa1[5])/2
            d5=float(sa1[6])/2
            p1=(0,0,0)
            p2=(0,0,d5)
            p3=(k,0,d5-5)
            p4=(k,0,d2)
            p5=(Lx,0,d2)
            p6=(Lx,0,d0)
            p7=(k,0,d0)
            p8=(k,0,0)
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            w10=Part.makePolygon(plst)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        label='mass[kg]'
        g0=7.15
        g=c1.Volume*g0*1000/10**9  
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