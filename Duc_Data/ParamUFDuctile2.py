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
from . import UF_Data

doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
#JPDA G 3003

class uf_ductile:
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
        def socket(self):#ソケット UF 直管---------------------------------------------------------------------------------------
            global c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            Y=float(sa[3])
            P=sa[4]
            d3=d5*0.97
            x=(d3-d2)*math.sqrt(3)
            L0=P+x
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(P,0,d3)
            p4=Base.Vector(L0,0,d2)
            p5=Base.Vector(L0,0,d0)
            p6=Base.Vector(P,0,d0)
            p7=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)

        def socketKF2(self):#ソケット 異形管 NS---------------------------------------------------------------------------------------
            global c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            s=2
            s1=P/4
            y0=P-s1
            d3=d5*0.97
            d4=d3-y0*math.tan(math.radians(3))
            x=(d4-d2)*math.sqrt(3)
            L0=P+x
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d2), None, QtGui.QApplication.UnicodeUTF8))
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(s1,0,d5)
            p4=Base.Vector(s1,0,d5-10)
            p5=Base.Vector(P/2,0,d5-10)
            p6=Base.Vector(P/2,0,d5)
            p7=Base.Vector(P*3/4,0,d5)
            p8=Base.Vector(P*7/8,0,d4)
            p9=Base.Vector(P,0,d4)
            p10=Base.Vector(P+x,0,d2)
            p11=Base.Vector(P+x,0,d0)
            p12=Base.Vector(P,0,d0)
            p13=Base.Vector(P,0,d2)

            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)
        def socketUF(self):#ソケット 異形管UF------------------------------------------------------------------------------
            global c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d3=d5*0.95
            x1=P*0.3
            x2=P-x1
            x3=(d3-d2)*math.sqrt(3)
            L0=P+x3
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(x1,0,d5)
            p4=Base.Vector(x1,0,d3)
            p5=Base.Vector(P,0,d3)
            p6=Base.Vector(L0,0,d2)
            p7=Base.Vector(L0,0,d0)
            p8=Base.Vector(P,0,d0)
            p9=Base.Vector(P,0,d2)

            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)

        def socketKF(self):#ソケット 異形管NS----------------------------------------------------------------------------------
            global c00
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=float(sa[3])
            d4=float(sa[4])/2
            E0=float(sa[5])/2
            k=sa[6]
            L=sa[7]
            d3=d4-(E0+5)
            d1=(d3+d2)/2
            y1=(d1-d2)*math.sqrt(3)
            y2=(d3-d1)*math.sqrt(3)
            L0=(P+y1)
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(k,0,d5)
            p4=Base.Vector(k,0,d3)
            p5=Base.Vector(P/2,0,d3)
            p6=Base.Vector(P/2+y2,0,d1)
            p7=Base.Vector(P,0,d1)
            p8=Base.Vector(L0,0,d2)
            p9=Base.Vector(L0,0,d0)
            p10=Base.Vector(P,0,d0)
            p11=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)
        #self.label_7.setText(QtGui.QApplication.translate("Dialog", "", None))
        if key=='00' :#---------------------------------------------------------------
            b='UF_Straight tube'
            sa=UF_Data.rcvd[key_1]
            socket(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            Y=float(sa[3])
            P=sa[4]
            d3=d5*0.97
            x=(d3-d2)*math.sqrt(3)
            L0=P+x
            c1=c00
            L=App.ActiveDocument.getObject(label).L
            L=float(L)
            c2 = Part.makeCylinder(d2,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            c1=c1.cut(c3)
    
        elif key=='01' or key=='02':
            if key=='01':
                sa=UF_Data.trcts[dia]
            elif key=='02':
                sa=UF_Data.trcts2[dia]
            H=sa[0]
            I=sa[1]
            J=sa[2]
            LL=sa[3]
            sa=UF_Data.rcvdUF[key_1]
            socketUF(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d3=d5*0.95
            x1=P*0.3
            x2=P-x1
            x3=(d3-d2)*math.sqrt(3)
            L0=P+x3
            c1=c00
            P0=P
            d02=d2
            d00=d0
            L00=L0
            if float(key_2)<=700:
                sa=UF_Data.rcvdNS[key_2]
                socketKF(self)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                P=float(sa[3])
                d4=float(sa[4])/2
                E0=float(sa[5])/2
                k=sa[6]

            elif float(key_2)>700:
                sa=UF_Data.rcvdUF[key_2]
                socketUF(self)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                P=sa[3]
                d3=d5*0.95
                x1=P*0.3
                x2=P-x1
                x3=(d3-d2)*math.sqrt(3)
                L0=P+x3
            c2=c00
            c2.Placement=App.Placement(App.Vector(P0+H,P+I,0),App.Rotation(App.Vector(0,0,1),-90))

            c11 = Part.makeCylinder(d02,P0+LL-L00,Base.Vector(L00,0,0),Base.Vector(1,0,0))
            c12 = Part.makeCylinder(d00,P0+LL-L00,Base.Vector(L00,0,0),Base.Vector(1,0,0))
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
                c4 = Part.makeCylinder(d2,2*I,Base.Vector(P0+H,-I,0),Base.Vector(0,1,0))
                c5 = Part.makeCylinder(d0,2*I,Base.Vector(P0+H,-I,0),Base.Vector(0,1,0))
                c1=c1.fuse(c4)
                c1=c1.cut(c5)
                c1=c1.cut(c12)
    

        elif key=='03' or key=='04':#---------------------------------------------------------------
            if key=='03':
                if float(key_1)<=700:
                    sa=UF_Data.rcvdNS[key_1]
                    socketKF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=float(sa[3])
                    d4=float(sa[4])/2
                    E0=float(sa[5])/2
                    k=sa[6]
                elif float(key_1)>700:
                    sa=UF_Data.rcvdUF[key_1]
                    socketUF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=sa[3]
                    d3=d5*0.95
                    x1=P*0.3
                    x2=P-x1
                    x3=(d3-d2)*math.sqrt(3)
                    L0=P+x3
                    d0=float(sa[0])/2
                c1=c00
                d00=d0
                d02=d2
                L00=L0
                P0=P
                if float(key_2)<=700:
                    sa=UF_Data.rcvdNS[key_2]
                    socketKF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=float(sa[3])
                    d4=float(sa[4])/2
                    E0=float(sa[5])/2
                    k=sa[6]
                elif float(key_2)>700:
                    sa=UF_Data.rcvdUF[key_2]
                    socketUF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=sa[3]
                    d3=d5*0.95
                    x1=P*0.3
                    x2=P-x1
                    x3=(d3-d2)*math.sqrt(3)
                    L0=P+x3
                sa1=UF_Data.trcts3[dia]
                A0=P0/2
                B=sa1[1]
                C=sa1[2]
                E=P
                L1=sa1[4]
                L2=sa1[5]
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
                if float(key_2)<=700:
                    sa=UF_Data.rcvdNS[key_2]
                    socketKF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=float(sa[3])
                    d4=float(sa[4])/2
                    E0=float(sa[5])/2
                    k=sa[6]
                    #L=sa[7]
                    d3=d4-(E0+5)
                    d1=(d3+d2)/2
                    y1=(d1-d2)*math.sqrt(3)
                    y2=(d3-d1)*math.sqrt(3)
                    L0=(P+y1)
                elif float(key_2)>700:
                    sa=UF_Data.rcvdUF[key_2]
                    socketUF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=sa[3]
                    d3=d5*0.95
                    x1=P*0.3
                    x2=P-x1
                    x3=(d3-d2)*math.sqrt(3)
                    L0=P+x3
                c1=c00
                d00=d0
                d02=d2
                L00=L0
                P0=P
                if float(key_1)<=700:
                    sa=UF_Data.rcvdNS[key_1]
                    socketKF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=float(sa[3])
                    d4=float(sa[4])/2
                    E0=float(sa[5])/2
                    k=sa[6]
                    #L=sa[7]
                    d3=d4-(E0+5)
                    d1=(d3+d2)/2
                    y1=(d1-d2)*math.sqrt(3)
                    y2=(d3-d1)*math.sqrt(3)
                    L0=(P+y1)
                elif float(key_1)>700:
                    sa=UF_Data.rcvdUF[key_1]
                    socketUF(self)
                    d0=float(sa[0])/2
                    d5=float(sa[1])/2
                    d2=float(sa[2])/2
                    P=sa[3]
                    d3=d5*0.95
                    x1=P*0.3
                    x2=P-x1
                    x3=(d3-d2)*math.sqrt(3)
                    L0=P+x3
                sa1=UF_Data.trcts3[dia]
                A0=P0/2
                B=sa1[1]
                C=sa1[2]
                E=P
                L1=sa1[4]
                L2=sa1[5]
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
                c1.Placement=App.Placement(App.Vector(L2+P,0,0),App.Rotation(App.Vector(0,0,1),180))

        elif key=='05' or key=='06' or key=='07' or key=='08' or key=='09':#両受曲管-----------------------------------------
            sa=UF_Data.rcvdUF[key_1]
            socketUF(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d3=d5*0.95
            x1=P*0.3
            x2=P-x1
            x3=(d3-d2)*math.sqrt(3)
            L0=P+x3
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
            if key=='05':#90
                sa1=UF_Data.two_t_90[key_1]
                b='UF_90Elbow_'
            elif key=='06':#45
                sa1=UF_Data.two_t_45[key_1]
                b='UF_45Elbow_'
            elif key=='07':#22
                sa1=UF_Data.two_t_22[key_1]
                b='UF_22Elbow_'
            elif key=='08':#11
                sa1=UF_Data.two_t_11[key_1]
                b='UF_11Elbow_'
            elif key=='09':#45
                sa1=UF_Data.two_t_5[key_1]
                b='UF_5Elbow_'
            R=sa1[0]
            L1=sa1[1]
            L2=L1
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
            c1.Placement=App.Placement(App.Vector(0,-(P+L1),0),App.Rotation(App.Vector(0,0,1),90))
            p1=(0,-(L1-a0),0)
            p2=(0,-R*math.tan(math.radians(s)),0)
            p3=(x,-y3,0)
            p4=(x1,y2,0)
            p5=((L1-a0)*math.cos(math.radians(90-2*s)),(L1-a0)*math.sin(math.radians(90-2*s)),0)
            p6=((L1-a0)*math.cos(math.radians(90-2*s))+L0*math.cos(math.radians(90-2*s)),(L1-a0)*math.sin(math.radians(90-2*s))+L0*math.sin(math.radians(90-2*s)),0)
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

            sa=UF_Data.rcvdUF[key_1]
            socketUF(self)

            c10=c00
            c10.Placement=App.Placement(App.Vector(p6),App.Rotation(App.Vector(0,0,1),-2*s-90))
            c1=c1.fuse(c10)

        elif key=='10' or key=='11' or key=='12' or key=='13' or key=='14':#曲管-----------------------------------------
            sa=UF_Data.rcvdUF[key_1]
            socketUF(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d3=d5*0.95
            x1=P*0.3
            x2=P-x1
            x3=(d3-d2)*math.sqrt(3)
            L0=P+x3
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
            if key=='10':#90
                sa1=UF_Data.elbows_90[key_1]
                b='UF_90Elbow_'
            elif key=='11':#45
                sa1=UF_Data.elbows_45[key_1]
                b='UF_45Elbow_'
            elif key=='12':#22 1/2
                sa1=UF_Data.elbows_22[key_1]
                b='UF_22Elbow_'
            elif key=='13':#11 1/4
                sa1=UF_Data.elbows_11[key_1]
                b='UF_11Elbow_'
            elif key=='14':#5 5/8
                sa1=UF_Data.elbows_5[key_1]
                b='UF_5Elbow_'
            R=sa1[0]
            L1=sa1[1]
            L2=sa1[2]
            Y=sa1[3]
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
            c1.Placement=App.Placement(App.Vector(0,-(P-Y+L1),0),App.Rotation(App.Vector(0,0,1),90))
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
    
        elif key=='15' or key=='16':#-----------------------------------------------------------------------------------
            if key=='15':
                b='UF_Gate_valve_secondary pipe_A1_'
                sa=UF_Data.rcvdUF[key_1]
                socketUF(self)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                P=sa[3]
                d3=d5*0.95
                x1=P*0.3
                x2=P-x1
                x3=(d3-d2)*math.sqrt(3)
                L0=P+x3
                c1=c00
                #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(a), None))
                d00=d0
                d02=d2
                P0=P
                sa=UF_Data.flngs[key_1]
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
                sa=UF_Data.flngs[key_2]
                flng(self)
                d0=float(sa[0])/2
                d2=float(sa[1])/2
                d3=float(sa[2])/2
                d4=float(sa[3])/2
                d5=float(sa[4])/2
                k=sa[5]-sa[6]
                m=sa[6]
                n=sa[7]
                c3=c01
                sa1=UF_Data.gvsps[dia]
                B=sa1[0]
                H=sa1[1]
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
            elif key=='16':
                b='UF_Gate_valve_secondary pipe_A2_'
                sa=UF_Data.flngs[key_1]
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
                d00=d0
                d02=d2
                x01=m+k
                sa=UF_Data.flngs[key_2]
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
                sa1=UF_Data.gvsps2[dia]
                B=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L2=sa1[3]
                x1=m+k
                J=L2-B
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

        elif key=='17'  :#-----------------------------
            if key=='17':
                sa1=UF_Data.ttfs[dia]
                H=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L=sa1[3]
                b='UF_T-shaped tube with flange'
                sa=UF_Data.rcvdUF[key_1]
                socketUF(self)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                P=sa[3]
                d3=d5*0.95
                x1=P*0.3
                x2=P-x1
                x3=(d3-d2)*math.sqrt(3)
                L0=P+x3
                c1=c00
                #Part.show(c1)
                d00=d0
                d02=d2
                P0=P
                L00=L0
                x=P0+H+J-L00
                c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                sa=UF_Data.flngs[key_2]
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
                h=sa[14]
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

        elif key=='18':#排水T字管---------------------------------------------------
            sa=UF_Data.rcvdUF[key_1]
            socketUF(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d3=d5*0.95
            x1=P*0.3
            x2=P-x1
            x3=(d3-d2)*math.sqrt(3)
            L0=P+x3
            c1=c00
            P0=P
            d00=d0
            d02=d2
            socketUF(self)
            c2=c00
            sa1=UF_Data.dtps[dia]
            H=sa1[0]
            I=sa1[1]
            Lx=sa1[2]
            x=2*P0+Lx
            x1=Lx+2*P0-2*L0
            c2.Placement=App.Placement(App.Vector(x,0,0),App.Rotation(App.Vector(0,0,1),180))
            c3 = Part.makeCylinder(d02,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d00,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            #Part.show(c3)
            sa=UF_Data.rcvdNS[key_2]
            socketKF(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=float(sa[3])
            d4=float(sa[4])/2
            E0=float(sa[5])/2
            k=sa[6]
            c5=c00
            c5.Placement=App.Placement(App.Vector(P0+H,I+P,-(d02-d2)),App.Rotation(App.Vector(0,0,1),-90))
            c1=c1.fuse(c5)
            x=I+P-L0
            c6 = Part.makeCylinder(d2,I,Base.Vector(P0+H,0,-(d02-d2)),Base.Vector(0,1,0))
            c61 = Part.makeCylinder(d0,I,Base.Vector(P0+H,0,-(d02-d2)),Base.Vector(0,1,0))
            c6=c6.cut(c61)
            c1=c1.fuse(c6)
            c1=c1.fuse(c3)
            c1=c1.cut(c4)
            c1=c1.cut(c61)

        elif key=='19':#短管１号---------------------------------------------------
            sa=UF_Data.rcvdUF[key_1]
            socketUF(self)
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            P=sa[3]
            d3=d5*0.95
            x1=P*0.3
            x2=P-x1
            x3=(d3-d2)*math.sqrt(3)
            L0=P+x3
            c1=c00
            sa=UF_Data.flngs[key_1]
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
            sa1=UF_Data.tnkns[dia]
            L1=sa1[0]
            c2.Placement=App.Placement(App.Vector(P+L1,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            x=P+L1-x1-L0
            c3 = Part.makeCylinder(d2,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d0,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.fuse(c3)

        elif key=='20':#短管2号---------------------------------------------------
            sa=UF_Data.flngs[key_1]
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
            sa1=UF_Data.tnkns[dia]
            L2=sa1[1]
            x=L2-x1
            c2 = Part.makeCylinder(d2,x,Base.Vector(x1,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,x,Base.Vector(x1,0,0),Base.Vector(1,0,0))
            c2=c2.cut(c3)
            c1=c1.fuse(c2)
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        obj.Shape=c1
