from core.visualizer.plot_3d import Plot3D
import math


class Visualizer:

    def __init__(self):
        self.plot3d = Plot3D()

   

    def show_3d(self, toolpath,original_distance,optimized_toolpath,optimized_distance,scale,issues):
        self.plot3d.plot(toolpath,original_distance,optimized_toolpath,optimized_distance,scale,issues)
        

  



    def total_distance(self,toolpath):
        total = 0.0

        for seg in toolpath:
            dx = seg.end.x - seg.start.x
            dy = seg.end.y - seg.start.y
            dz = seg.end.z - seg.start.z

            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            total += dist

        return total