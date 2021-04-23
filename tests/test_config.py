from hypothesis import given, assume, strategies as st
from ddrp.config import *


@given(st.builds(FigureSettings))
def test_fig_dimensions(instance: FigureSettings):
    print(instance.__pydantic_model__.schema())
    assert 0 < instance.axis_lw
    assert 0 < instance.plot_lw


# @given(st.strings)
# @given(st.builds(Publication))
# def test_pub_dim(inst: Publication):
#     print(inst.schema())
#     pass


# @given(st.builds(Paper, column_width=None))
# def test_default_columns(p: Paper):
#     # assume(p.column_width_pt <= p.text_width_pt)
#     print(Paper.schema())
#     # assert(p.column_width)
#     assert p.column_width == p.text_width
