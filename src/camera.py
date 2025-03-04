from vector import Vector3,apply_rotation
from math import radians,tan

class Camera:
    def __init__(self,position:Vector3,field_of_view):
        self.pos = position
        self.fov = field_of_view
        self.rotation = Vector3(0,0,0)

    def get_ray(self,x,y):
        dist_to_eye = 1/tan(radians(self.fov/2))
        ray_pos = apply_rotation(Vector3(x,y,dist_to_eye),self.rotation)+self.pos
        ray_dir = (ray_pos-self.pos).normalize()
        return ray_pos,ray_dir