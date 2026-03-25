import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class Plot3D:

    def set_equal_axes(self,ax):
        limits = [
                ax.get_xlim3d(),
                ax.get_ylim3d(),
                ax.get_zlim3d()
        ]
        spans = [lim[1] - lim[0] for lim in limits]
        centers = [(lim[0] + lim[1]) / 2 for lim in limits]
        radius = max(spans) / 2

        ax.set_xlim3d([centers[0] - radius, centers[0] + radius])
        ax.set_ylim3d([centers[1] - radius, centers[1] + radius])
        ax.set_zlim3d([centers[2] - radius, centers[2] + radius])



    def highlight_issues(self,issues):
        issue_lines = [i.line_number for i in issues]

        return issue_lines

    def plot(self, original,original_distance, optimized_toolpath,optimized_distance,scale,issues):

    # -------- ORIGINAL --------
        fig1 = plt.figure("Toolpath Comparison")
        fig1.text(
    0.30, 0.07,
    f"Distance: {original_distance:.2f} {'mm' if scale == 'G21' else 'inch'}",
    ha='center',
    fontsize=13
)
        
        issue_lines=self.highlight_issues(issues)

           





        ax1 = fig1.add_subplot(121, projection='3d')
        ax1.set_title("Original Toolpath",fontsize=20,fontweight='bold')
        for seg in original:
            x = [seg.start.x, seg.end.x]
            y = [seg.start.y, seg.end.y]
            z = [seg.start.z, seg.end.z]

            if seg.line_number in issue_lines:
                ax1.plot(x, y, z, 'r-')
            else:
                if seg.move_type == "G00":
                    ax1.plot(x, y, z, 'y--')
                else:
                    ax1.plot(x, y, z, 'b-')

        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")


        # -------- OPTIMIZED --------
        
        fig1.text(
    0.75, 0.07,
    f"Distance: {optimized_distance:.2f} {'mm' if scale == 'G21' else 'inch'}",
    ha='center',
    fontsize=13
        )

        ax2 = fig1.add_subplot(122, projection='3d')
        ax2.set_title("Optimized Toolpath",fontsize=20,fontweight='bold')


        for seg in optimized_toolpath:
            x = [seg.start.x, seg.end.x]
            y = [seg.start.y, seg.end.y]
            z = [seg.start.z, seg.end.z]
            

            if seg.move_type == "G00":
                    ax2.plot(x, y, z, 'y--')
            else:
                    ax2.plot(x, y, z, 'g-')  # green for optimized cut

        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        ax2.set_zlabel("Z")


        legend_elements = [
            Line2D([0], [0], color='yellow', linestyle='--', label='Rapid (G00)'),
            Line2D([0], [0], color='blue', linestyle='-', label='Cutting (Original)'),
             Line2D([0], [0], color='green', linestyle='-', label='Cutting (Optimized)'),
             Line2D([0], [0], color='red', linestyle='-', label='Issue')
            
        ]
        

        fig1.legend(
        handles=legend_elements,
        loc='upper right',
        ncol=1,
        fontsize=10
    )

        self.set_equal_axes(ax1)
        self.set_equal_axes(ax2)

        plt.show()