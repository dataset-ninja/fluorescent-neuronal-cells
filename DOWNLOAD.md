Dataset **Fluorescent Neuronal Cells** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/r/6/sl/cahW4f2E0om1e5qxhbTy1gp3TjWLyVmDXeDGz84DfObhX8UBC7wLTvegoebPLv4D5FJPSlXj2OPHYPjoaSiOfdlHuNtnlQozFOFRFxbD8wfPh070nMTW372z7nBO.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Fluorescent Neuronal Cells', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/nbroad/fluorescent-neuronal-cells/download?datasetVersionNumber=26)