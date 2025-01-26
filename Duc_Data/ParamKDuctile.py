from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import K_Data

class k_ductile:
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
            #sa=K_Data.flngs[key_1]
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
            #L=float(sa[9])
            h=float(sa[9])
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

        def socket0(self):#ソケット-----------------------------------------------------------------------------------------------
            global c00
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
        
        if key=='00' or key=='20':
            if key=='00':
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                sa=K_Data.rcvd[key_1]
                d2 = float(sa[2]/2)
                d0 = float(sa[0]/2)
                d4=float(sa[3])/2
                k=float(sa[4])
                E0=float(sa[5]/2)
                d3=d4-(E0+5)
                P=sa[6]
                gu=sa[9]
                g0=sa[10]
                g=gu+g0*L/1000
                x1=P-k
                s=3.0
                d6=d3-x1*math.tan(math.radians(s))
                x=(d6-d2)*math.sqrt(3)
                L0=P+x
                socket0(self)
                c1=c00
                c2 = Part.makeCylinder(d2,L-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(d0,L-(L0-P),Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c2=c2.cut(c3)
                c1=c1.fuse(c2)
            elif key=='20':
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                sa=K_Data.rcvd[key_1]
                g0=sa[10]
                g=g0*L/1000
                #socket0(self)
                d0=float(sa[0])/2
                d2=float(sa[2])/2
                c1 = Part.makeCylinder(d2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
        elif key=='01' or key=='02':
            if key=='01':
                sa=K_Data.trcts[dia]
            elif key=='02':
                sa=K_Data.trcts2[dia]
            H=sa[0]
            I=sa[1]
            J=sa[2]
            LL=sa[3]
            g=sa[4]
            sa=K_Data.rcvd[key_1]
            socket0(self)
            c1=c00
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
            P0=P
            d02=d2
            d00=d0
            sa=K_Data.rcvd[key_2]
            socket0(self)
            c2=c00
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
            c2.Placement=App.Placement(App.Vector(P0+H,P+I,0),App.Rotation(App.Vector(0,0,1),-90))

            c11 = Part.makeCylinder(d02+0.1,P0+LL-L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c12 = Part.makeCylinder(d00-0.1,P0+LL-L0,Base.Vector(L0,0,0),Base.Vector(1,0,0))
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
            if key=='03':
                sa=K_Data.rcvd[key_1]
            elif key=='04':
                sa=K_Data.rcvd[key_2]    
            socket0(self)
            c1=c00
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
            d00=d0
            d02=d2
            L00=L0
            P0=P
            if key=='03':
                sa=K_Data.rcvd[key_2]
            elif key=='04':
                sa=K_Data.rcvd[key_1]        
            socket0(self)
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
            sa1=K_Data.trcts3[dia]
            A0=sa1[0]
            B=sa1[1]
            C=sa1[2]
            E=sa1[3]
            L1=sa1[4]
            L2=sa1[5]

            if key=='03':

                sa1=K_Data.trcts3[dia]
                g=sa1[6]
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
                sa1=K_Data.trcts3[dia]
                g=sa1[7]
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

        elif key=='05' or key=='06' or key=='07' or key=='08' or key=='09':#曲管-----------------------------------------
            sa=K_Data.rcvd[key_1]
            socket0(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))      
            d0=float(sa[0])/2
            #print(d0)
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
            
            if key=='05':#90
                sa1=K_Data.elbows_90[key_1]
            elif key=='06':#45
                sa1=K_Data.elbows_45[key_1]
            elif key=='07':#22 1/2
                sa1=K_Data.elbows_22[key_1]
            elif key=='08':#11 1/4
                sa1=K_Data.elbows_11[key_1]
            elif key=='09':#5 5/8
                sa1=K_Data.elbows_5[key_1]
                
            R=sa1[0]
            L1=sa1[1]
            L2=sa1[2]
            g=sa1[4]
            #print(g)
            s=float(sa1[3])/2
            a0=L0-P-10
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
            #print(d0)
            if d0==750.0:
                c2=c2.cut(c3)
                cs=[c1,c2]
                c1 = Part.makeCompound(cs)
            else:
                c1=c1.fuse(c2)
                c1=c1.cut(c3)

        elif key=='10' or key=='11' :
            if key=='10':
                sa=K_Data.rcvd[key_1]
                socket0(self)
                c1=c00
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
                d00=d0
                d02=d2
                P0=P
                sa=K_Data.flngs[key_1]
                flng0(self)
                c2=c01
                #Part.show(c2)
                sa=K_Data.flngs[key_2]
                flng0(self)
                c3=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k0=m+k
                sa1=K_Data.gvsps[dia]
                B=sa1[0]
                H=sa1[1]
                I=sa1[2]
                J=sa1[3]
                L1=sa1[4]
                L2=sa1[5]
                g=sa1[6]
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
                sa=K_Data.flngs[key_1]
                flng0(self)
                c1=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                k0=m+k
                d00=d0
                d02=d2
                x01=m+k
                sa=K_Data.flngs[key_2]
                flng0(self)
                c2=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m1 = sa[6]
                k = sa[5]
                k0=m1+k
                sa1=K_Data.gvsps[dia]
                B=sa1[0]
                H=sa1[1]
                I=sa1[2]
                J=sa1[3]
                L1=sa1[4]
                L2=sa1[5]
                g=sa1[7]
                x1=m1+k
                x=B+J-(m1+k)
                c2.Placement=App.Placement(App.Vector(B,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c1=c1.fuse(c2)
                c3 = Part.makeCylinder(d02,L2-x01+m,Base.Vector(x01-m,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c3)
                c4 = Part.makeCylinder(d2,(I-x1)+m1,Base.Vector(B,0,0),Base.Vector(0,1,0))
                c1=c1.fuse(c4)
                c5 = Part.makeCylinder(d00,L2-x01+m,Base.Vector(x01-m,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c5)
                c6 = Part.makeCylinder(d0,I-x1+m1,Base.Vector(B,0,0),Base.Vector(0,1,0))
                c1=c1.cut(c6)
        elif key=='12' or key=='13':
            if key=='12':
                sa=K_Data.rcvd[key_1]
                socket0(self)
                c1=c00
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
                d00=d0
                d02=d2
                P0=P
                L00=L0

                sa1=K_Data.ttfs[dia]
                H=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L=sa1[3]
                g=sa1[4]
                x=P0+H+J-L00

                c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                sa=K_Data.flngs[key_2]
                flng0(self)
                c2=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                x1=m+k

                c2.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c4 = Part.makeCylinder(d2-0.1,I-x1+m,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.fuse(c4)
                c5 = Part.makeCylinder(d0,I-x1+m,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)
                c1=c1.cut(c6)
                c1=c1.cut(c5)
            elif key=='13':
                sa1=K_Data.ttfs[dia]
                H=sa1[0]
                I=sa1[1]
                J=sa1[2]
                L=sa1[3]
                g=sa1[5]

                sa=K_Data.rcvd[key_1]
                socket0(self)
                c1=c00
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
                d00=d0
                d02=d2
                P0=P
                L00=L0
                d00=d0
                d02=d2
                P0=P
                L00=L0
                x=P0+H+J-L00
                c3 = Part.makeCylinder(d02,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                c6 = Part.makeCylinder(d00,x,Base.Vector(L0,0,0),Base.Vector(1,0,0))
                sa=K_Data.flngs[key_2]
                flng0(self)
                c2=c01
                d2 = sa[1]/2
                d0 = sa[0]/2
                m = sa[6]
                k = sa[5]
                x1=m+k
                c2.Placement=App.Placement(App.Vector(P0+H,I,0),App.Rotation(App.Vector(0,0,1),-90))
                c4 = Part.makeCylinder(d2-0.1,I-x1+m,Base.Vector(P0+H,0,0),Base.Vector(0,1,0))
                c2=c2.fuse(c4)
                c5 = Part.makeCylinder(d0,I-d02+m,Base.Vector(P0+H,d02,0),Base.Vector(0,1,0))

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
                c1=c1.cut(c5)
        elif key=='14':
            sa=K_Data.rcvd[key_1]
            socket0(self)
            c1=c00
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
            P0=P
            d00=d0
            d02=d2
            socket0(self)
            c2=c00

            sa1=K_Data.dtps[dia]
            H=sa1[0]
            I=sa1[1]
            L=sa1[2]
            g=sa1[3]
            x=2*P0+L
            x1=L+2*P0-2*L0
            c2.Placement=App.Placement(App.Vector(x,0,0),App.Rotation(App.Vector(0,0,1),180))
            c3 = Part.makeCylinder(d02,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d00,x1,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            sa=K_Data.rcvd[key_2]
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
            socket0(self)
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
        elif key=='15':    
            sa=K_Data.rcvd[key_1]
            d0=sa[0]/2
            d5=sa[1]/2
            d2=sa[2]/2
            d4=sa[3]/2
            k=sa[4]
            E0=sa[5]/2
            L=sa[8]
            g=sa[11]

            d3=d4-(E0+5)
            d6=(L/2-k)*math.tan(math.radians(3))+d3
            #socketk(self)
            p1=Base.Vector(0,0,d2)
            p2=Base.Vector(0,0,d5)
            p3=Base.Vector(k,0,d5)
            p4=Base.Vector(k,0,d3)
            p5=Base.Vector(L/2,0,d6)
            p6=Base.Vector(L-k,0,d3)
            p7=Base.Vector(L-k,0,d5)
            p8=Base.Vector(L,0,d5)
            p9=Base.Vector(L,0,d2)
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d5), None, QtGui.QApplication.UnicodeUTF8))
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p1]
            w10=Part.makePolygon(plst)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        elif key=='16':#短管１号
            sa=K_Data.rcvd[key_1]
            socket0(self)
            c1=c00
            d2 = float(sa[2]/2)
            d0 = float(sa[0]/2)
            d4=float(sa[3])/2
            k=float(sa[4])
            E0=float(sa[5]/2)
            d3=d4-(E0+5)
            P=sa[6]
            g=sa[12]
            x1=P-k
            s=3.0
            d6=d3-x1*math.tan(math.radians(s))
            x=(d6-d2)*math.sqrt(3)
            L0=P+x
            sa=K_Data.flngs[key_1]
            flng0(self)
            c2=c01
            m = sa[6]
            k = sa[5]
            x1=m+k
            sa1=K_Data.tnkns[dia]
            L1=sa1[0]
            c2.Placement=App.Placement(App.Vector(P+L1,0,0),App.Rotation(App.Vector(0,0,1),180))
            c1=c1.fuse(c2)
            x=P+L1-x1-L0
            c3 = Part.makeCylinder(d2,x+m,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(d0,x+m,Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.fuse(c3)
        elif key=='17':#短管2号
            sa=K_Data.flngs[key_1]
            flng0(self)
            c1=c01
            d2 = sa[1]/2
            d0 = sa[0]/2
            m = sa[6]
            k = sa[5]
            g=sa[10]
            x1=m+k
            sa1=K_Data.tnkns[dia]
            L2=sa1[1]
            x=L2-x1
            c2 = Part.makeCylinder(d2,x+m,Base.Vector(x1-m,0,0),Base.Vector(1,0,0))
            c3 = Part.makeCylinder(d0,x+m,Base.Vector(x1-m,0,0),Base.Vector(1,0,0))
            c2=c2.cut(c3)
            c1=c1.fuse(c2)  
        elif key=='18':#プラグ---------------------------------------------------
            sa=K_Data.rcvd[key_1]
            socket0(self)
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
            d00=d0
            d02=d2
            P0=P
            L00=L0
            sa1=K_Data.tnkns[dia]
            M=sa1[2]
            M0=sa1[3]
            LL=sa1[4]

            g=sa1[7]
            d3=d2+M0
            p1=(0,0,0)
            p2=(0,0,d5)
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(k), None, QtGui.QApplication.UnicodeUTF8))
            p3=(k,0,d5)
            p4=(k,0,d3)
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(d3), None, QtGui.QApplication.UnicodeUTF8))
            p5=(LL-M,0,d3)
            p6=(LL-M,0,d2)
            p7=(LL,0,d2)
            p8=(LL,0,d0)
            p9=(k,0,d0)
            p10=(k,0,0)
            #self.label_3.setText(QtGui.QApplication.translate("Dialog", str(a), None, QtGui.QApplication.UnicodeUTF8))
            plst=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]
            w10=Part.makePolygon(plst)
            wface = Part.Face(w10)
            #Part.show(wface)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
            doc=App.ActiveDocument 
        elif key=='19':#押輪
            sa=K_Data.rtngs[dia]
            d3=float(sa[0])/2
            d4=float(sa[1])/2
            d5=float(sa[2])/2
            E=sa[3]
            M=sa[4]
            g=sa[6]
            if int(dia)<=600:
                M0=17
            else:
                M0=21
            p1=(0,0,d3)
            p2=(0,0,d5)
            p3=(M,0,d5)
            p4=(M,0,d3+M0)
            p5=(M+19,0,d3+M0)
            p6=(M+19,0,d3)
            plst=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plst)
            wface = Part.Face(w10)
            c1=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1.0,0.0,0.0),360)
        elif key=='21' :#仕切弁
            sa=K_Data.rcvd[dia]
            socket0(self)
            c1=c00
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
            sa1=K_Data.gates[dia]
            L=sa1[0]
            H=sa1[1]
            L1=sa1[2]
            L2=sa1[3]
            M=sa1[4]
            g=sa1[5]
            c2 = Part.makeCylinder(d2,(L1-L0),Base.Vector(L0,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)
            if key_1<='150':
                x3=0.4
            elif key_1<='300':
                x3=0.425
            else:
                x3=0.5
            x2=0.5
            w0=x2*L2
            h0=2*d2+20
            LL=P+L2-w0/2
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
            wface5.Placement=App.Placement(App.Vector((P+L2-w0/2),0,0),App.Rotation(App.Vector(0,0,1),0))
            c7=wface5.extrude(Base.Vector(0,0,z1))#z1角柱
            c1=c1.fuse(c7)
            wface6 = Part.Face(aWire5)
            wface6.Placement=App.Placement(App.Vector((P+L2-w0/2),0,z1+1),App.Rotation(App.Vector(0,0,1),0))
            c8=wface6.extrude(Base.Vector(0,0,0.7*M))
            c1=c1.fuse(c8)
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
            c9=Part.makeBox(32,32,50,Base.Vector((P+L2-32/2),-16,H-50),Base.Vector(0,0,1))
            c1=c1.fuse(c9)
            c10= Part.makeCylinder(C,3,Base.Vector((P+L2),0,H-50-3),Base.Vector(0,0,1))
            c1=c1.fuse(c10)
            c11= Part.makeCylinder(B,Lb-3,Base.Vector((P+L2),0,H-50-Lb),Base.Vector(0,0,1))
            c1=c1.fuse(c11)
            c12= Part.makeCylinder(B,Lb,Base.Vector((P+L2),0,z1+10),Base.Vector(0,0,1))
            c1=c1.fuse(c12)
            c13= Part.makeCylinder(15,(H-(z1+50+Lb)),Base.Vector((P+L2),0,z1+Lb-3),Base.Vector(0,0,1))
            c1=c1.fuse(c13)
            c14= Part.makeCylinder(d0,L1,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c14)

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