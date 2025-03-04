from math import floor

class Material:
    def __init__(self,color,shinyness:float =0.0):
        self.color = color
        self.reflection_factor = shinyness
        self.is_transparent = False
    
    def get_at(self,position):
        return self.color
    
class BasicMaterial(Material):#simple material that only returns one color
    pass

class CheckeredMaterial(Material):
    def __init__(self,color1,color2,scale=1,shinyness=0):
        super().__init__(color1,shinyness)
        self.color2 = color2
        self.scale = scale
    
    def get_at(self,position):
        isEven = (floor(position.x/self.scale)+floor(position.y/self.scale)+floor(position.z/self.scale))%2
        if isEven==0:
            return self.color
        return self.color2

class TransparentMaterial(Material):
    refraction_indices = {
        "air":1,
        "glass":1.5
    }
    def __init__(self,color,refraction_index,kt):
        super().__init__(color)
        self.is_transparent = True
        self.refraction_index = refraction_index
        self.refraction_factor= kt
    
    def get_at(self,position):
        return self.color