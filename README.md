# metasdata-workflow
This package connects to the METASPACE server using the metaspace2020 api and allows for searching, filtering, and downloading metadata on METASPACE.

## Gettting Started

```python
import metaspcae_fetch as mf
#from metadata_workflow import metaspace_fetch as mf

#returns all avalable datasets on METASPACE
datasets = mf.metaspaceFetch()
```


## Installation

The code can be installed from GitHub with:

```shell
$ pip install git+https://github.com/ruepongJonathan/metadata-workflow.git
```

The code can be installed in development mode with:

```shell
$ git clone https://github.com/ruepongJonathan/metadata-workflow.git
$ cd metadata-workflow
$ pip install --editable .
```
Where `--editable` means the coe is symlinked into your environment's site-packages directory




