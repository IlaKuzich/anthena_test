import matplotlib.pyplot as plt

from matplotlib.projections import PolarAxes
from matplotlib.transforms import Affine2D
from mpl_toolkits.axisartist import Axes, HostAxes, angle_helper
from mpl_toolkits.axisartist.grid_helper_curvelinear import \
    GridHelperCurveLinear

import numpy as np
import csv

def curvelinear_diagram(fig, diagram_0, diagram_20, diagram_40, diagram_60, freq):
    tr = Affine2D().scale(np.pi/180, 1) + PolarAxes.PolarTransform()
    extreme_finder = angle_helper.ExtremeFinderCycle(
        nx=20, ny=20,  # Number of sampling points in each direction.
        lon_cycle=360, lat_cycle=None,
        lon_minmax=None, lat_minmax=(0, np.inf),
    )

    grid_locator1 = angle_helper.LocatorDMS(12)
    tick_formatter1 = angle_helper.FormatterDMS()

    grid_helper = GridHelperCurveLinear(
        tr, extreme_finder=extreme_finder,
        grid_locator1=grid_locator1, tick_formatter1=tick_formatter1)
    ax1 = fig.add_subplot(
        1, 1, 1, axes_class=HostAxes, grid_helper=grid_helper)


    # make ticklabels of right and top axis visible.
    ax1.axis["right"].major_ticklabels.set_visible(True)
    ax1.axis["top"].major_ticklabels.set_visible(True)
    # let right axis shows ticklabels for 1st coordinate (angle)
    ax1.axis["right"].get_helper().nth_coord_ticks = 0
    # let bottom axis shows ticklabels for 2nd coordinate (radius)
    ax1.axis["bottom"].get_helper().nth_coord_ticks = 1

    print(diagram_0.shape)
    d_min = np.amin(diagram_0, axis=0)
    d_max = np.amax(diagram_0, axis=0)
    diagram_0 = diagram_0 - d_min + (d_max - d_min) / 2
    diagram_20 = diagram_20 - d_min + (d_max - d_min) / 2
    diagram_40 = diagram_40 - d_min + (d_max - d_min) / 2
    diagram_60 = diagram_60 - d_min + (d_max - d_min) / 2

    border = np.amax(diagram_0)
    print(border)

    ax1.set_aspect(1)
    ax1.set_xlim(-border, border)
    ax1.set_ylim(-border, border)

    ax1.grid(True, zorder=0)

    ax2 = ax1.get_aux_axes(tr)
    ax1.title.set_text(f'LPDA Diagram. Frequency {freq}')

    ax2.plot(np.linspace(0, 360 * 13, 36 * 13), diagram_0, linewidth=2)
    ax2.plot(np.linspace(0, 360 * 13, 36 * 13), diagram_20, linewidth=2)
    ax2.plot(np.linspace(0, 360 * 13, 36 * 13), diagram_40, linewidth=2)
    ax2.plot(np.linspace(0, 360 * 13, 36 * 13), diagram_60, linewidth=2)


if __name__ == "__main__":
    with open('Diagrams_final.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader, None) #skip header
        unsplitted_data = np.asarray(list(reader))

        data = np.apply_along_axis(lambda s: np.asarray(str(s).split(";")), -1, unsplitted_data)

        reshaped = np.reshape(data, newshape=(4, 36, 21, 13, 8))
        for f in range(0, 21):
            # print(reshaped[:, :, f, 0, 2:6])
            diagram_0 = np.reshape(reshaped[0, :, f, :, 5].swapaxes(0,1), newshape=(36*13,)).astype(float)
            diagram_20 = np.reshape(reshaped[1, :, f, :, 5].swapaxes(0, 1), newshape=(36 * 13,)).astype(float)
            diagram_40 = np.reshape(reshaped[2, :, f, :, 5].swapaxes(0, 1), newshape=(36 * 13,)).astype(float)
            diagram_60 = np.reshape(reshaped[3, :, f, :, 5].swapaxes(0, 1), newshape=(36 * 13,)).astype(float)

            fig = plt.figure()
            curvelinear_diagram(fig, diagram_0, diagram_20, diagram_40, diagram_60, reshaped[0, 0, f, 0, 4])
            plt.show()
