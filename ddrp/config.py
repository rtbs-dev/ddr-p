from typing import List, Dict, Union, Optional
from srsly import read_yaml
from dataclasses import dataclass, field
from dacite import from_dict
from pathlib import Path


@dataclass
class Paper:
    git_url: Optional[str]
    folder: str
    columns: int
    column_width_pt: float
    text_width_pt: float
    text_height_pt: float
    column_width: float = field(init=False)
    text_width: float = field(init=False)
    text_height: float = field(init=False)
    dpi: int = 200

    def __post_init__(self):
        """need to turn pts to inches"""
        self.column_width = self.column_width_pt / 72.47
        self.text_with = self.text_width_pt / 72.47
        self.text_height = self.text_height_pt / 72.47


@dataclass
class Figure:
    label_size: int = 8
    font_size: int = 8
    ticks_size: int = 6
    axis_lw: float = 0.6
    plot_lw: float = 1.5


@dataclass
class DDRPConfig:
    papers: List[Paper]
    figure_setup: Figure


def config_context(type_hooks: Optional[Dict] = None) -> DDRPConfig:
    """
    Retrieve a structured representation of the current ddrp.yml config.

    Parameters
    ----------
    type_hooks : dict
        type -> callable mappings, instrtucting the constructor to apply the
        passed function to all data of that type. e.g. {str: str.lower}

    Returns
    -------
    DDRPConfig, a dataclass containing structured type-checked config options.
    """
    yml_loc = Path("ddrp.yml")
    with yml_loc.open() as fp:
        config_dict = read_yaml(fp)
    return from_dict(data_class=DDRPConfig, data=config_dict, type_hooks=type_hooks)
