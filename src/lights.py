from vector import Vector3

class Light:
    def __init__(self,position,color=Vector3(1,1,1)):#Simple point light
        self.pos = position
        self.color = color
        self.ambient = 0.15
        self.specular = 0.5