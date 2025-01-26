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
from . import GX_Data
doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
#JDPA G 1049
class gx_ductile:
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
        def socket(self):#ソケット 直管75～400---------------------------------------------------------------------------------------
            global c00
          
            d0=float(sa[0])/2
            d5=float(sa[1])/2
            d2=float(sa[2])/2
            Y=float(sa[3])
            P=sa[4]
            L=sa[5]
            d3=d5*0.95
            d4=d3*0.95
            y=d4-d2
            x=y/math.tan(math.radians(20))
            y1=d5-d3
            y2=d3-d4
            x1=2*y1
            x2=2*y2
            L0=P+x
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(30,0,d5)
            p4=Base.Vector(30+x1,0,d3)
            p5=Base.Vector(P/2,0,d3)
            p6=Base.Vector(P/2+x2,0,d4)
            p7=Base.Vector(P,0,d4)
            p8=Base.Vector(L0,0,d2)
            p9=Base.Vector(L0,0,d0)
            p10=Base.Vector(P,0,d0)
            p11=Base.Vector(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            #Part.show(c00)
        def socket1(self):#ソケット 異形管75～400---------------------------------------------------------------------------------------
            global c00
            global d2
            global d0
            global d3
            global d4
            global d5
            global P
            global x
            global L0
            global Y

            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
                p1=Base.Vector(0,0,d2)
                p2=Base.Vector(0,0,d5)
                p3=Base.Vector(M,0,d5)
                p4=Base.Vector(M,0,d3)
                p5=Base.Vector(P/2-5,0,d3)
                p6=Base.Vector(P/2,0,d6)
                p7=Base.Vector(P*3/4,0,d6)
                p8=Base.Vector(P*3/4+10,0,d7)
                p9=Base.Vector(P,0,d7)
                p10=Base.Vector(L0,0,d2)
                p11=Base.Vector(L0,0,d0)
                p12=Base.Vector(P,0,d0)
                p13=Base.Vector(P,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p1]
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x
                p1=Base.Vector(0,0,d2)
                p2=Base.Vector(0,0,d5)
                p3=Base.Vector(M,0,d5)
                p4=Base.Vector(M,0,d3)
                p5=Base.Vector(P*3/4-y1,0,d3)
                p6=Base.Vector(P*3/4,0,d6)
                p7=Base.Vector(P,0,d6)
                p8=Base.Vector(L0,0,d2)
                p9=Base.Vector(L0,0,d0)
                p10=Base.Vector(P,0,d0)
                p11=Base.Vector(P,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)

        def socketk(self):#ソケット 両受短管 075～450----------------------------------------------------------------------------------
            global d0
            global d1
            global d2
            global d3
            global d4
            global d5
            global d6
            global d7
            global P
            #global L
            global c00
            global E
            global M
            d0=sa[0]/2
            d2=sa[1]/2
            d5=sa[2]/2
            P=sa[4]
            d4=sa[7]/2
            E=sa[8]/2
            M=sa[9]
            L=sa[11]
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                p1=Base.Vector(0,0,d2)
                p2=Base.Vector(0,0,d5)
                p3=Base.Vector(M,0,d5)
                p4=Base.Vector(M,0,d3)
                p5=Base.Vector(P/2-5,0,d3)
                p6=Base.Vector(P/2,0,d6)
                p7=Base.Vector(P*3/4,0,d6)
                p8=Base.Vector(P*3/4+10,0,d7)
                p9=Base.Vector(P,0,d7)
                p10=Base.Vector(P,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)

            else:
                d3=d4-(E+10)
                d6=(d2+d3)/2
                d7=d6
                y1=d3-d6
                p1=Base.Vector(0,0,d2)
                p2=Base.Vector(0,0,d5)
                p3=Base.Vector(M,0,d5)
                p4=Base.Vector(M,0,d3)
                p5=Base.Vector(P*3/4-y1,0,d3)
                p6=Base.Vector(P*3/4,0,d6)
                p7=Base.Vector(P,0,d6)
                p8=Base.Vector(P,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c00=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)

        if key=='00' or key=='20' :#---------------------------------------------------------------
            if key=='00':
                sa=GX_Data.rcvd[key_1]
                socket(self)
                c1=c00
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                d0=float(sa[0])/2
                d5=float(sa[1])/2
                d2=float(sa[2])/2
                Y=float(sa[3])
                P=sa[4]
                d3=d5*0.95
                d4=d3*0.95
                y=d4-d2
                x=y/math.tan(math.radians(20))
                y1=d5-d3
                y2=d3-d4
                x1=2*y1
                x2=2*y2
                L0=P+x
                
                c2 = Part.makeCylinder(d2,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d0,L-Y-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
                c1=c1.cut(c3)
            elif key=='20':
                sa=GX_Data.rcvd[key_1]
                d0=float(sa[0])/2
                d2=float(sa[2])/2
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                c1 = Part.makeCylinder(d2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
        
        elif key=='01':#二受T字管
            sa1=GX_Data.trcts2[dia]
            H=sa1[0]
            I=sa1[1]
            J=sa1[2]
            LL=sa1[3]
            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x    
            c1=c00
            P0=P
            d02=d2
            d00=d0
            L00=L0
            sa=GX_Data.rcvd1[key_2]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
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
        
        elif key=='02' or key=='03':#片落ち管---------------------------------------------------------------
            sa1=GX_Data.sreduc[dia]
            B=sa1[0]
            C=sa1[1]
            L1=sa1[2]
            L2=sa1[3]
            if key=='02':
                sa=GX_Data.rcvd1[key_1]
                L10=L1
                B10=B
            else:
                sa=GX_Data.rcvd1[key_2]
                L10=L2
                B10=C
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x  
            c1=c00

            d00=d0
            d02=d2
            L00=L0
            P0=P
            x1=L00-P0
            x=50
            if key=='02':
                sa=GX_Data.rcvd1[key_2]
            else:
                sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x  
            p1=(0,0,d00)
            p2=(0,0,d02)
            p3=(x,0,d02)
            p4=(L10-B10-x1,0,d2)
            p5=(L10-x1,0,d2)
            p6=(L10-x1,0,d0)
            p7=(L10-B10-x1,0,d0)
            p8=(x,0,d00)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
            c2.Placement=App.Placement(App.Vector(L00,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
        
        elif key=='04' or key=='05' or key=='06' or key=='07' or key=='08' :#曲管-----------------------------------------
            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x  
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
            if key=='04':#90
                sa1=GX_Data.elbows_90[key_1]
            elif key=='05':#45
                sa1=GX_Data.elbows_45[key_1]
            elif key=='06':#22 1/2
                sa1=GX_Data.elbows_22[key_1]
            elif key=='07':#11 1/4
                sa1=GX_Data.elbows_11[key_1]
            elif key=='08':#5 5/8
                sa1=GX_Data.elbows_5[key_1]
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
        
        elif key=='09' or key=='10':#両受曲管-----------------------------------------
            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x  
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            #Part.show(c1)
            #sa=GX_Data.rcvd1[key_1]
            socket1(self)
            c2=c00
            if key=='09':#45
                s=float(22.5)
                sa1=GX_Data.two_t_45[key_1]
            elif key=='10':
                s=float(11.25)
                sa1=GX_Data.two_t_22[key_1]
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
        
        elif key=='11' :#フランジ付きT字管------------------------------
            sa1=GX_Data.frjts[dia]
            H=sa1[0]
            I=sa1[1]
            J=sa1[2]
            L=sa1[3]

            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x  
            c1=c00
            d00=d0
            d02=d2
            P0=P
            L00=L0
            x=P0+H+J-L00
            c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            sa=GX_Data.flngs[key_2]
            flng(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
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
       
        elif key=='12' :#浅層埋設形フランジ付きT字管------------------------------
            sa1=GX_Data.sfrjts[dia]
            H=sa1[0]
            I=sa1[1]
            J=sa1[2]
            L=sa1[3]
            #b='GX_T-shaped pipe with shallow buried Flange'
            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x    
            c1=c00
            d00=d0
            d02=d2
            P0=P
            L00=L0
            x=P0+H+J-L00
            c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            sa=GX_Data.flngs[key_2]
            flng(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
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
        
        elif key=='13':#うず巻式フランジ付きT字管
            sa1=GX_Data.pfrjts[dia]
            H=sa1[0]
            I=sa1[1]
            J=sa1[2]
            L=sa1[3]
            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x    
            c1=c00
            d00=d0
            d02=d2
            P0=P
            L00=L0
            x=P0+H+J-L00
            c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            sa=GX_Data.flngs[key_2]
            flng(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            k=sa[5]-sa[6]
            m=sa[6]
            c2=c01
            x1=m+k
            c2.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
            c4 = Part.makeCylinder(d2-0.1,I-x1,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
            c2=c2.fuse(c4)
            c5 = Part.makeCylinder(d0,I-d02,Base.Vector(P0+H,d02,0),Base.Vector(0,1,0))
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
            #c1=c1.fuse(c7)
            #Part.show(c1)
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
            c1=c1.fuse(c7)
            c1=c1.fuse(c8)
            c1=c1.cut(c6)
            c1=c1.cut(c5)
        
        elif key=='14':#排水T字管---------------------------------------------------
            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x  
            c1=c00
            P0=P
            d00=d0
            d02=d2
            #sa=GX_Data.rcvd1[key_1]
            socket1(self)
            c2=c00
            sa1=GX_Data.dfrjts[dia]
            H=sa1[0]
            I=sa1[1]
            L=sa1[2]
            x=2*P0+L
            x1=L+2*P0-2*L0
            c2.Placement=App.Placement(App.Vector(x,0,0),App.Rotation(App.Vector(0,0,1),180))
            c3 = Part.makeCylinder(d02,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d00,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            sa=GX_Data.rcvd1[key_2]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
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
        
        elif key=='15':#継輪-----------------------------------------------------
            sa=GX_Data.rcvd1[key_1]
            socketk(self)
            d0=sa[0]/2
            d2=sa[1]/2
            d5=sa[2]/2
            #d6=sa[3]/2
            P=sa[4]
            d4=sa[7]/2
            E=sa[8]/2
            M=sa[9]
            Lx=sa[11]
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                x=50
                y=d6-d3
                x1=M+x+y
                p1=(0,0,d2)
                p2=(0,0,d5)
                p3=(M,0,d5)
                p4=(M,0,d3)
                p5=(M+x,0,d3)
                p6=(M+x+y,0,d6)
                p7=(Lx-x1,0,d6)
                p8=(Lx-x1+y,0,d3)
                p9=(Lx-M,0,d3)
                p10=(Lx-M,0,d5)
                p11=(Lx,0,d5)
                p12=(Lx,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            else:
                d3=d4-(E+5)
                d6=d3-5
                x=50
                y=d3-d6
                x1=M+x+y
                p1=(0,0,d2)
                p2=(0,0,d5)
                p3=(M,0,d5)
                p4=(M,0,d3)
                p5=(M+x,0,d3)
                p6=(x1,0,d6)
                p7=(Lx-x1,0,d6)
                p8=(Lx-x1+y,0,d3)
                p9=(Lx-M,0,d3)
                p10=(Lx-M,0,d5)
                p11=(Lx,0,d5)
                p12=(Lx,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        
        elif key=='16':#両受短管---------------------------------------------------
            sa=GX_Data.rcvd1[key_1]
            socketk(self)
            d0=sa[0]/2
            d2=sa[1]/2
            d5=sa[2]/2
            #d6=sa[3]/2
            P=sa[4]
            d4=sa[7]/2
            E=sa[8]/2
            M=sa[9]
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
            else:
                d3=d4-(E+10)
                d6=(d2+d3)/2
                d7=d6
                y1=d3-d6    
            c1=c00
            socketk(self)
            c2=c00
            Lx=20
            c2.Placement=App.Placement(Base.Vector(2*P+Lx,0.0,0.0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            c3 = Part.makeCylinder(d7,Lx,Base.Vector(P,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d0,Lx,Base.Vector(P,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.fuse(c3)
        
        elif key=='17':#乙字管---------------------------------------------------
            sa1=GX_Data.zshps[dia]
            R=float(sa1[0])
            Lx=float(sa1[1])
            L1=float(sa1[2])
            L3=float(sa1[3])
            H=float(sa1[4])
            sa=GX_Data.rcvd1[key_1]
            #print(key_1)
            #d0=sa[0]
            #d2=sa[1]
            socket1(self)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d5=float(sa[2])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=float(sa[9])
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d3=d4-(E+10)
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x    
            c1=c00
            x=L0-P
            L2=Lx-(L1+L3)

            s=math.atan(L2/H)
            s1=(math.radians(90)-s)/2
            y=R*math.sin(s)
            x2=R*math.tan(s1)
            x1=L1-x-x2
            x3=L1+L2-x+x2
            y4=x2*math.cos(s)
            x5=y4*math.tan(s)
            x6=R*math.cos(s)
            y1=R-y
            x7=y1*math.tan(s)
            y3=H-(y4+y1)
            x4=y3*math.tan(s)
            edge6 = Part.makeCircle(d2, Base.Vector(0,0,0), Base.Vector(1,0,0))
            edge7 = Part.makeCircle(d0, Base.Vector(0,0,0), Base.Vector(1,0,0))
            p1=(0,0,0)
            p2=(x1,0,0)
            p3=(x1,-R,0)
            p4=(x1+x6,-y4,0)
            p5=(x1+x2+x5+x4,-(y3+y4),0)
            p6=(x3,-(H-R),0)
            p7=(x3,-H,0)
            p8=(Lx-x,-H,0)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(R, Base.Vector(x1,-R,0), Base.Vector(0,0,1), math.degrees(s), 90)
            edge3=Part.makeLine(p4,p5)
            edge4 = Part.makeCircle(R, Base.Vector(x3,-(H-R),0), Base.Vector(0,0,1), 180+math.degrees(s), 270)
            edge5=Part.makeLine(p7,p8)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5])
            profile2=Part.Wire([edge6])
            profile3=Part.Wire([edge7])
            makeSolid=True
            isFrenet=True
            c2 = Part.Wire(aWire).makePipeShell([profile2],makeSolid,isFrenet)
            c3 = Part.Wire(aWire).makePipeShell([profile3],makeSolid,isFrenet)
            c2=c2.cut(c3)
            c2.Placement=App.Placement(App.Vector(L0,0,0),App.Rotation(App.Vector(0,0,1),0))
            c1=c1.fuse(c2)
        
        elif key=='18':#帽---------------------------------------------------
            global T1
            sa=GX_Data.rcvd1[key_1]
            socketk(self)
            d0=sa[0]/2
            d2=sa[1]/2
            d5=sa[2]/2
            P=sa[4]
            d4=sa[7]/2
            E=sa[8]/2
            M=sa[9]
            L=sa[11]
            if float(key_1)<=250.0:
                d3=d4-(E+10)
                d6=d3+5
                d7=d6-10
            else:
                d3=d4-(E+10)
                d6=(d2+d3)/2
                d7=d6    
            T1=sa[10]
            c1=c00
            c2 = Part.makeCylinder(d7,T1,Base.Vector(P,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
        
        elif key=='19':#押輪---------------------------------------------------
            #global y
            sa=GX_Data.rcvd1[key_1]
            d5=float(sa[2])/2
            d2=float(sa[1])/2
            d4=float(sa[7])/2
            E=float(sa[8])/2
            M=sa[9]
            d3=d4-(E+5)
            y=5
            p1=(0,0,d2)
            p2=(0,0,d5)
            p3=(M,0,d5)
            p4=(M,0,d3+y)
            p5=(M-y,0,d3)
            p6=(M-y,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),360)
        
        elif key=='21':#P-Link---------------------------------------------------
            sa1=GX_Data.plnks[key_1]
            d0=float(sa1[0])/2
            d2=float(sa1[2])/2
            P=sa1[3]
            d8=float(sa1[4])/2
            Lx=sa1[6]
            d3=d2+30
            x=30
            y=P-(41+0.5*P)
            d4=d3-10
            d5=d4-10
            L0=P+Lx
            p1=(0,0,d2)
            p2=(0,0,d2+10)
            p3=(5,0,d2+10)
            p4=(5,0,d8-10)
            p5=(5+0.3*P,0,d8)
            p6=(5+0.3*P+y,0,d3)
            p7=(5+0.5*P+y,0,d3)
            p8=(15+0.5*P+y,0,d4)
            p9=(35+0.5*P+y,0,d4)
            p10=(45+0.5*P+y,0,d5)
            p11=(P+15,0,d5)
            p12=(P+15,0,d2)
            p13=(L0,0,d2)
            p14=(L0,0,d0)
            p15=(P,0,d0)
            p16=(P,0,d2)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        
        elif key=='22':#G-Link---------------------------------------------------
            sa1=GX_Data.glinks[key_1]
            d0=float(sa1[0])/2
            d4=float(sa1[1])/2
            d5=float(sa1[2])/2
            d8=float(sa1[3])/2
            B=sa1[4]
            E=sa1[5]/2
            M=sa1[6]
            d2=float(sa1[7])/2
            d3=d4-(E+5)
            x=(B-M)/2
            if key_1=='300':
                p1=(0,0,d2)
                p2=(0,0,d3)
                p3=(2*x,0,d3)
                p4=(2*x,0,d5)
                p5=(B,0,d5)
                p6=(B,0,d3)
                p7=(B-5,0,d3-5)
                p8=(B-5,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            else:
                p1=(0,0,d2)
                p2=(0,0,d2+5)
                p3=(x,0,d2+5)
                p4=(x,0,d3)
                p5=(2*x,0,d3)
                p6=(2*x,0,d5)
                p7=(B,0,d5)
                p8=(B,0,d3)
                p9=(B-5,0,d3-5)
                p10=(B-5,0,d2)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        
        elif key=='23':
            sa=GX_Data.rcvd[key_1]
            d0=sa[0]
            d2=sa[2]
            Lx=sa[6]
            c1 = Part.makeCylinder(d2,Lx,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c2 = Part.makeCylinder(d0,Lx,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)
        
        elif key=='24' or key=='25':#gate valve(Internal)---------------------------------------------------
            sa1=GX_Data.sfgs[key_1]
            L1=sa1[0]
            Lx=sa1[1]
            H=sa1[2]
            sa=GX_Data.rcvd1[key_1]
            socket1(self)
            c1=c00
            socket1(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            P=sa[4]
            d4=float(sa[7])/2
            E=float(sa[8])/2
            d3=d4-(E+10)
            M=float(sa[9])
            if float(key_1)<=250.0:
                d6=d3+5
                d7=d6-10
                y=d7-d2
                x=y
                L0=P+x
            else:
                d6=(d3+d2)/2
                y1=d3-d6
                y2=d6-d2
                x=y2
                L0=P+x

            c2 = Part.makeCylinder(d2,L1-2*L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            x2=0.3
            if float(key_1)<=150.0:
                x3=0.4
            elif float(key_1)<=300.0:
                x3=0.45
            else:
                x3=0.5
            w0=x2*Lx
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
            L0x=h0
            if float(key_1)<=200.0:
                L0x=0.9*L0x
                z1=x3*H+2*0.7*M+3+L0x/2+10
            elif float(key_1)<=250.0:
                L0x=0.8*L0x
                z1=x3*H+2*0.7*M+3+L0x/2+20
            elif float(key_1)<=300.0:
                L0x=0.7*L0x
                z1=x3*H+2*0.7*M+3+L0x/2+50
            elif float(key_1)<=400.0:
                L0x=0.6*L0x
                z1=x3*H+2*0.7*M+3+L0x/2+50
            else:
                L0x=0.5*L0x
                z1=x3*H+2*0.7*M+3+L0x/2+60
            w0=w0-0.1
            w1=w0-20
            h1=L0x-20
            p1=(0,h1/2,0)
            p2=(10,L0x/2,0)
            p3=(w0-10,L0x/2,0)
            p4=(w0,h1/2,0)
            p5=(w0,-h1/2,0)
            p6=(w0-10,-L0x/2,0)
            p7=(10,-L0x/2,0)
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
            if key=='24':
                if float(key_1)<=100.0:
                    Lb=20
                    B=20
                    C=25
                elif float(key_1)<=150.0:
                    Lb=35
                    B=20
                    C=25
                elif float(key_1)<=200.0:
                    Lb=40
                    B=25
                    C=30
                elif float(key_1)<=250.0:
                    Lb=45
                    B=35
                    C=40
                elif float(key_1)<=300.0:
                    Lb=45
                    B=35
                    C=45
                elif float(key_1)<=400.0:
                    Lb=70
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

            elif key=='25':
                H=sa1[3]
                w=sa1[4]
                if float(key_1)<=150.0:
                    Lb1=40
                    Lb2=50
                    B1=20
                    C=10
                elif float(key_1)<=200.0:
                    Lb1=40
                    Lb2=50
                    B1=30
                    C=15
                elif float(key_1)<=250.0:
                    Lb1=40
                    Lb2=50
                    B1=40
                    C=15
                elif float(key_1)<=300.0:
                    Lb1=50
                    Lb2=60
                    B1=40
                    C=15
                elif float(key_1)<=400.0:
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
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        label='mass[kg]'
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
            obj.ViewObject.Proxy=0
        except:
            obj.mass=g
            obj.ViewObject.Proxy=0
            pass   
        obj.Shape=c1



