import math
import matplotlib.pyplot as plt
from os import fspath
import subprocess
import tempfile
import seaborn as sns

from .config import config_context


def figure_setup(papernum=0):
    """Set all the sizes to the correct values.
    TODO: use tex fonts for all texts, if installed
    """
    cfg = config_context().papers[papernum]
    figure_setup = cfg.fig_settings
    # This sets reasonable defaults for font size in a paper
    # sns.set_context("paper")
    # Set the font to be serif, rather than sans
    # sns.set(font="serif")
    # Make the background white, and specify the specific font family
    rcparams = {
        # "font.serif": ["Times", "Palatino", "serif"],
        "figure.dpi": figure_setup.dpi,
        "font.size": figure_setup.font_size,
        "figure.titlesize": figure_setup.font_size,
        "axes.titlesize": figure_setup.font_size,
        "legend.fontsize": figure_setup.font_size,
        "legend.fontsize": figure_setup.label_size,
        "axes.labelsize": figure_setup.label_size,
        "xtick.labelsize": figure_setup.ticks_size,
        "ytick.labelsize": figure_setup.ticks_size,
        "axes.linewidth": figure_setup.axis_lw,
    }

    sns.set_theme(
        context=cfg.pubtype,
        style="white",
        font=figure_setup.font_family,
        rc=rcparams,
    )


def figsize(fig_width=None, fig_height=None, papernum=0, aspect="phi"):
    """helper to define figsize based on columns
    If no height is given, it is computed using the golden ratio.
    """
    paper_config = config_context().papers[papernum]
    assert (aspect in ["phi", "square"]) or isinstance(aspect, float)

    ratios = {
        "phi": (1.0 + math.sqrt(5.0)) / 2.0,
        "square": 1.0,
    }
    if aspect in ["phi", "square"]:
        aspect = 1.0 / ratios[aspect] if paper_config.columns == 1 else ratios[aspect]
    elif isinstance(aspect, float):
        pass
    else:
        raise TypeError("`aspect` must be one of {'phi', 'square'} or `float`")

    if fig_width is None:
        if paper_config.columns == 2:
            fig_width = paper_config.column_width
        else:
            fig_width = paper_config.text_width
    if fig_width is "full":
        fig_width = paper_config.text_width
    if fig_width is "column":
        fig_width = paper_config.column_width
    if fig_height is None:
        fig_height = fig_width / aspect

    return fig_width, fig_height


def save_fig(fig, file_name, fmt=None, tight=True, papernum=0):
    """Save a Matplotlib figure as EPS/PNG/PDF to the given path and trim it."""
    cfg = config_context().papers[papernum]
    fig_cfg = cfg.fig_settings
    if not fmt:
        fmt = file_name.suffix  # pathlib

    if fmt not in [".eps", ".png", ".pdf"]:
        raise ValueError("unsupported format: %s" % (fmt,))

    extension = fmt
    if not file_name.suffix == extension:
        file_name = file_name.with_suffix(extension)

    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_name = tmp_file.name + extension

    # save figure
    if tight:
        fig.savefig(tmp_name, dpi=fig_cfg.dpi, bbox_inches="tight")
    else:
        fig.savefig(tmp_name, dpi=fig_cfg.dpi)

    # trim it
    if fmt == ".eps":
        subprocess.call(
            "epstool --bbox --copy %s %s" % (tmp_name, fspath(file_name)), shell=True
        )
    elif fmt == ".png":
        subprocess.call(
            "convert {} -trim {}".format(tmp_name, fspath(file_name)), shell=True
        )
    elif fmt == ".pdf":
        subprocess.call("pdfcrop {} {}".format(tmp_name, fspath(file_name)), shell=True)


def args_to_str(args, skip=None):
    """
    transform an argparse object into a string for the purposes of naming in a
    reproducible way. Can be given a list of 'skipped' terms, which will be
    ignored (e.g. whether to save files is irrelevant if they're being saved).

    """
    skip = [] if skip is None else skip

    def abrev_list(s):
        if isinstance(s, list):
            return "-".join(map(str, s))
        else:
            return str(s)

    argstr = "_".join(
        [
            "".join([str(arg), abrev_list(getattr(args, arg))])
            for arg in vars(args)
            if str(arg) not in skip
        ]
    )
    return argstr


def plot_or_save(dir, args, fname, fig=None):
    """
    show plots live, or save plots to file
     Used in in an experiment run where `args.save` is present. Automatically
     names files using `args_to_str`.
    REQUIRES `logging`be defined!
    """
    import logging

    if fig is None:
        fig = plt.gcf()
    if args.save:
        argstr = args_to_str(args)
        fpath = (dir / "_".join([fname, argstr])).with_suffix(".pdf")
        save_fig(fig, fpath)
        logging.info(f"saving file: {fpath}")
    else:
        plt.show(block=False)
        logging.info(f"displaying plot: {fname}")
