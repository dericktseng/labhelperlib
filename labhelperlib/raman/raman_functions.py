from matplotlib.figure import Figure
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib import colors
import cycler
from . import raman_helper as rh

__all__ = ['plot_polarized']

def plot_polarized(datafile: Path,
         peaks: dict[str, tuple[float,float]],
         savefile=None,
         vertical=True,
         connect_final=False) -> tuple[Figure, Figure]:
    """
    datafile - Path to the polarized raman txt file to process.
    peaks - dictionary of the form: {'peakname': (low_bound, top_bound), ...} e.g.
        {
            'a1g': (170, 190),
            'e2g': (230, 250),
            'substrate': (500, 550),
        }
    savefile - location to save file, or None if we don't want to.
    vertical - plots vertical guides on heatmap if True.
    returns: matplotlib figures for heatmap and polar plot.
    """

    # plot is [left, right] = [heatmap, polarized]
    fig_heat, ax_heat = plt.subplots()

    # loads data from file
    datapts = np.loadtxt(datafile)

    # normalize the intensities to the maximum intensity of all spectra
    max_intensity = np.max(datapts[:,2])
    datapts[:,2] = datapts[:,2] / max_intensity

    # split the datapts into sections (spectrum) of constant polarization angle
    # each section in sections is 1 raman scan (one for each polarization angle)
    pol_uniq, index_uniq = np.unique(datapts[:,0], return_index=True)
    pol_sections = np.array(np.split(datapts, index_uniq[1:]))
    pol_sections = np.flip(pol_sections, axis=1)

    # plots the intensity map
    intensitymap = pol_sections[:,:,2]
    ramanshift = pol_sections[0,:,1]
    ramanshift_posts = rh.generate_posts(ramanshift)
    pol_posts = rh.connect_final_init_pt(pol_uniq, 360)
    colorbar = ax_heat.pcolormesh(ramanshift_posts, pol_posts, intensitymap)
    fig_heat.colorbar(colorbar, ax=ax_heat)
    ax_heat.set_xlabel('Raman Shift')
    ax_heat.set_ylabel('Polarization angle')

    # draws vertical line guides on the heatmap
    # additionally draws the polar plots
    colorcycle = cycler.cycler('color', colors.TABLEAU_COLORS)
    fig_polars = plt.figure(figsize=(10, 5))
    for i, (c, name) in enumerate(zip(colorcycle, peaks)):
        # vertical line guides.
        peakrange = peaks[name]
        c = c['color']

        if vertical:
            bottom = np.min(pol_posts)
            top = np.max(pol_posts)
            ax_heat.vlines(peakrange, bottom, top, colors=c, label=name, linestyles='dotted')

        # draws the polar plots as well
        ax = plt.subplot(1, len(peaks), i+1, polar=True)
        ax.set_yticklabels([])
        
        # normalizes integrated intensities
        integrated_intensities = rh.integrate_in_range(ramanshift, intensitymap, *peakrange)
        integrated_intensities = integrated_intensities / np.max(integrated_intensities)
        plot_pol = pol_uniq
        plot_int = integrated_intensities
        if connect_final:
            spacing = (pol_uniq[-1] - pol_uniq[-2])
            plot_pol = rh.connect_final_init_pt(pol_uniq, pol_uniq[-1] + spacing)
            plot_int = rh.connect_final_init_pt(integrated_intensities, integrated_intensities[0])
        ax.plot(np.deg2rad(plot_pol), plot_int, color=c, marker='o')

    fig_polars.tight_layout()
    ax_heat.legend(bbox_to_anchor=(1.45, 0), loc='lower right')

    if savefile is not None:
        fig_heat.savefig(f'heatmap_{savefile}', dpi=600, bbox_inches='tight')
        fig_polars.savefig(f'polar_{savefile}', dpi=600, bbox_inches='tight')
    return fig_heat, fig_polars
