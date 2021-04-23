---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.7.1
  kernelspec:
    display_name: Python [conda env:ddrp]
    language: python
    name: conda-env-ddrp-py
---

```python
from pydantic import BaseModel,DirectoryPath, PositiveInt
from hypothesis import given,strategies as st
from pathlib import Path
from ddrp.config import *
```

```python
norm_distance_to_in('10 cm')
```

```python
Paper(pubtype='talk',folder='.', height=10.,width="300 cm", columns=1)
```

```python
PaperColumns.single == 1

```

```python
from pint import definitions
```

```python
@given(st.sampled_from(PaperColumns))
def paper_columns(inst):
    print(inst)
    pass

@given(st.builds(FigureSettings))
def fig_settings(inst):
    print(inst)
    pass
```

```python
fig_settings()
```

```python
from srsly import read_yaml
from pprint import pprint
cfg_raw = read_yaml(Path('ddrp.yaml'))
pprint(cfg_raw)
DDRPRegistry.parse_obj(cfg_raw).dict()
# Publications.parse_file(Path('ddrp.yaml'))
```

```python
validator
```
