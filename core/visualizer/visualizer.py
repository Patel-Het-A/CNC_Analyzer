from core.visualizer.plot_3d import Plot3D
import math


class Visualizer:

    def __init__(self):
        self.plot3d = Plot3D()

    def show_2d(self, toolpath):
        self.plot2d.plot(toolpath)

    def show_3d(self, toolpath,original_distance,optimized_toolpath,optimized_distance,scale):
        self.plot3d.plot(toolpath,original_distance,optimized_toolpath,optimized_distance,scale)

    def animate(self, toolpath):
        self.animator.animate(toolpath)

    def show_all(self, toolpath):
        # optional combined view
        self.show_2d(toolpath)
        self.show_3d(toolpath)
        self.animate(toolpath)


    def total_distance(self,toolpath):
        total = 0.0

        for seg in toolpath:
            dx = seg.end.x - seg.start.x
            dy = seg.end.y - seg.start.y
            dz = seg.end.z - seg.start.z

            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            total += dist

        return total