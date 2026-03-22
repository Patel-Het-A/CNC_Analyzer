import matplotlib.pyplot as plt

class Plot3D:

    def plot(self, original,original_distance, optimized_toolpath,optimized_distance,scale):

    # -------- ORIGINAL --------
        fig1 = plt.figure("Original Toolpath")
        fig1.text(
    0.5, 0.02,
    f"Distance: {original_distance:.2f} {'mm' if scale == 'G21' else 'inch'}",
    ha='center',
    fontsize=10
)
        ax1 = fig1.add_subplot(111, projection='3d')

        for seg in original:
            x = [seg.start.x, seg.end.x]
            y = [seg.start.y, seg.end.y]
            z = [seg.start.z, seg.end.z]

            if seg.move_type == "G00":
                ax1.plot(x, y, z, 'r--')
            else:
                ax1.plot(x, y, z, 'b-')

        ax1.set_title("Original Toolpath")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")


        # -------- OPTIMIZED --------
        fig2 = plt.figure("Optimized Toolpath")

        fig2.text(
    0.5, 0.02,
    f"Distance: {optimized_distance:.2f} {'mm' if scale == 'G21' else 'inch'}",
    ha='center',
    fontsize=10
)
        ax2 = fig2.add_subplot(111, projection='3d')

        for seg in optimized_toolpath:
            x = [seg.start.x, seg.end.x]
            y = [seg.start.y, seg.end.y]
            z = [seg.start.z, seg.end.z]

            if seg.move_type == "G00":
                ax2.plot(x, y, z, 'r--')
            else:
                ax2.plot(x, y, z, 'g-')  # green for optimized cut

        ax2.set_title("Optimized Toolpath")
        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        ax2.set_zlabel("Z")

        plt.show()