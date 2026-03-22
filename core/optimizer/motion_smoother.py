import math


class MotionSmoother:
    def smooth(self, toolpath, angle_threshold=30):
        smoothed = [toolpath[0]]

        for i in range(1, len(toolpath) - 1):
            prev = toolpath[i - 1]
            curr = toolpath[i]
            next_seg = toolpath[i + 1]

            angle = self.calculate_angle(prev, curr, next_seg)

            if angle < angle_threshold:
                if curr.feed:
                    curr.feed *= 0.7

            smoothed.append(curr)

        smoothed.append(toolpath[-1])
        return smoothed

    def calculate_angle(self, s1, s2, s3):
        v1 = (
            s1.end.x - s1.start.x,
            s1.end.y - s1.start.y
        )
        v2 = (
            s2.end.x - s2.start.x,
            s2.end.y - s2.start.y
        )

        dot = v1[0]*v2[0] + v1[1]*v2[1]
        mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2)

        if mag1 == 0 or mag2 == 0:
            return 180

        cos_theta = dot / (mag1 * mag2)
        return math.degrees(math.acos(max(min(cos_theta, 1), -1)))