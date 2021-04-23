from typing import Dict, Union, Optional

from srsly import read_yaml
from pydantic.dataclasses import dataclass
from pydantic import (
    BaseModel,
    BaseSettings,
    DirectoryPath,
    AnyHttpUrl,
    PositiveFloat,
    validator,
    constr,
)
from pathlib import Path
from enum import Enum, IntEnum
from pint import UnitRegistry

ureg = UnitRegistry()
Q = ureg.Quantity
Q_str = constr(regex="^[0-9]+.?[0-9]*\\s?[a-zA-Z_]+")
AcceptableDist = Union[PositiveFloat, Q_str, Q]


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
    axis_lw: PositiveFloat = 0.6
    plot_lw: PositiveFloat = 1.5
    font_family: str = "serif"


def norm_distance_to_in(d: AcceptableDist) -> PositiveFloat:
    def to_quantity_inch(d: AcceptableDist) -> Q:
        if isinstance(d, str):
            d = Q(d)
        else:
            d = Q(d, "inch")
        return d

    q = to_quantity_inch(d)
    assert q.magnitude > 0

    return q.to("in").magnitude


class Publication(BaseSettings):
    pubtype: PubType
    folder: DirectoryPath
    height: PositiveFloat
    width: PositiveFloat
    git_url: Optional[AnyHttpUrl]
    fig_settings: Optional[FigureSettings]

    _norm_dim_to_inch = validator(
        "height", "width", pre=True, always=True, allow_reuse=True
    )(norm_distance_to_in)


class Paper(Publication):
    pubtype: PubType = PubType.paper
    columns: PaperColumns = PaperColumns.single
    column_width: PositiveFloat = None

    @validator("pubtype", pre=True, always=True)
    def coerce_pubtype(cls, typ):
        return PubType.paper

    @validator("column_width", pre=True, always=True)
    def col_leq_width(cls, colw, values):
        if colw == None and values["columns"] == 1:
            colw = values["width"]
        elif colw == None:
            raise TypeError("Must pass column width for 2-column papers!")
        colw = norm_distance_to_in(colw)
        assert colw <= values["width"], "column width must be strictly less than width"
        return colw


class Publications(BaseModel):
    __root__: Dict[str, Union[Paper, Publication]]
    # TODO: Discover w/ plugin system
    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        if isinstance(item, int):
            item = list(self.__root__.keys())[item]
        return self.__root__[item]


class DDRPRegistry(BaseModel):
    papers: Publications
    fig_settings: Optional[FigureSettings] = FigureSettings()


def config_context() -> DDRPRegistry:

    yml_loc = Path("ddrp.yml")
    config_dict = read_yaml(yml_loc)
    return DDRPRegistry.parse_obj(config_dict)
