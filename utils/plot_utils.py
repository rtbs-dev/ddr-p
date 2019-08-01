import math
import matplotlib.pyplot as plt
from os import fspath
import subprocess
import tempfile
import seaborn as sns
import logging

""" modified from: 
https://github.com/Wookai/paper-tips-and-tricks/blob/master/src/python/
"""

# ### ENTER HERE ### #
# #from tex command `\showthe\<x>{width,height}`
COLUMN_WIDTH = 241.38208  # pt
TEXT_WIDTH = 495.04993  # pt
TEXT_HEIGHT = 694.7  # pt
# ################## #

COLUMN_WIDTH /= 72.47  # pt to inches for latex
TEXT_WIDTH /= 72.47
TEXT_HEIGHT /= 72.47



"""
The following functions can be used by other scripts to get/set the sizes of
the various elements of the figures, manually (to override this default).
"""


def label_size():
    """Size of axis labels
    """
    return 8


def font_size():
    """Size of all texts shown in plots
    """
    return 8


def ticks_size():
    """Size of axes' ticks
    """
    return 6


def axis_lw():
    """Line width of the axes
    """
    return 0.6


def plot_lw():
    """Line width of the plotted curves
    """
    return 1.5


def figure_setup():
    """Set all the sizes to the correct values.
    TODO: use tex fonts for all texts, if installed
    """

    # This sets reasonable defaults for font size in a paper
    sns.set_context("paper")
    # Set the font to be serif, rather than sans
    sns.set(font='serif')
    # Make the background white, and specify the specific font family
    sns.set_style("white", {
        "font.family": "serif",
        "font.serif": ["Times", "Palatino", "serif"],
        'figure.dpi': 200,
        'font.size': font_size(),
        'legend.fontsize': label_size(),
        'figure.titlesize': font_size(),
        'axes.titlesize': font_size(),
        'axes.labelsize': label_size(),
        'axes.linewidth': axis_lw(),
        'legend.fontsize': font_size(),
        'xtick.labelsize': ticks_size(),
        'ytick.labelsize': ticks_size(),
    })


def figsize(fig_width=None, fig_height=None, columns=1, aspect='phi'):
    """helper to define figsize based on columns
    If no height is given, it is computed using the golden ratio.
    """
    assert (columns in [1, 2])
    assert (aspect in ['phi', 'square']) or isinstance(aspect, float)

    ratios = {
        'phi': (1. + math.sqrt(5.))/2.,
        'square': 1.,
    }
    if aspect in ['phi', 'square']:
        aspect = 1./ratios[aspect] if columns == 1 else ratios[aspect]
    elif isinstance(aspect, float):
        pass
    else:
        raise TypeError("`aspect` must be one of {'phi', 'square'} or `float`")

    if fig_width is None:
        fig_width = COLUMN_WIDTH if columns == 1 else TEXT_WIDTH

    if fig_height is None:
        fig_height = fig_width / aspect

    return fig_width, fig_height


def save_fig(fig, file_name, fmt=None, dpi=300, tight=True):
    """Save a Matplotlib figure as EPS/PNG/PDF to the given path and trim it.
    """

    if not fmt:
        fmt = file_name.suffix  # pathlib

    if fmt not in ['.eps', '.png', '.pdf']:
        raise ValueError('unsupported format: %s' % (fmt,))

    extension = fmt
    if not file_name.suffix == extension:
        file_name = file_name.with_suffix(extension)

    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_name = tmp_file.name + extension

    # save figure
    if tight:
        fig.savefig(tmp_name, dpi=dpi, bbox_inches='tight')
    else:
        fig.savefig(tmp_name, dpi=dpi)

    # trim it
    if fmt == '.eps':
        subprocess.call('epstool --bbox --copy %s %s' %
                        (tmp_name, fspath(file_name)), shell=True)
    elif fmt == '.png':
        subprocess.call(
            'convert {} -trim {}'.format(tmp_name, fspath(file_name)),
            shell=True
        )
    elif fmt == '.pdf':
        subprocess.call(
            'pdfcrop {} {}'.format(tmp_name, fspath(file_name)),
            shell=True
        )


def args_to_str(args, skip=None):
    """
    transform an argparse object into a string for the purposes of naming in a
    reproducible way. Can be given a list of 'skipped' terms, which will be
    ignored (e.g. whether to save files is irrelevant if they're being saved).

    """
    skip = [] if skip is None else skip
    def abrev_list(s):
        if isinstance(s, list):
            return '-'.join(map(str,s))
        else:
            return str(s)
    argstr = '_'.join([
        ''.join([
            str(arg), abrev_list(getattr(args, arg))
        ]) for arg in vars(args) if str(arg) not in skip
    ])
    return argstr


def plot_or_save(dir, args, fname, fig=None):
    """
    show plots live, or save plots to file
     Used in in an experiment run where `args.save` is present. Automatically
     names files using `args_to_str`.
    REQUIRES `logging`be defined!
    """
    if fig is None:
        fig = plt.gcf()
    if args.save:
        argstr = args_to_str(args)
        fpath = (dir/'_'.join([fname, argstr])).with_suffix('.pdf')
        save_fig(fig, fpath)
        logging.info(f'saving file: {fpath}')
    else:
        plt.show(block=False)
        logging.info(f'displaying plot: {fname}')