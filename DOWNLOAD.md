Please visit dataset [homepage](https://www.kaggle.com/datasets/nbroad/fluorescent-neuronal-cells) to download the data. 

Afterward, you have the option to download it in the universal supervisely format by utilizing the *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Fluorescent Neuronal Cells', dst_path='~/dtools/datasets/Fluorescent Neuronal Cells.tar')
```