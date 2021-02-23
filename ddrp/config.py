from typing import List, Dict, Union, Optional
import yaml
from dataclasses import dataclass
from dacite import from_dict
from pathlib import Path


@dataclass
class Paper:
    git_url: Optional[str]
    folder: str
    column_width: float
    text_width: float
    text_height: float


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
        config_dict = yaml.safe_load(fp)
    return from_dict(data_class=DDRPConfig, data=config_dict)
