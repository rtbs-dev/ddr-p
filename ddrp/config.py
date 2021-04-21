from typing import List, Dict, Union, Optional
from srsly import read_yaml
from pydantic.dataclasses import dataclass
from pydantic import BaseModel, BaseSettings, DirectoryPath, AnyHttpUrl
from dataclasses import field, InitVar
from dacite import from_dict, Config
from pathlib import Path
from enum import Enum, IntEnum


class PubType(str, Enum):
    paper = "paper"
    talk = "talk"
    poster = "poster"


class PaperColumns(IntEnum):
    single = 1
    double = 2


@dataclass
class FigureSettings:
    dpi: int = 200
    label_size: int = 8
    font_size: int = 8
    ticks_size: int = 6
    axis_lw: float = 0.6
    plot_lw: float = 1.5
    font_family: str = "serif"


@dataclass
class Publication:
    pubtype: PubType
    folder: DirectoryPath
    git_url: Optional[AnyHttpUrl]
    fig_settings: Optional[FigureSettings]


@dataclass
class Paper(Publication):
    columns: PaperColumns
    column_width_pt: InitVar[float]
    text_width_pt: InitVar[float]
    text_height_pt: InitVar[float]
    column_width: float = field(init=False)
    text_width: float = field(init=False)
    text_height: float = field(init=False)

    def __post_init__(self, column_width_pt, text_width_pt, text_height_pt):
        """need to turn pts to inches"""
        self.column_width = column_width_pt / 72.47
        self.text_width = text_width_pt / 72.47
        self.text_height = text_height_pt / 72.47


class Publications(BaseModel):
    __root__: Dict[str, Publication]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class DDRPConfig(BaseSettings):
    papers: Publications
    fig_settingr: Optional[FigureSettings] = FigureSettings()


def config_context(dacite_config: Optional[Config] = None) -> DDRPConfig:
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
    config_dict = read_yaml(yml_loc)
    return from_dict(data_class=DDRPConfig, data=config_dict, config=dacite_config)
