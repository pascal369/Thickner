from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import F_Data
from . import K_Data
from . import NS_Data
from . import GX_Data
from . import NSE_Data
from . import S_Data
from . import T_Data
from . import U_Data
from . import UF_Data
from . import US_Data

class f_ductile:
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

        def flng0(self):#フランジ---------------------------------------------------------------------------------------------
            global c01
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d3=float(sa[2])/2
            d4=float(sa[3])/2
            d5=float(sa[4])/2
            m=float(sa[6])
            k=float(sa[5])-m
            k0=m+k
            n=int(sa[7])
            LL2=float(sa[8])
            L=float(sa[9])
            h=float(sa[14])
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

        if key=='00' or key=='01' :
            global g
            sa=F_Data.flngs[key_1]
            flng0(self)
            c1=c01
            d2 = sa[1]/2
            d0 = sa[0]/2
            m = sa[6]
            k = sa[5]
            gf=sa[17]
            g0=sa[18]
            k0=m+k
            
            if key=='00' :
                #L0 = sa[9]
                L0=App.ActiveDocument.getObject(label).L0
                L0 = float(L0)
                c3 = Part.makeCylinder(d2,L0-2*k0+2*m,Base.Vector(k0-m,0,0),Base.Vector(1,0,0))
                c4 = Part.makeCylinder(d0,L0-2*k0+2*m,Base.Vector(k0-m,0,0),Base.Vector(1,0,0))
                flng0(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(L0,0,0),App.Rotation(App.Vector(0,0,1),180))
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)
                c1=c1.cut(c4)
                g=2*gf+g0*L0/1000
            elif key=='01':#片フランジ長管
                L0=App.ActiveDocument.getObject(label).L0
                L0 = float(L0)
                c2 = Part.makeCylinder(d2,L0-k0+m,Base.Vector(k0-m,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d0,L0-k0+m,Base.Vector(k0-m,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
                c1=c1.cut(c3)
                g=gf+g0*L0/1000
        elif key=='02' :#3フランジT字管
            b='F3T_shaped tube'
            label=b

            sa=F_Data.flngs[key_1]
            d02 = sa[1]/2
            d00 = sa[0]/2
            m = sa[6]
            k = sa[5]
            k00=m+k

            sa1=F_Data.trcts[dia]
            B=sa1[0]
            I=sa1[1]
            L0=sa1[2]
            g=sa1[3]
            flng0(self)
            c1=c01
            flng0(self)
            c2=c01
            c2.Placement=App.Placement(App.Vector(L0,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            
            sa=F_Data.flngs[key_2]
            flng0(self)
            d2 = sa[1]/2
            d0 = sa[0]/2
            m = sa[6]
            k = sa[5]
            k0=m+k

            c3=c01
            c3.Placement=App.Placement(App.Vector(B,I,0),App.Rotation(App.Vector(0,0,1),-90))
            c1=c1.fuse(c3)
            c4 = Part.makeCylinder(d02,L0-2*k00+2*m,Base.Vector(k00-m,0,0),Base.Vector(1,0,0))
            c5 = Part.makeCylinder(d00,L0-2*k00+2*m,Base.Vector(k00-m,0,0),Base.Vector(1,0,0))
            c6 = Part.makeCylinder(d2,I-k0+m,Base.Vector(B,0,0),Base.Vector(0,1,0))
            c7 = Part.makeCylinder(d0,I-k0+m,Base.Vector(B,0,0),Base.Vector(0,1,0))
            c1=c1.fuse(c4)
            c1=c1.fuse(c6)
            c1=c1.cut(c7)
            c1=c1.cut(c5)
            
        elif key=='03' :#2フランジT字管
                b='F2T_shaped tube'
                label=b
                sa1=F_Data.trcts2[dia]
                B=sa1[0]
                I=sa1[1]
                L0=sa1[3]
                g=sa1[4]
                sa=F_Data.flngs[key_1]
                flng0(self)
                c1=c01
                d02 = sa[1]/2
                d00 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k00=m+k

                sa=F_Data.flngs[key_2]
                flng0(self)
                c3=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k0=m+k

                c3.Placement=App.Placement(App.Vector(B,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c1=c1.fuse(c3)
                c4 = Part.makeCylinder(d02,L0-k00+m,Base.Vector(k00-m,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c4)
                c5 = Part.makeCylinder(d00,L0-k00+m,Base.Vector(k00-m,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d2,I-k0+m,Base.Vector(B,0,0),Base.Vector(0,1,0))
                c7 = Part.makeCylinder(d0,I-k0+m,Base.Vector(B,0,0),Base.Vector(0,1,0))

                c1=c1.fuse(c6)
                c1=c1.cut(c7)
                c1=c1.cut(c5)
        
        elif key=='04' :#フランジ片落管---------------------------------------------------------------
                b='Flange Reducer'
                label=b
                sa1=F_Data.trcts3[dia]
                A00=sa1[0]
                E=sa1[1]
                Lf=sa1[2]
                g=sa1[3]
                sa=F_Data.flngs[key_1]
                flng0(self)
                c1=c01
                #Part.show(c1)
                d02 = sa[1]/2
                d00 = sa[0]/2
                m1 = sa[6]
                k = sa[5]
                k00=m1+k
                sa=F_Data.flngs[key_2]
                flng0(self)
                c2=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m2 = sa[6]
                k = sa[5]
                k0=m2+k
                c2.Placement=App.Placement(App.Vector(Lf,0,0),App.Rotation(App.Vector(0,0,1),180))

                L0=Lf-(k00+k0)
                A0=A00-k0
                E0=E-k0

                p1=(-m1,0,d00)
                p2=(-m1,0,d02)
                p3=(A0,0,d02)
                p4=(L0-E0,0,d2)
                p5=(m2+L0,0,d2)
                p6=(m2+L0,0,d0)
                p7=(L0-E0,0,d0)
                p8=(A0,0,d00)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                w10=Part.makePolygon(plist)
                wface = Part.Face(w10)
                c3=wface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                c3.Placement=App.Placement(App.Vector(k00,0,0),App.Rotation(App.Vector(0,0,1),0))
                #Part.show(c3)
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)
        
        elif key=='05' or key=='06' :#曲管-----------------------------------------
                if key=='05':#90
                    sa1=F_Data.elbows_90[key_1]
                    label='F90Elbow_'
                elif key=='06':#45
                    sa1=F_Data.elbows_45[key_1]
                    label='F45Elbow_'

                R=sa1[0]
                L1=sa1[1]
                deg=sa1[2]
                g=sa1[3]
                s=float(deg)/2
                sa=F_Data.flngs[key_1]

                flng0(self)
                c1=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k0=m+k

                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))
                c1.Placement=App.Placement(App.Vector(0,-L1,0),App.Rotation(App.Vector(0,0,1),90))
                flng0(self)
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
                p1=(0,-(L1-a0+m),0)
                p2=(0,-R*math.tan(math.radians(s)),0)
                p3=(x,-y3,0)
                p4=(x1,y2,0)
                p5=((L1-a0+m)*math.cos(math.radians(90-2*s)),(L1-a0+m)*math.sin(math.radians(90-2*s)),0)
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
        
        elif     key=='07' :#-----------------------------------------------------------------------------------
                sa1=F_Data.gvsps[dia]
                R=sa1[0]
                L1=sa1[1]
                L2=sa1[2]
                g=sa1[3]

                label='F_Gate Valve Secondary PipeB1_'
                sa=F_Data.flngs[key_2]
                flng0(self)
                c1=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k0=m+k
                c1.Placement=App.Placement(App.Vector(0,-L1,0),App.Rotation(App.Vector(0,0,1),90))
                sa=F_Data.flngs[key_2]
                flng0(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(L2,0,0),App.Rotation(App.Vector(0,0,1),180))
                c1=c1.fuse(c2)

                L0=L1-(R+k0)
                L01=L2-(R+k0)

                p1=(0,-(R+L0+m),0)
                p2=(0,-R,0)
                p3=(R,0,0)
                p4=(R+L01+m,0,0)
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
        
        elif     key=='08':#-----------------------------------------------------------------------------------
                sa1=F_Data.flgts[dia]
                L0=sa1[0]
                g=sa1[2]
                label='Flange Short Tube'
                sa=F_Data.flngs[key_1]
                flng0(self)
                c1=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k0=m+k
                x=L0-2*k0+2*m
                c2 = Part.makeCylinder(d2,x,Base.Vector(k0-m,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d0,x,Base.Vector(k0-m,0,0),Base.Vector(1,0,0))
                c2=c2.cut(c3)
                sa=F_Data.flngs[key_1]
                flng0(self)
                c4=c01
                c4.Placement=App.Placement(App.Vector(L0,0,0),App.Rotation(App.Vector(0,0,1),180))
                c1=c1.fuse(c2)
                c1=c1.fuse(c4)
        
        elif key=='09':#フランジ蓋-----------------------------------------------------
                sa=F_Data.flngs[dia]
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
                sa1=F_Data.tnkns[dia]
                R1=sa1[0]
                R2=sa1[1]
                T=sa1[2]
                g=sa1[5]
                k0=k+m
                R=R1+T
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))

                if float(dia)>=150.0:
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
        
        elif     key=='10':#人孔蓋---------------------------------------------------
                sa=F_Data.flngs[key_1]
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
                sa1=F_Data.mhlcs[dia]
                H=sa1[0]
                L0=sa1[1]
                g=sa1[2]
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

                sa=F_Data.flngs[key_2]
                flng0(self)
                c4=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k1=m+k
                x=L0-k1
                c4.Placement=App.Placement(App.Vector(0,L0,0),App.Rotation(App.Vector(0,0,1),-90))
                c5 = Part.makeCylinder(d2,x,Base.Vector(0,0,0),Base.Vector(0,1,0))
                c6 = Part.makeCylinder(d0,x,Base.Vector(0,0,0),Base.Vector(0,1,0))
                c4=c4.fuse(c5)
                c1=c1.fuse(c4)
                c1=c1.cut(c22)
                c1=c1.cut(c6)
        
        elif     key=='11':#らっぱ口----------------------------------------------------------------
                sa=F_Data.flngs[key_1]
                flng0(self)
                c1=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k0=m+k
                T=sa[10]
                T1=sa[11]
                D1=sa[12]
                L0=sa[13]
                g=sa[19]
                R2=float(D1)/2
                r1=float(T1)/2
                R=R2-d0
                y2=L0-R

                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))

                p1=(d0,k0-m,0)
                p2=(d0,y2,0)
                p3=(R2,L0,0)
                p4=(R2,L0-T,0)
                p5=(d0+T,y2,0)
                p6=(d0+T,k0-m,0)
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
        
        elif     key=='12' or key=='13':#gate valve(Internal)---------------------------------------------------
                global M
                sa=F_Data.flngs[key_1]
                M=sa[5]
                flng0(self)
                c1=c01
                sa=F_Data.flngs[key_1]
                flng0(self)
                c2=c01

                sa1=F_Data.gates[key_1]
                L1=sa1[0]
                L=sa1[0]
                H=sa1[1]
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                L0=m+k
                c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,0,1),180))
                c1=c1.fuse(c2)

                #c3 = Part.makeCylinder(d2,L1-2*L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d2,L1,Base.Vector(0,0,0),Base.Vector(1,0,0))
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
                #Part.show(c2)
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
                #Part.show(c3)
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
                    g=sa1[4] 
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
                    #Part.show(c1)
                    #Part.show(c14)

                elif key=='13':
                    H=sa1[2]
                    w=sa1[3]
                    g=sa1[5]
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

