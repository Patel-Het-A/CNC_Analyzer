class CodeCleaner:
    def clean(self, toolpath):
        cleaned = []

        for seg in toolpath:
            if (seg.start.x == seg.end.x and
                seg.start.y == seg.end.y and
                seg.start.z == seg.end.z):
                continue

            cleaned.append(seg)

        return cleaned