class Metrics:

    def calculate(self, toolpath):
        total = 0.0
        cutting = 0.0
        air = 0.0

        for seg in toolpath:
            dx = seg.end.x - seg.start.x
            dy = seg.end.y - seg.start.y
            dz = seg.end.z - seg.start.z

            dist = (dx**2 + dy**2 + dz**2) ** 0.5
            total += dist

            if seg.is_cutting:
                cutting += dist
            else:
                air += dist

        efficiency = (cutting / total * 100) if total else 0

        return {
            "total": round(total, 2),
            "cutting": round(cutting, 2),
            "air": round(air, 2),
            "efficiency_%": round(efficiency, 2)
        }