from vector import Vector3
from lights import Light

class Scene:
    def __init__(self,*args):
        self.objects = list(args)
        self.lights = []
    
    def add(self,obj):
        if type(obj) is Light:
            self.lights.append(obj)
        else:
            self.objects.append(obj)
    
    def get_distance(self,point:Vector3):
        distances = [(obj.sdf(point),obj) for obj in self.objects]
        return min(distances,key= lambda dist_and_obj : dist_and_obj[0])