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
from . import U_Data

doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
#JDPA G 3006
class u_ductile:
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
        def socket(self):#ソケット 直管 -----------------------------------------------------------------------------------------------
            global c00
            global Y
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=float(sa[3])
            Y=sa[4]
            L=sa[5]
            x=(d5-d2)*math.sqrt(3)
            L0=P+x
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(P,0,d5)
            p4=Base.Vector(L0,0,d2)
            p5=Base.Vector(L0,0,d0)
            p6=Base.Vector(P,0,d0)
            p7=Base.Vector(P,0,d2)
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            plist=[p1,p2,p3,p4,p5,p6,p7,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)

        def socket1(self):#ソケット 異形管 -----------------------------------------------------------------------------------------------
            global c00
            global d2
            global d0
            global L0
            global P
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=float(sa[3])
            Y=sa[4]
            k=0.1*P
            x1=10
            x=(d5-d2)*math.sqrt(2)
            L0=P+x
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5+x1)
            p3=Base.Vector(k,0,d5+x1)
            p4=Base.Vector(k,0,d5)
            p5=Base.Vector(P,0,d5)
            p6=Base.Vector(L0,0,d2)
            p7=Base.Vector(L0,0,d0)
            p8=Base.Vector(P,0,d0)
            p9=Base.Vector(P,0,d2)
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)

        def socket2(self):#k形ソケット-----------------------------------------------------------------------------------------------
            global d00
            global d0
            global d1
            global d2
            global d3
            global d4
            global d5
            global L0
            global L00
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
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            d4=float(sa[3])/2
            k=sa[4]
            E0=sa[5]/2
            P=sa[6]
            x1=P-k
            s=3
            d3=d4-(E0+5)
            d6=d3-x1*math.tan(math.radians(s))
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(k,0,d5)
            p4=Base.Vector(k,0,d3)
            p5=Base.Vector(P,0,d6)
            p6=Base.Vector(L0,0,d2)
            p7=Base.Vector(L0,0,d0)
            p8=Base.Vector(P,0,d0)
            p9=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)

        if key=='00' or key=='17':#直管---------------------------------------------------------------
            if key=='00':
                b='U_Straight tube'
                sa=U_Data.rcvd[key_1]
                socket(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d5=float(sa[2])/2
                P=float(sa[3])
                Y=sa[4]
                L=sa[5]
                x=(d5-d2)*math.sqrt(3)
                L0=P+x
                c1=c00
                #d00=d0
                d02=d2
                M=sa[7]
                x1=sa[8]
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                c2 = Part.makeCylinder(d2,L-(L0-P+Y),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d0,L-(L0-P+Y),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
                c1=c1.cut(c3)
                #Part.show(c1)
                for i in range(4):
                    cs0 = Part.makeCylinder(d02+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    cs1 = Part.makeCylinder(d02,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    c11=cs0.cut(cs1)
                    c11.Placement=App.Placement(App.Vector(L+P-Y-(M+x1),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                    #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(x1), None, QtGui.QApplication.UnicodeUTF8))
                    c1=c1.fuse(c11)

            elif key=='17':
                b='U_Straight tube'
                sa=U_Data.rcvd[key_1]
                d0=sa[0]/2
                d2=sa[1]/2
                M=sa[7]
                x1=sa[8]
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                c1 = Part.makeCylinder(d2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d0), None, QtGui.QApplication.UnicodeUTF8))
                #Part.show(c1)
                for i in range(4):
                    cs0 = Part.makeCylinder(d2+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    cs1 = Part.makeCylinder(d2,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    c11=cs0.cut(cs1)
                    c11.Placement=App.Placement(App.Vector(L-(M+x1),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                    c11=c11.fuse(c11)
                    c1=c1.fuse(c11)

                for i in range(4):
                    cs0 = Part.makeCylinder(d2+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    cs1 = Part.makeCylinder(d2,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    c11=cs0.cut(cs1)
                    c11.Placement=App.Placement(App.Vector(x1,0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                    c11=c11.fuse(c11)
                    c1=c1.fuse(c11)
        
        elif key=='01' or key=='02':
            if key=='01':
                sa=U_Data.trcts[dia]
            elif key=='02':
                sa=U_Data.trcts2[dia]

            H=sa[0]
            I=sa[1]
            J=sa[2]
            LL=sa[3]

            sa=U_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=float(sa[3])
            Y=sa[4]
            k=0.1*P
            x1=10
            x=(d5-d2)*math.sqrt(2)
            L0=P+x
            c1=c00
            P0=P
            d02=d2
            d00=d0
            M=sa[7]
            x1=sa[8]

            if float(key_2)<=700:
                sa=U_Data.rcvd2[key_2]
                socket2(self)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                d4=float(sa[3])/2
                k=sa[4]
                E0=sa[5]/2
                P=sa[6]
                x1=P-k
                s=3
                d3=d4-(E0+5)
                d6=d3-x1*math.tan(math.radians(s))
                x=(d6-d2)*math.sqrt(3)
                L0=P+x
                c2=c00
                c2.Placement=App.Placement(App.Vector(P0+H-Y,P+I,0),App.Rotation(App.Vector(0,0,1),-90))
            else:
                sa=U_Data.rcvd1[key_2]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d5=float(sa[2])/2
                P=float(sa[3])
                Y=sa[4]
                k=0.1*P
                x1=10
                x=(d5-d2)*math.sqrt(2)
                L0=P+x
                c2=c00
                c2.Placement=App.Placement(App.Vector(P0+H-Y,P+I-Y,0),App.Rotation(App.Vector(0,0,1),-90))

            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            c11 = Part.makeCylinder(d02,P0+LL-Y-L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c12 = Part.makeCylinder(d00,P0+LL-Y-L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))

            c1=c1.fuse(c2)
            c1=c1.fuse(c11)

            if key=='01':
                c3=c00
                c3.Placement=App.Placement(App.Vector(P0+H-Y,-(P+I),0),App.Rotation(App.Vector(0,0,1),90))
                c1=c1.fuse(c3)
            if key=='02':
                c4 = Part.makeCylinder(d2-0.1,I,Base.Vector(P0+H-Y,0,0),Base.Vector(0,1,0))
                c5 = Part.makeCylinder(d0,I,Base.Vector(P0+H-Y,0,0),Base.Vector(0,1,0))
                c1=c1.fuse(c4)
                c1=c1.cut(c5)
                c1=c1.cut(c12)

                for i in range(4):
                    cs0 = Part.makeCylinder(d02+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    cs1 = Part.makeCylinder(d02,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    c111=cs0.cut(cs1)
                    c111.Placement=App.Placement(App.Vector(LL+P0-Y-(M+x1),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                    #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(x1), None, QtGui.QApplication.UnicodeUTF8))
                    c1=c1.fuse(c111)

            elif key=='01':
                #Part.show(c1)
                c4 = Part.makeCylinder(d2,2*I,Base.Vector(P0+H-Y,-I,0),Base.Vector(0,1,0))
                c5 = Part.makeCylinder(d0,2*I,Base.Vector(P0+H-Y,-I,0),Base.Vector(0,1,0))
                c1=c1.fuse(c4)
                c1=c1.cut(c5)
                c1=c1.cut(c12)

                for i in range(4):
                    cs0 = Part.makeCylinder(d02+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    cs1 = Part.makeCylinder(d02,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    c111=cs0.cut(cs1)
                    c111.Placement=App.Placement(App.Vector(LL+P0-Y-(M+x1),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                    #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(x1), None))
                    c1=c1.fuse(c111)

        elif key=='03' or key=='04':#---------------------------------------------------------------
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
            sa=U_Data.rcvd1[key_1]
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=float(sa[3])
            Y=sa[4]
            k=0.1*P
            x1=10
            x=(d5-d2)*math.sqrt(2)
            L0=P+x
            c1=c00
            d00=d0
            d02=d2
            L00=L0
            P0=P
            Y0=Y
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            M=sa[7]
            x1=sa[8]
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(M), None, QtGui.QApplication.UnicodeUTF8))
            if float(key_2)<=700:
                sa=U_Data.rcvd2[key_2]
                socket2(self)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                d4=float(sa[3])/2
                k=sa[4]
                E0=sa[5]/2
                P=sa[6]
                x1=P-k
                s=3
                d3=d4-(E0+5)
                d6=d3-x1*math.tan(math.radians(s))
                x=(d6-d2)*math.sqrt(3)
                L0=P+x
                c2=c00
            else:
                sa=U_Data.rcvd1[key_2]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d5=float(sa[2])/2
                P=float(sa[3])
                Y=sa[4]
                k=0.1*P
                x1=10
                x=(d5-d2)*math.sqrt(2)
                L0=P+x
                c2=c00
            sa1=U_Data.trcts3[dia]
            A0=sa1[0]
            B=sa1[1]
            C=sa1[2]
            E=sa1[3]
            L1=sa1[4]-Y0
            L2=sa1[5]-Y

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
                if float(key_2)>700:
                    for i in range(4):
                        cs0 = Part.makeCylinder(d2+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                        cs1 = Part.makeCylinder(d2,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                        c111=cs0.cut(cs1)
                        c111.Placement=App.Placement(App.Vector(L1+P0-(M+x1),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                        c1=c1.fuse(c111)

            elif key=='04':
                if float(key_2)<=700:
                    sa=U_Data.rcvd2[key_2]
                    socket2(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    d4=float(sa[3])/2
                    k=sa[4]
                    E0=sa[5]/2
                    P=sa[6]
                    x1=P-k
                    s=3
                    d3=d4-(E0+5)
                    d6=d3-x1*math.tan(math.radians(s))
                    x=(d6-d2)*math.sqrt(3)
                    L0=P+x
                    L2=sa1[5]
                elif float(key_2)>700:
                    sa=U_Data.rcvd1[key_2]
                    socket1(self)
                    d0=float(sa[0])/2
                    d2=float(sa[1])/2
                    d5=float(sa[2])/2
                    P=float(sa[3])
                    Y=sa[4]
                    k=0.1*P
                    x1=10
                    x=(d5-d2)*math.sqrt(2)
                    L0=P+x
                    L2=sa1[5]-Y
                c1=c00
                d00=d0
                d02=d2
                L00=L0
                P0=P
                if float(key_1)<=700:
                    sa=U_Data.rcvd2[key_1]
                    socket2(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    d4=float(sa[3])/2
                    k=sa[4]
                    E0=sa[5]/2
                    P=sa[6]
                    x1=P-k
                    s=3
                    d3=d4-(E0+5)
                    d6=d3-x1*math.tan(math.radians(s))
                    x=(d6-d2)*math.sqrt(3)
                    L0=P+x
                elif float(key_1)>700:
                    sa=U_Data.rcvd1[key_1]
                    socket1(self)
                    d0=float(sa[0])/2
                    d2=float(sa[1])/2
                    d5=float(sa[2])/2
                    P=float(sa[3])
                    Y=sa[4]
                    k=0.1*P
                    x1=10
                    x=(d5-d2)*math.sqrt(2)
                    L0=P+x
                x0=L2-(E+C)
                p1=(L00,0,d00)
                p2=(L00,0,d02)
                p3=(P0+E,0,d02)
                p4=(P0+E+x0,0,d2)
                p5=(P0+E+x0+C,0,d2)
                p6=(P0+L2,0,d0)
                p7=(P0+E+x0,0,d0)
                p8=(P0+E,0,d00)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c5=wface.revolve(Base.Vector(0,0,0),Base.Vector(1.0,0.0,0.0),360)
                c1=c1.fuse(c5)
                c1.Placement=App.Placement(App.Vector(L2+P0,0,0),App.Rotation(App.Vector(0,0,1),180))

                if float(key_1)>700:
                    for i in range(4):
                        cs0 = Part.makeCylinder(d2+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                        cs1 = Part.makeCylinder(d2,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                        c111=cs0.cut(cs1)
                        c111.Placement=App.Placement(App.Vector(x1,0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                        #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                        c1=c1.fuse(c111)

        elif key=='05' or key=='06' or key=='07' or key=='08' or key=='09':#曲管-----------------------------------------
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
            sa=U_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=float(sa[3])
            Y=sa[4]
            k=0.1*P
            x1=10
            x=(d5-d2)*math.sqrt(2)
            L0=P+x
            M=sa[7]
            x0=sa[8]
            c1=c00
            #Part.show(c1)
            #c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
            if key=='05':#90
                sa1=U_Data.elbows_90[key_1]
                b='U_90Elbow_'
            elif key=='06':#45
                sa1=U_Data.elbows_45[key_1]
                b='U_45Elbow_'
            elif key=='07':#22 1/2
                sa1=U_Data.elbows_22[key_1]
                b='U_22Elbow_'
            elif key=='08':#11 1/4
                sa1=U_Data.elbows_11[key_1]
                b='U_11Elbow_'
            elif key=='09':#5 5/8
                sa1=U_Data.elbows_5[key_1]
                b='U_5Elbow_'

            R=sa1[0]
            L1=sa1[1]-Y
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
            edge3=Part.makeLine(p5,p4)
            aWire = Part.Wire([edge1,edge2,edge3])
            #Part.show(aWire)
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

            for i in range(4):
                cs0 = Part.makeCylinder(d2+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                cs1 = Part.makeCylinder(d2,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                c111=cs0.cut(cs1)
                c111.Placement=App.Placement(App.Vector(L2-(M+x0),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                c111=c111.fuse(c111)
                c111.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),(90-2*s)))
                c1=c1.fuse(c111)

        elif key=='10' or key=='11':#-----------------------------------------------------------------------------------
            if key=='10':
                b='U_Gate_valve_secondary pipe_A1_'
                sa=U_Data.rcvd1[key_1]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d5=float(sa[2])/2
                P=float(sa[3])
                Y=sa[4]
                k=0.1*P
                x1=10
                x=(d5-d2)*math.sqrt(2)
                L0=P+x
                c1=c00
                #Part.show(c1)
                d00=d0
                d02=d2
                P0=P
                #Part.show(c1)
                sa=U_Data.flngs[key_1]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                LL2=sa[8]
                c2=c01
                #Part.show(c2)
                sa=U_Data.flngs[key_2]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                LL2=sa[8]
                c3=c01
                sa1=U_Data.gvsps[dia]
                B=sa1[0]
                H=sa1[1]-Y
                I=sa1[2]

                c2.Placement=App.Placement(App.Vector(P0+H+B,0,0),App.Rotation(App.Vector(0,0,1),180))
                c1=c1.fuse(c2)
                c3.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c1=c1.fuse(c3)
                x1=m+k
                x2=P+H+B-(L0+x1)
                x=P+H+B-(L0)
                c4 = Part.makeCylinder(d02,x2,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c4)
                c5 = Part.makeCylinder(d2,I-x1,Base.Vector(x1,0,0),Base.Vector(1,0,0))
                c5.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c1=c1.fuse(c5)
                c45 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c45)
                c55 = Part.makeCylinder(d0,I,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c55.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c1=c1.cut(c55)
            elif key=='11':
                b='U_Gate_valve_secondary pipe_A2_'
                sa=U_Data.flngs[key_1]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                LL2=sa[8]
                c1=c01
                d00=d0
                d02=d2
                x01=m+k
                sa=U_Data.flngs[key_2]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                LL2=sa[8]
                c2=c01
                sa1=U_Data.gvsps2[dia]
                B=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L2=sa1[3]
                sa=U_Data.rcvd1[key_1]
                M=sa[7]
                x0=sa[8]
                x1=m+k
                x=B+J-(m+k)
                c2.Placement=App.Placement(App.Vector(B,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c1=c1.fuse(c2)
                c3 = Part.makeCylinder(d02,L2-x01,Base.Vector(x01,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c3)
                c4 = Part.makeCylinder(d2,(I-x1),Base.Vector(B,0,0),Base.Vector(0,1,0))
                c1=c1.fuse(c4)
                c5 = Part.makeCylinder(d00,L2-x01,Base.Vector(x01,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c5)
                c6 = Part.makeCylinder(d0,I-x1,Base.Vector(B,0,0),Base.Vector(0,1,0))
                c1=c1.cut(c6)

                for i in range(4):
                    cs0 = Part.makeCylinder(d02+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    cs1 = Part.makeCylinder(d02,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    c11=cs0.cut(cs1)
                    c11.Placement=App.Placement(App.Vector(L2-(M+x0),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                    c11=c11.fuse(c11)
                    c1=c1.fuse(c11)

        elif key=='12' or key=='13':#-----------------------------------------------------------------------------------
            if key=='12':
                b='U_T-shaped tube with flange_'
                sa=U_Data.rcvd1[key_1]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d5=float(sa[2])/2
                P=float(sa[3])
                Y=sa[4]
                k=0.1*P
                x1=10
                x=(d5-d2)*math.sqrt(2)
                L0=P+x
                c1=c00
                d00=d0
                d02=d2
                P0=P
                L00=L0
                M=sa[7]
                x0=sa[8]
                sa1=U_Data.ttfs[dia]
                H=sa1[0]-Y
                I=sa1[1]
                J=sa1[2]
                L=sa1[3]
                x=P0+H+J-L00
                c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                sa=U_Data.flngs[key_2]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                LL2=sa[8]
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
                for i in range(4):
                    cs0 = Part.makeCylinder(d02+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    cs1 = Part.makeCylinder(d02,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                    c11=cs0.cut(cs1)
                    c11.Placement=App.Placement(App.Vector(L+(P0-Y)-(M+x0),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                    c11=c11.fuse(c11)
                    c1=c1.fuse(c11)
            elif key=='13':#排水T字管---------------------------------------------------

                b='U_Drainage T-shaped pipe_'
                sa=U_Data.rcvd1[key_1]
                socket1(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d5=float(sa[2])/2
                P=float(sa[3])
                Y=sa[4]
                k=0.1*P
                x1=10
                x=(d5-d2)*math.sqrt(2)
                L0=P+x
                c1=c00
                P0=P
                d00=d0
                d02=d2
                socket1(self)
                c2=c00
                sa1=U_Data.dtps[dia]
                H=sa1[0]-Y
                I=sa1[1]
                L=sa1[2]
                #Part.show(c1)
                x=2*P0+L-2*Y
                x1=L+2*P0-2*L0
                c2.Placement=App.Placement(App.Vector(x,0,0),App.Rotation(App.Vector(0,0,1),180))
                c3 = Part.makeCylinder(d02,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c4 = Part.makeCylinder(d00,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
                #Part.show(c1)

                sa=U_Data.rcvd2[key_2]
                socket2(self)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                d4=float(sa[3])/2
                k=sa[4]
                E0=sa[5]/2
                P=sa[6]
                x1=P-k
                s=3
                d3=d4-(E0+5)
                d6=d3-x1*math.tan(math.radians(s))
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

        elif key=='14':#継輪-----------------------------------------------------
            sa=U_Data.rcvd1[key_1]
            d2=sa[1]/2
            d5=sa[2]/2
            L=sa[6]
            #socket(self)
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(L,0,d5)
            p4=Base.Vector(L,0,d2)

            plst=[p1,p2,p3,p4,p1]
            w10=Part.makePolygon(plst)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)

        elif key=='15':#短管１号---------------------------------------------------
            sa=U_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=float(sa[3])
            Y=sa[4]
            k=0.1*P
            x1=10
            x=(d5-d2)*math.sqrt(2)
            L0=P+x
            c1=c00
            sa=U_Data.flngs[key_1]
            flng(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            LL2=sa[8]
            c2=c01
            x1=m+k
            sa1=U_Data.tnkns[dia]
            L1=sa1[0]-Y
            c2.Placement=App.Placement(App.Vector(P+L1,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            x=P+L1-x1-L0
            c3 = Part.makeCylinder(d2,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d0,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.fuse(c3)

        elif key=='16':#短管2号---------------------------------------------------
            sa=U_Data.flngs[key_1]
            flng(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            n=sa[7]
            LL2=sa[8]
            c1=c01
            x1=m+k
            sa1=U_Data.tnkns[dia]
            L2=sa1[1]
            x=L2-x1
            c2 = Part.makeCylinder(d2,x,Base.Vector(x1,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,x,Base.Vector(x1,0,0),Base.Vector(1,0,0))
            c2=c2.cut(c3)
            c1=c1.fuse(c2)
            sa=U_Data.rcvd1[key_1]
            M=sa[7]
            x0=sa[8]

            for i in range(4):
                cs0 = Part.makeCylinder(d2+16,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                cs1 = Part.makeCylinder(d2,M,Base.Vector(0,0,0),Base.Vector(1,0,0),30)
                c11=cs0.cut(cs1)
                c11.Placement=App.Placement(App.Vector(L2-(M+x0),0,0),App.Rotation(App.Vector(1,0,0),-15+i*90))
                c11=c11.fuse(c11)
                c1=c1.fuse(c11)
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
