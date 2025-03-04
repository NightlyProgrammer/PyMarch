import pygame#for window managment and so on also used
from scene import Scene
from camera import Camera
from vector import Vector3
from primitives import *
from material import *
from math import radians
from lights import Light
from operators import *
from os import listdir

class Ray:
    def __init__(self,position,direction):
        self.pos = position
        self.dir = direction
    def march(self,distance):#marches a distance in the direction of ray
        self.pos += self.dir*distance
        
class RenderEngine:
    def __init__(self):
        self.scene = Scene()
        self.camera = Camera(Vector3(0,0,0),45)
    
    def add(self,scene_obj):
        self.scene.add(scene_obj)
            
    def phong(self,obj,hit_pos,view_dir):#used this for reflection and refraction https://web.cse.ohio-state.edu/~shen.94/681/Site/Slides_files/reflection_refraction.pdf
        ambient,diffuse,specular = Vector3(0,0,0),Vector3(0,0,0),Vector3(0,0,0)

        normal = obj.get_normal(hit_pos)
        for light in self.scene.lights:
            
            ambient += light.color*light.ambient
            #diffuse
            
            light_dir = (light.pos-hit_pos).normalize()
            shadow_march = self.raymarch(Ray(hit_pos+(light_dir*0.01),light_dir),inf_dist=(light.pos-hit_pos).length())[0]
            if shadow_march is None:#so that it doesnt collide with previosu hit püos
                diffuse_impact = max((light_dir.dot_product(normal)),0)#in this case the dot product basiclly tells us how closley the light_dir and obj normal "align"
                diffuse += light.color*diffuse_impact
                #specular(shiny spots)
                #view_dir = ray.dir
                reflect_dir = (-1*light_dir).reflect(normal)
                spec = max(view_dir.dot_product(reflect_dir),0)**24#the higher the exponent the smaller the shiny spot
                specular += spec*light.specular*light.color
            #else:
                #print(shadow_march)

        return ((ambient+diffuse+specular)*obj.get_color_at(hit_pos))
    
    def calculate_color(self,start_ray,recursion_depth=8):
        #max_reflections_recursions = 8
        #raymrach through mutliple glass and mirror thingys
        color = Vector3(0,0,0)

        obj,inside_obj = self.raymarch(start_ray)
        if obj is not None:
            #c= ((obj+Vector3(1,1,1))/2*255).coords
            color += self.phong(obj,start_ray.pos,-1*start_ray.dir)#*(1-obj.material.reflection_factor)
            if recursion_depth > 0:
                normal = obj.get_normal(start_ray.pos)
                if obj.material.reflection_factor > 0:
                    new_ray_dir = (start_ray.dir).reflect(normal)
                    color += obj.material.reflection_factor*self.calculate_color(Ray(start_ray.pos+(new_ray_dir*0.01),new_ray_dir),recursion_depth=recursion_depth-1)
                """if obj.material.is_transparent:
                    refraction_ratio = obj.material.refraction_index/TransparentMaterial.refraction_indices["air"]
                    if inside_obj:
                        refraction_ratio = 1/refraction_ratio
                    new_ray_dir = (start_ray.dir).refract(normal,refraction_ratio)
                    if new_ray_dir.length() != 0:
                        sign = -1
                        if inside_obj:
                            sign = 1
                        color += obj.material.refraction_factor*self.calculate_color(Ray(start_ray.pos+(new_ray_dir*0.01),new_ray_dir*-sign),recursion_depth=recursion_depth-1)#refraction factor is how much liught can pass through rename to better name if im not llazy"""
            return color
        return color#(min(10/obj,255),min(5/obj,255),min(2/obj,255))
    
    def raymarch(self,ray,inf_dist=100):
        hit_dist = 0.0001
        #inf_dist = 100
        #smallest_dist = inf_dist
        distance_traveled = 0
        #i = 0#should matter but just in case for some reasion the distance traveled goes up and down for infinity
        while distance_traveled<inf_dist:
            dist,obj = self.scene.get_distance(ray.pos)
            #smallest_dist = min(smallest_dist,dist)
            distance_traveled += dist
            ray.march(dist)
            if abs(dist)<=hit_dist:
                return obj,dist<0
            #i += 1
        return None,None#,smallest_dist
    
    def render(self,surface):
        size = surface.get_size()
        aspect_ratio = size[1]/size[0]
        for y in range(size[1]):
            for x in range(size[0]):
                ray = Ray(*self.camera.get_ray(x/size[0]*2-1,(y/size[1]*2-1)*aspect_ratio))#covnvert x to range -1,1 and y accordingly
                surface.set_at((x,y),self.calculate_color(ray).to_rgb())
    
    def render_and_display_rows(self,screen):
        size = screen.get_size()
        aspect_ratio = size[1]/size[0]
        time_stamp1 = pygame.time.get_ticks()
        for y in range(size[1]):
            for x in range(size[0]):
                ray = Ray(*self.camera.get_ray(x/size[0]*2-1,(y/size[1]*2-1)*aspect_ratio))#change this shitty ray expression by having ray class in sepereate folder
                col = self.calculate_color(ray).to_rgb()
                screen.set_at((x,y),col)
                temp_time_stamp = pygame.time.get_ticks()
                time = round((temp_time_stamp-time_stamp1)*0.001)
                h,m,s = time//3600,time//60%60,time%60
                pygame.display.set_caption(f"{x},{y}    {h}h, {m}m, {s}s")
                for event in pygame.event.get([pygame.QUIT]):
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            pygame.display.flip()
        time_stamp2 = pygame.time.get_ticks()
        time = round((time_stamp2-time_stamp1)*0.001)
        h,m,s = time//3600,time//60%60,time%60
        
        pygame.display.set_caption(f"Finished: {h} hours, {m} minutes, {s} seconds")
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get([pygame.QUIT,pygame.KEYDOWN]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        try:
                            pygame.image.save(screen,f"images/screenshot{len(listdir('images'))}.png")
                        except:
                            pygame.image.svae(screen,f"screenshot.png")
                    

if __name__ == '__main__':
    pygame.init()
    engine = RenderEngine()
    engine.add(InfinitePlane(0.5,CheckeredMaterial(Vector3(0.2,0.1,0.4),Vector3(1,0.9,0.7),shinyness=0.0)))

    engine.add(Light(Vector3(1,-1,-1),Vector3(1,0.1,0.3)))
    engine.add(Light(Vector3(-1,-1,-0.8),Vector3(0.5,1,1)))
        
    engine.camera = Camera(Vector3(0,-1,-3),60)
    engine.camera.rotation.x = -radians(15)
    #engine.scene.add(Sph)
    engine.scene.add(Sphere(Vector3(0,0,0),0.5,BasicMaterial(Vector3(1,1,1))))
    screen = pygame.display.set_mode((640,360))#(1280,720))
    engine.render_and_display_rows(screen)