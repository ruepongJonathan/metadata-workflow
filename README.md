# metasdata-workflow
This package connects to the METASPACE server using the metaspace2020 api and allows for searching, filtering, and downloading metadata on METASPACE.

## Gettting Started

```python
import metaspace_fetch as mf
#from metadata_workflow import metaspace_fetch as mf
```
## Work flow

### Step one: importing and setting up connection to METASPACE
```python
import metaspace_fetch as mf

#this makes an instance of metaspaceFetch and sets up the connection to METASPACE
ms = mf.metaspaceFetch()
```
Give an argument to `downloadPathName` to specify where downloaded datasets
should go. By default it will make a new folder local to where the package is called 
"data"

### Step two: search METASPACE
```python
import metaspace_fetch as mf

ms = mf.metaspaceFetch()

#call the search_metaspace() function to search datasets by the given arguments
datasets = ms.search_metaspace(keyword = "brain", organism = "Homo sapiens (human)
")

print(datasets)
```
`search_metaspace()` searches on METASPACE and returns a list of datasets that match the 
arguments given to it. There are several paramters where each one is a filter METASPACE uses
to search for matching datasets.

### Step three: filter metadata
```python
```

### Step four: more filtering/annotations
```python
```

### Step five: downloading metadata
```python
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

## License

This code is licensed under MIT License.


