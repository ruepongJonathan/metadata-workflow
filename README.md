# metasdata-workflow
This package connects to the METASPACE server using the metaspace2020 api and allows for searching, filtering, and downloading metadata on METASPACE.

## Getting Started

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
should go. By default it will make a new folder local to where the package. The folder will be called
"data"

### Step two: search METASPACE
```python
import metaspace_fetch as mf

ms = mf.metaspaceFetch()

#call the search_metaspace() function to search datasets by the given arguments
#ex: search datasets with keyword brain and is a Homo sapiens (human)
datasets = ms.search_metaspace(keyword = "brain", organism = "Homo sapiens (human)
")
```
`search_metaspace()` searches on METASPACE and returns a list of datasets that match the 
arguments given to it. These datasets are represented by SMDataset objects. Each object
contains information on a dataset in METASPACE. There are several paramters where 
each one is a filter METASPACE uses to search for matching datasets. 

Note: Go to the METASPACE website and see what values can be inputed to the parameters/filters
used with this function. Also when using keyword, replace spaces with "_" as dataset names does not 
support spaces.

paramters/filters include:

* **keyword**: Search datasets by keyword (based on dataset's name)
* **datasetID**: Search datasets by dataset id (takes in a list of ids)
* **submitter_ID**: Search datasets by submitter id
* **group_ID**: Search datasets by group id
* **project_ID**: Search datasets by project id
* **polarity**: Search datasets by polarity (must be "POSITIVE" or "NEGATIVE")
* **ionisation_Source**: Search datasets by the ionisation source
* **analyzer_Type**: Search datasets by the analyzer type
* **maldi_Matrix**: Search datasets by maldi matrix
* **organism**: Search datasets by organism

### Step three: make dataframe
```python
import metaspace_fetch as mf

ms = mf.metaspaceFetch()

datasets = ms.search_metaspace(keyword = "brain", organism = "Homo sapiens (human)")

#call make_dataframe() to make a dataframe which includes information on each dataset
#provided by the given list
dataframe = ms.make_dataframe(datasets)
```
`make_dataframe()` takes a list of dataset objects (SMDataset) and produces a dataframe
which includes information on those datasets. It is organized so that each column represents
information like "name", "id", "organism", etc.

included information by default:
* Name
* ID
* SMDataset object
* Submitter (dict)
* Group (dict)
* Analyzer
* Metadata Type
* Ionisation Source
* Organism 
* Organism Part 
* Adducts (list)
* Condition 
* Maldi Matrix 
* Growth Condition 
* Polarity 
* Resolving Power 
* Pixel Size 
* Mz Value 
* Maldi Matrix Application 
* Sample Stabilisation 
* Solvent 
* Tissue Modification 
* Additional Information (dict)

### Step four: filtering/annotations
```python
import metaspace_fetch as mf

ms = mf.metaspaceFetch()

datasets = ms.search_metaspace(keyword = "brain", organism = "Homo sapiens (human)")

dataframe = ms.make_dataframe(datasets)

#call the filter_metadata() function to filter through a dataframe of datasets
dataframe = ms.filter_metadata(df = dataframe,
                               maldiMatrix=["BPYN"],
                               polarity=["NEGATIVE"])
```

`filter_metadata()` takes a dataframe of datasets and filters through it. It will
return a new dataframe after filtering. It requires a dataframe to filter. Each parameter 
is a filter which takes in a list of keys or values to filter with.

filter/parameters:
* adducts 
* analyzer 
* condition 
* groupID 
* groupName 
* groupShortName 
* growthCondition
* ionisationSource 
* maldiMatrix 
* metadataType
* organism 
* organismPart 
* polarity 
* lessOrEq_ResolvingPower
* lessOrEq_PixelSize_Xaxis
* lessOrEq_PixelSize_Yaxis
* lessOrEq_mzValue

`filter_molecule()` filters the dataframe by molecules. These molcules are annotations on METASPACE. The function
takes in a list of keys or values to filter by. Molecules must be represented by its ion formula. The function adds in a new
column called "Molecules" if the given dataframe does not have it. `annotate()` is called to include 
the new column "Molecules" which can be called before `filter_molecule()`. The column is a list dataframes
which contains annotations/results of the molecules detected in the dataset.

```python
import metaspace_fetch as mf

ms = mf.metaspaceFetch()

datasets = ms.search_metaspace(keyword = "brain", organism = "Homo sapiens (human)")

dataframe = ms.make_dataframe(datasets)

dataframe = ms.filter_metadata(df = dataframe,
                               maldiMatrix=["BPYN"],
                               polarity=["NEGATIVE"])

#adds in a new column "Molecules"
dataframe = ms.annotate(dataframe)

#filters dataframe by datasets which detected "C24H45O7P"
dataframe = ms.filter_molecule(dataframe, molecules=["C24H45O7P"])
```

### Step five: downloading metadata
```python
import metaspace_fetch as mf

ms = mf.metaspaceFetch()

datasets = ms.search_metaspace(keyword = "brain", organism = "Homo sapiens (human)")

dataframe = ms.make_dataframe(datasets)

dataframe = ms.filter_metadata(df = dataframe,
                               maldiMatrix=["BPYN"],
                               polarity=["NEGATIVE"])

dataframe = ms.annotate(dataframe)

dataframe = ms.filter_molecule(dataframe, molecules=["C24H45O7P"])

#a list datasets to download (by name)
to_Download = ["Some name", "Other name"]

#downloads the datasets
ms.dataset_selection(dataframe, selected_Datasets=to_Download, df_Column="Name", download_All=False)
```

`dataset_selection()` downloads datasets based on a given list.
Note: The function currently only prints out the dataset object. Does not download anything.

parameters:
* df: the dataframe of datasets
* selected_Datasets: a list of datasets to download 
* df_Column: the column to select the datasets from (defaults to the "Name" column)
* download_All: set to True to download all datasets present in the given dataframe

`dataset_selection()` downloads and stores the datasets to a default directory which can be specified
by using `set_download_pathname()`. Use `get_download_pathname()` to show the current path to the directory where the downloaded
datasets will be stored.

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
Where `--editable` means the code is symlinked into your environment's site-packages directory

## License

This code is licensed under MIT License.


