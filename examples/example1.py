#example of how to use libary to render a scene
from src import *
from math import radians

engine = RenderEngine()
screen = pygame.display.set_mode((640,360))#create pygame window to be used for rendering


material1 = CheckeredMaterial(Vector3(0.2,0.1,0.4),Vector3(1,0.9,0.7),shinyness=0.0)
engine.add(InfinitePlane(0.5,material1))#creates plane primitive and adds it to the scene to be rendered

engine.add(Light(Vector3(1,-1,-1),Vector3(1,0.1,0.3)))
engine.add(Light(Vector3(-1,-1,-0.8),Vector3(0.5,1,1)))
        
engine.camera = Camera(Vector3(0,-1,-3),field_of_view=60)
engine.camera.rotation.x = -radians(15)

#engine.render(screen)#renders image of scene from camera
engine.render_and_display_rows(screen)#renders image of scene from camera and displays rows while rendering
