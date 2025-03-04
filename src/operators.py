#max min smooth min etc.
from vector import Vector3
from primitives import Primitive

class Operator(Primitive):
    def __init__(self,obj1,obj2,position=Vector3(0,0,0)):
        super().__init__(position,None)
        self.pos = Vector3(0,0,0)
        self.material = obj1.material#just in case change later
        try:
            self.obj1,self.sign1 = obj1
        except TypeError:#self.sign1 doesnt exist
            self.obj1,self.sign1 = obj1,1

        try:
            self.obj2,self.sign2 = obj2
        except TypeError:
            self.obj2,self.sign2 = obj2,1
    def get_color_at(self, point: Vector3):
        return self.obj1.get_color_at(point)
    
class Max(Operator):
    def sdf(self,point):
        return max(self.obj1.sdf(point)*self.sign1,self.obj2.sdf(point)*self.sign2)
    
    def get_color_at(self,point):
        return self.obj1.get_color_at(point)

class SmoothMin(Operator):
    def __init__(self,obj1,obj2,k:float):
        super().__init__(obj1,obj2)
        self.k = k
        #self.last_h = 0
    
    def sdf(self,point):
        dist1 = self.obj1.sdf(point)*self.sign1
        dist2 = self.obj2.sdf(point)*self.sign2

        h = dist1-dist2
        h = max(min(0.5+0.5*h/self.k,1),0)#turn values from [-k,k] to [0,1] and 'clamp' to range if larger
        dist = dist1*(1-h)+dist2*h - self.k*h*(1-h)
        #self.last_h = h
        return dist
    
    def get_color_at(self,point):
        dist1 = self.obj1.sdf(point)*self.sign1
        dist2 = self.obj2.sdf(point)*self.sign2

        h = dist1-dist2
        h = max(min(0.5+0.5*h/self.k,1),0)
        color1 = self.obj1.get_color_at(point)
        color2 = self.obj2.get_color_at(point)

        return color1*(1-h)+color2*h - (self.k*h*(1-h)*Vector3(1,1,1))


if __name__ == '__main__':
    from primitives import *
    obj1 = Sphere(Vector3(0,0,0),1,None)
    obj2 = Sphere(Vector3(1,0,0),2,None)
    m = Max(-obj1,obj2)
    print(m.sdf(Vector3(1,1,1)))
