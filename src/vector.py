from math import sqrt,radians,cos,sin

class Vector3:
    def __init__(self,x,y,z):
        self.coords = self.x,self.y,self.z = (x,y,z)
    
    def __add__(self,other):
        return Vector3(self.x+other.x,self.y+other.y,self.z+other.z)
    
    def __sub__(self,other):
        return Vector3(self.x-other.x,self.y-other.y,self.z-other.z)
    
    def __mul__(self,other):
        #add multiplication of two vectors later on mabye rn i jsut need it if i decide to do raymarching
        if type(other) is Vector3:
            return Vector3(self.x*other.x,self.y*other.y,self.z*other.z)
        return Vector3(self.x*other,self.y*other,self.z*other)
    
    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __truediv__(self,other):
        return Vector3(self.x/other,self.y/other,self.z/other)
    
    def __mod__(self,other):
        return Vector3(self.x%other,self.y%other,self.z%other)
    
    def __abs__(self):
        return Vector3(abs(self.x),abs(self.y),abs(self.z))
    
    def __str__(self):#built in fun called by python when using print fun
        return f"Vector3(   {self.x},   {self.y},   {self.z})"
    
    def length(self):
        return sqrt(self.x**2+self.y**2+self.z**2)
    
    def normalize(self):
        l = self.length()
        if l == 0:
            return Vector3(0,0,0)
        return Vector3(self.x/l,self.y/l,self.z/l)

    def dot_product(self,other):#aka scalar product
        return self.x*other.x+self.y*other.y+self.z*other.z
    
    def reflect(self,normal):#reflect vector along normal(also a Vector3) (normal must be normalized)
        return self-(2*self.dot_product(normal)*normal)
    
    def refract(self,normal,refraction_indices_ratio):#https://web.cse.ohio-state.edu/~shen.94/681/Site/Slides_files/reflection_refraction.pdf
        cosI = -self.dot_product(normal)
        sinT2 = refraction_indices_ratio**2*(1-cosI**2)
        if sinT2 > 1:
            return Vector3(0,0,0)#invalid
        cosT = sqrt(1-sinT2)
        return refraction_indices_ratio*self+ (refraction_indices_ratio*cosI-cosT)*normal
        #return (refraction_indices_ratio*self.dot_product(normal)-sqrt((1-refraction_indices_ratio**2)*(1-self.dot_product(normal)**2)))*normal -refraction_indices_ratio*self
    
    def to_rgb(self):
        return max(min(self.x*255,255),0),max(min(self.y*255,255),0),max(min(self.z*255,255),0)#convert from range 0,1 to range 0,255 and clip anything outside that domain

class Vec3(Vector3):
    pass

#https://en.wikipedia.org/wiki/Rotation_matrix
def rotation_x(point:Vector3,angle):
    y = cos(angle)*point.y-sin(angle)*point.z
    z = sin(angle)*point.y+cos(angle)*point.z
    return Vector3(point.x,y,z)

def rotation_y(point:Vector3,angle):
    x = cos(angle)*point.x+sin(angle)*point.z
    z = -sin(angle)*point.x+cos(angle)*point.z
    return Vector3(x,point.y,z)

def rotation_z(point:Vector3,angle):
    x = cos(angle)*point.x-sin(angle)*point.y
    y = sin(angle)*point.x+cos(angle)*point.y
    return Vector3(x,y,point.z)

def apply_rotation(point:Vector3,rotations:Vector3):
    return rotation_z(rotation_y(rotation_x(point,rotations.x),rotations.y),rotations.z)
    
if __name__ == '__main__':#testing
    a = Vector3(10,5,8)
    b = Vector3(2,3,1)
    print(a+b)
    a = a.normalize()
    print(a)
    print(a*15,(a*15).length())