import math
import copy
from core.models.toolpath import ToolpathPoint, ToolpathSegment
from core.optimizer.code_cleaner import CodeCleaner
from core.optimizer.feed_optimizer import FeedOptimizer
from core.optimizer.motion_smoother import MotionSmoother

SAFE_Z = 5.0


class PathOptimizer:

    def __init__(self):
        self.cleaner = CodeCleaner()
        self.feed_optimizer = FeedOptimizer()
        self.smoother = MotionSmoother()

    def optimize(self, toolpath):
        #  Step 1: clean
        toolpath = self.cleaner.clean(toolpath)

        # Step 2: air cut fix
        toolpath = self.remove_air_cuts(toolpath)

        # Step 3: merge
        toolpath = self.merge_collinear(toolpath)

        # Step 4: path order optimization
        toolpath = self.optimize_cut_order(toolpath)

        #  Step 5: ML feed optimization
        toolpath = self.feed_optimizer.optimize(toolpath)

        #  Step 6: smoothing
        toolpath = self.smoother.smooth(toolpath)

        return toolpath

    def merge_collinear(self, toolpath):
        if len(toolpath) == 0:
            return []

        result = [toolpath[0]]

        for i in range(1, len(toolpath)):
            prev = result[-1]
            curr = toolpath[i]

            if self.is_collinear(prev, curr) and prev.move_type == curr.move_type:
                prev.end = curr.end
            else:
                result.append(curr)

        return result

    def is_collinear(self, s1, s2):
        dx1 = s1.end.x - s1.start.x
        dy1 = s1.end.y - s1.start.y
        dx2 = s2.end.x - s2.start.x
        dy2 = s2.end.y - s2.start.y
        return dx1 * dy2 == dy1 * dx2

    def remove_air_cuts(self, toolpath):
        optimized = []

        for seg in toolpath:
            if seg.move_type == "G00" and seg.end.z < 0:
                seg.move_type = "G01"

            elif seg.move_type == "G01":
                if seg.start.z > SAFE_Z and seg.end.z > SAFE_Z:
                    seg.move_type = "G00"

            optimized.append(seg)

        return optimized

    def optimize_cut_order(self, toolpath):
        
        cuts=copy.deepcopy(toolpath)

        if len(cuts) == 0:
            return toolpath

        optimized = []
        current = cuts[0]
        optimized.append(current)
        cuts = cuts[1:]

        while len(cuts) > 0:
            best_seg = None
            best_dist = float("inf")

            for s in cuts:
                d = self.distance(current.end, s.start)
                if d < best_dist:
                    best_dist = d
                    best_seg = s

            cuts.remove(best_seg)

            if not self.same_point(current.end, best_seg.start):
                transition_moves = self.create_safe_transition(current, best_seg)
                optimized.extend(transition_moves)

            optimized.append(best_seg)
            current = best_seg

        return optimized

    def same_point(self, p1, p2):
        return p1.x == p2.x and p1.y == p2.y and p1.z == p2.z

    def create_safe_transition(self, current, next_seg):
        moves = []
        current_end = current.end
        next_start = next_seg.start

        if current_end.z < SAFE_Z:
            up_point = ToolpathPoint(current_end.x, current_end.y, SAFE_Z)
            moves.append(ToolpathSegment(current_end, up_point, "G00"))

        start_safe = ToolpathPoint(current_end.x, current_end.y, SAFE_Z)
        end_safe = ToolpathPoint(next_start.x, next_start.y, SAFE_Z)

        if not self.same_point(start_safe, end_safe):
            moves.append(ToolpathSegment(start_safe, end_safe, "G00"))

        if next_start.z < SAFE_Z:
            down_start = ToolpathPoint(next_start.x, next_start.y, SAFE_Z)
            moves.append(ToolpathSegment(down_start, next_start, "G01"))

        return moves

    def distance(self, p1, p2):
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        dz = p1.z - p2.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)