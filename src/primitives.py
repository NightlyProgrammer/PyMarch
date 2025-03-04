#objects and their sdf
from math import sqrt
from vector import Vector3,apply_rotation

class Primitive:
    def __init__(self,position:Vector3,material):
        self.pos = position
        self.rotation = Vector3(0,0,0)#in radians
        self.material = material
    
    def get_color_at(self,point:Vector3):
        return self.material.get_at(point)
    
    def get_normal(self,point:Vector3):
        epsilon = 0.001#very small number
        vec1 = Vector3(
            self.sdf(point+Vector3(epsilon,0,0)),
            self.sdf(point+Vector3(0,epsilon,0)),
            self.sdf(point+Vector3(0,0,epsilon))
        )
        vec2 = Vector3(
            self.sdf(point-Vector3(epsilon,0,0)),
            self.sdf(point-Vector3(0,epsilon,0)),
            self.sdf(point-Vector3(0,0,epsilon))
        )
        return (vec1-vec2).normalize()
    
    def __neg__(self):#for operators,called when there is a minus sign
        return self,-1

class Sphere(Primitive):
    def __init__(self,position:Vector3,radius:float,material):
        super().__init__(position,material)
        self.r = radius
    
    def sdf(self,point:Vector3):#return distance between object and point
        #point = apply_rotation(point-self.pos,self.rotation*-1)+self.pos
        return (self.pos-point).length()-self.r

#got this from https://iquilezles.org/articles/distfunctions/
class Cuboid(Primitive):#Box
    def __init__(self,position,width,height,length,material):
        super().__init__(position,material)
        self.dimensions = Vector3(width/2,height/2,length/2)#size of box/cuboid
    
    def sdf(self,point):# see https://www.youtube.com/watch?v=62-pRVZuS5c for a good explanaition
        #p = abs(point)-self.position
        #distance = sqrt(max(p.x,0)**2+max(p.y,0)**2)
        point = apply_rotation(point-self.pos,self.rotation*-1)#+self.pos
        p = abs(point)-self.dimensions
        return sqrt(max(p.x,0)**2+max(p.y,0)**2+max(p.z,0)**2)+min(max(p.x,max(p.y,p.z)),0)#the second term is for the points inside the cuboid

#got the sdf from https://iquilezles.org/articles/distfunctions/
class Donut(Primitive): #whoever thinks its spelled doughnut,youre wrong
    def __init__(self,position,donut_radius,ring_radius,material):#first radius for radius of donut,second for the circle shape or thickness
        super().__init__(position,material)
        self.radii = donut_radius,ring_radius#yes that the actual plural of radius look it up!,donut_radius->radius,ring_radius_>"thickness of donut"
    
    def sdf(self,point):
        point = apply_rotation(point-self.pos,self.rotation*-1)+self.pos
        p = point-self.pos
        #in this case p.y is seperate as the y axis is the up and down axis
        return sqrt((sqrt(p.x**2+p.z**2)-self.radii[0])**2+p.y**2)-self.radii[1]

class InfinitePlane(Primitive):
    def __init__(self,height,material):
        super().__init__(Vector3(0,height,0),material)
    
    def sdf(self,point):
        return self.pos.y-point.y#the -1 is cuz y up is negative cuz idk
"""class SierpinskiTriangle:#try saying that 3 times fast lol
    def __init__(self,)"""