'''This package connects to the METASPACE website and establishes a workflow for searching, filtering, and downloading mass spectrometry imaging metadata.'''

import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import numpy as np
from metaspace import SMInstance


class metaspaceFetch():
    
    def __init__(self, downloadPathName: str ="./data/"):
        '''
        Setup metaspaceFetch class

        Parameters
        ----------
        downloadPathName : str, optional
            The path name where downloaded datasets are located. 
            The default is "./data/".

        Returns
        -------
        None.

        '''
        self.__SM = self.setup_connection()
        self.__downloadPathName = downloadPathName
        
        
    def setup_connection(self):
        '''
        Setup connection to METASPACE server using METASPACE API

        Returns
        -------
        SMInstance : Class object for communication with METASPACE
            The object is used to connect and communicate witht the
            METASPACE server.

        '''
        return SMInstance()



    def search_metaspace(self,
                         keyword: str = None,
                         datasetID: list = [],
                         submitter_ID: str = None,
                         group_ID: str = None,
                         project_ID: str = None,
                         polarity: str = None,
                         ionisation_Source: str = None,
                         analyzer_Type: str = None,
                         maldi_Matrix: str = None,
                         organism: str = None): 
        '''
        Call METASPACE API function "datasets", search METASPACE website by the 
        given arguments, return searched datasets as a list.
        
        Parameters
        ----------
        keyword : str, optional
            Search by key word on METASPACE, which is by name. 
            The default is None.
        datasetID : list, optional
            Given a list of dataset IDs, it will search METASPACE by ID. 
            The default is [].
        submitter_ID : str, optional
            Search datasets by submitter ID. 
            The default is None.
        group_ID : str, optional
            Search datasets by group ID. 
            The default is None.
        project_ID : str, optional
            Search datasets by project ID. 
            The default is None.
        polarity : str[Polarity] , optional
            Search datasets by polarity by using "POSITIVE" or "NEGATIVE". 
            The default is None.
        ionisation_Source : str, optional
            Search datasets by ionisation source. 
            The default is None.
        analyzer_Type : str, optional
            Search datasets by analyzer. 
            The default is None.
        maldi_Matrix : str, optional
            Search datasets by the maldi matrix. 
            The default is None.
        organism : str, optional
            Search datasets by organism. 
            The default is None.
    
        Returns
        -------
        dataset_List : List
            A list of SMObjects which each object is a dataset on 
            METSPACE.
        '''
        
        dataset_List =  self.__SM.datasets(nameMask=(keyword),
                                 idMask=(datasetID),
                                 submitter_id=(submitter_ID), 
                                 group_id=(group_ID),
                                 project_id=(project_ID), 
                                 polarity=(polarity),
                                 ionisation_source=(ionisation_Source),
                                 analyzer_type=(analyzer_Type),
                                 maldi_matrix=(maldi_Matrix),
                                 organism=(organism))
        
        #returns a list of datasets
        return dataset_List
       
    

    def make_dataframe(self, list_of_datasets: list): 
        '''
        Make a dataframe of a list of SMObjects/datasets.
        
        Parameters
        ----------
        list_of_datasets : list
            A list of SMObjects/datasets are required to make the dataframe.

        Returns
        -------
        dataframe: pd.DataFrame()
            A dataframe which contains information of the datasets given from 
            the list.

        '''        
        #if the list_of_datasets is not emtpy, then run
        if (list_of_datasets):
            column_List = ["Name","ID","SMDataset Object","Submitter","Group",
                           "Analyzer","Metadata Type","Ionisation Source",
                           "Organism","Organism Part","Adducts","Condition",
                           "Maldi Matrix","Growth Conditions","Polarity",
                           "Resolving Power","Pixel Size","MZ Value",
                           "MALDI Matrix Application","Sample Stabilisation",
                           "Solvent","Tissue Modification",
                           "Additional Information"]
            
            return pd.concat([pd.DataFrame([[
                                         self.get_dataset_name(dataset),
                                         self.get_dataset_id(dataset),
                                         dataset,
                                         self.get_dataset_submitter(dataset),
                                         self.get_dataset_group(dataset),
                                         self.get_dataset_analyzer(dataset),
                                         self.get_dataset_metadatatype(dataset),
                                         self.get_dataset_ionisationsource(dataset),
                                         self.get_dataset_organism(dataset),
                                         self.get_dataset_organismpart(dataset),
                                         self.get_dataset_adducts(dataset),
                                         self.get_dataset_condition(dataset),
                                         self.get_dataset_maldimatrix(dataset),
                                         self.get_dataset_growthconditions(dataset),
                                         self.get_dataset_polarity(dataset),
                                         self.get_dataset_resolvingpower(dataset),
                                         self.get_dataset_pixelsize(dataset),
                                         self.get_dataset_mzvalue(dataset),
                                         self.get_dataset_maldimatrixapp(dataset),
                                         self.get_dataset_sample_stabilisation(dataset),
                                         self.get_dataset_solvent(dataset),
                                         self.get_dataset_tissue_modification(dataset),
                                         self.get_dataset_additionalinfo(dataset)
                                         ]],
                                         columns= column_List) for dataset in list_of_datasets],
                                         ignore_index=True)
            
        #If the list_of_datasets is empty, then return an empty dataframe
        else:
            return pd.DataFrame()
        

    def filter_metadata(self,
                        df: pd.DataFrame(),
                        adducts: list = None,
                        analyzer: list = None,
                        condition: list = None,
                        groupID: list = None,
                        groupName: list = None,
                        groupShortName: list = None,
                        growthConditions: list = None,
                        ionisationSource: list = None,
                        maldiMatrix: list = None,
                        metadataType: list = None,
                        organism: list = None,
                        organismPart: list = None,
                        polarity: list = None,
                        lessOrEq_ResolvingPower: list = None,
                        lessOrEq_PixelSize_Xaxis: list = None,
                        lessOrEq_PixelSize_Yaxis: list = None,
                        lessOrEq_mzValue: list = None):
        
        '''
        Filter through a dataframe of datasets by the give arguments

        Parameters
        ----------
        df : pd.DataFrame()
            A dataframe of SMObjects/datasets to filter.
        adducts : list, optional
            Give a list of keywords or values to filter by adducts. 
            The default is None.
        analyzer : list, optional
            Give a list of keywords or values to filter by analyzer. 
            The default is None.
        condition : list, optional
            Give a list of keywords or values to filter by condition. 
            The default is None.
        groupID : list, optional
            Give a list of keywords or values to filter by group ID. 
            The default is None.
        groupName : list, optional
            Give a list of keywords or values to filter by group name.
            The default is None
        groupShortName : list, optional
            Give a list of keywords or values to filter by group short name. 
            The default is None.
        growthConditions : list, optional
            Given a list of keywords or values to filter by growth condition. 
            The default is None.
        ionisationSource : list, optional
            Given a list of keywords or values to filter by ionisation source. 
            The default is None.
        maldiMatrix : list, optional
            Given a list of keywords or values to filter by MALDI matrix. 
            The default is None.
        metadataType : list, optional
            Given a list of keywords or values to filter by metadata type. 
            The default is None.
        organism : list, optional
            Given a list of keywords or values to filter by organism. 
            The default is None.
        organismPart : list, optional
            Given a list of keywords or values to filter by organism part. 
            The default is None.
        polarity : list, optional
            Given a list of keywords or values to filter by polarity. 
            The default is None.
        lessOrEq_ResolvingPower : list, optional
            Given a list of keywords or values to filter by resolving power.
            The given value (or key) must be <= to a datasets resolving power. 
            The default is None.
        lessOrEq_PixelSize_Xaxis : list, optional
            Given a list of keywords or values to filter by pixel size (Xaxis).
            The given value (or key) must be <= to a datasets pixel size (Xaxis).
            The default is None.
        lessOrEq_PixelSize_Yaxis : list, optional
            Given a list of keywords or values to filter by pixel size (Yaxis).
            The given value (or key) must be <= to a datasets pixel size (Yaxis).
            The default is None.
        lessOrEq_mzValue : list, optional
            Given a list of keywords or values to filter by mz value.
            The given value (or key) must be <= to a datasets mz value.
            The default is None.

        Returns
        -------
        pd.DataFrame()
            A dataframe which contains information on datasets.
            This will be a new dataframe after filtering.

        '''
        
        #a series of datasets
        curr_Datasets = df["SMDataset Object"]
        
        #a list for matched datasets, 
        filtered_List = list()
        
        #runs a if branch if the corresponding parameter was given a list as an argument
        if(adducts):
            #Goes through each dataset from the given dataframe
            for dataset in curr_Datasets.items():
                list_of_Adducts = self.get_dataset_adducts(dataset[1])
                #Goes through each element/key of the given list to find a match
                #when a match is found it stops to prevent duplications
                for key in adducts:
                    if(list_of_Adducts.count(key) != 0):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            #replaces curr_Datasets series with the new list of matched datasets        
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(analyzer):
            for dataset in curr_Datasets.items():
                for key in analyzer:
                    if(key == self.get_dataset_analyzer(dataset[1])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break   
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(condition):
            for dataset in curr_Datasets.items():
                for key in condition:
                    if(key == self.get_dataset_condition(dataset[1])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(groupName):
            for dataset in curr_Datasets.items():
                curr_Group = self.get_dataset_group(dataset[1])
                if((curr_Group != "N/A") and (curr_Group != None)):
                    for key in groupName:
                        if(key == curr_Group.get("name", "N/A")):
                            filtered_List.append(curr_Datasets[dataset[0]])
                            break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(groupID):
            for dataset in curr_Datasets.items():
                curr_Group = self.get_dataset_group(dataset[1])
                if((curr_Group != "N/A") and (curr_Group != None)):
                    for key in groupID:
                        if(key == curr_Group.get("id", "N/A")):
                            filtered_List.append(curr_Datasets[dataset[0]])
                            break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(groupShortName):
            for dataset in curr_Datasets.items():
                curr_Group = self.get_dataset_group(dataset[1])
                if((curr_Group != "N/A") and (curr_Group != None)):
                    for key in groupShortName:
                        if(key == curr_Group.get("shortName", "N/A")):
                            filtered_List.append(curr_Datasets[dataset[0]])
                            break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(growthConditions):
            for dataset in curr_Datasets.items():
                for key in growthConditions:
                    if(key == self.get_dataset_growthconditions(dataset[1])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if (ionisationSource):
            for dataset in curr_Datasets.items():
                for key in ionisationSource:
                    if(key == self.get_dataset_ionisationsource(dataset[1])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(maldiMatrix):
            for dataset in curr_Datasets.items():
                for key in maldiMatrix:
                    sequence = self.get_dataset_maldimatrix(dataset[1])
                    pattern = key
                    if(re.search(pattern,sequence)):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(metadataType):
            for dataset in curr_Datasets.items():
                for key in metadataType:
                    if(key == self.get_dataset_metadatatype(dataset[1])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        #Filtering my organism is case sensitive. 
        #Ex: mouse will match with mouse, but "Mouse" will not match with mouse
        if(organism):
            for dataset in curr_Datasets.items():
                for key in organism:
                    if(key == self.get_dataset_organism(dataset[1])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        #Filtering by organism part is case sensitive.
        #Ex: skin will match skin, but "Skin" will not match skin
        if(organismPart):
            for dataset in curr_Datasets.items():
                for  key in organismPart:
                    if(key == self.get_dataset_organismpart(dataset[1])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
            
        if(polarity):
            for dataset in curr_Datasets.items():
                for key in polarity:
                    if(key.upper() == self.get_dataset_polarity(dataset[1]).upper()):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        #finds a match if key <= to a datasets resolving power
        if(lessOrEq_ResolvingPower):
            for dataset in curr_Datasets.items():
                curr_ResolvingPower = self.get_dataset_resolvingpower(dataset[1])
                if(curr_ResolvingPower != "N/A"):
                    for key in lessOrEq_ResolvingPower:
                        key = float(key)
                        curr_ResolvingPower = float(curr_ResolvingPower)
                        if(key <= curr_ResolvingPower):
                            filtered_List.append(curr_Datasets[dataset[0]])
                            break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        #finds a match if key <= to a datasets pixel size (Xaxis)
        if(lessOrEq_PixelSize_Xaxis):
            for dataset in curr_Datasets.items():
                for key in lessOrEq_PixelSize_Xaxis:
                    pixelSize = self.get_dataset_pixelsize(dataset[1])
                    if(pixelSize == "N/A"):
                        break
                    elif(int(key) <= int(pixelSize["Xaxis"])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        #finds a match if key <= to a datasets pixel size (Yaxis)
        if(lessOrEq_PixelSize_Yaxis):
            for dataset in curr_Datasets.items():
                for key in lessOrEq_PixelSize_Yaxis:
                    pixelSize = self.get_dataset_pixelsize(dataset[1])
                    if(pixelSize == "N/A"):
                        break
                    elif(int(key) <= int(pixelSize["Yaxis"])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        #finds a match if key <= to a datasets mz value
        if(lessOrEq_mzValue):
            for dataset in curr_Datasets.items():
                for key in lessOrEq_mzValue:
                    mz = self.get_dataset_mzvalue(dataset[1])
                    if(mz == "N/A"):
                        break
                    elif(int(key) <= int(mz)):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()

        return self.make_dataframe(curr_Datasets.tolist())
     
    def filter_molecule(self, df: pd.DataFrame(), molecules: list):
        '''
        Filter dataframe of metadata by molecule.

        Parameters
        ----------
        df : pd.DataFrame()
            A dataframe of SMObjects/datasets to filter.
        molecules : list
            Given a list of keywords or values to filter by molecule.

        Returns
        -------
        pd.DataFrame()
            A dataframe which contains information on datasets.
            This will be a new dataframe after filtering.

        '''
        
        #checks to see if the dataframe has a "Molecules" column
        #if not then it creates one by calling annotate()
        if "Molecules" not in df.columns:
            df = self.annotate(df)
        
        #becomes a series
        dataset_Annotations = df["Molecules"]
        
        #a list for matched datasets
        filtered_List = list()
        
        #goes through each dataset's annotations (which are dataframes) from the given dataframe
        for dataset in dataset_Annotations.items():
            #a dataset can have multple annotations
            #it goes through each annotation dataframe
            for annotation_DF in dataset[1]:
                #a marker to signal when a dataset matches with a key
                stopMark = False
                #if a annotation dataframe is empty then skip
                if(annotation_DF.empty):
                    continue
                #a series of ions/molecules
                curr_Mols = annotation_DF["ion"]
                for mol in curr_Mols.items():
                    for key in molecules:
                        #runs when it finds a match
                        if(re.search(pattern=key, string=mol[1])):
                            temp_Dataset = df.iloc[dataset[0]]
                            temp_Dataset = temp_Dataset["SMDataset Object"]
                            filtered_List.append(temp_Dataset)
                            stopMark = True
                            break
                    if(stopMark):
                        break   
                if(stopMark):
                    break
        #returns the an empty dataframe when no datasets were found
        if(len(filtered_List) == 0):
            return df
        #returns a new dataframe of matched datasets if some are found
        else:    
            return self.annotate((self.make_dataframe(filtered_List)))
                            
    def annotate(self,df: pd.DataFrame()):
        '''
        Add a new column for a dataset's annotations/results called "Molecules"
        Each element in "Molecules" is a list of annotations/results dataframes  

        Parameters
        ----------
        df : pd.DataFrame()
            A dataframe of SMObjects/datasets.

        Returns
        -------
        df : pd.DataFrame()
            A dataframe of SMObjects/datasets with a new column called "Molecules".

        '''
        
        #a series of datasets
        datasets = df["SMDataset Object"]
        
        #a list of annotations/results
        #which is a dataframe of detected molecules from that dataset
        resultsList = list()
        
        #goes through each dataset
        for dataset in datasets.items():
            databases = dataset[1].database_details
            #this keeps track of all the dataset's reults/annotations
            List = list()
            #a dataset can have multiple databases
            #it goes through each database and grabs its corresponding annotations/results
            for database in databases:
                databaseTuple= (database["name"],database["version"])
                tempResult = dataset[1].results(database=databaseTuple,fdr=1.0)
                #if the results/annotations return nothing then add an empty dataframe
                if(tempResult.empty):
                    List.append(pd.DataFrame())
                #if the results/annotations return something then add it
                else:
                    List.append(tempResult)
            resultsList.append(List)
            
        #makes a new column in the given dataframe called "Molecules"
        df["Molecules"] = resultsList
        
        return df   
 
    def get_download_links(self, dataset):
        '''
        returns a dictionary with information on the dataset and its download links

        Parameters
        ----------
        dataset : SMDataset object
            An object that represents a dataset on METASPACE.

        Returns
        -------
        dict
            A dictionary with information on the dataset and its download links.

        '''
        return dataset.download_links()
 
    def get_dataset_name(self, dataset):
        return dataset.name

    def get_dataset_id(self, dataset):
        return dataset.id
    
    def get_dataset_group(self, dataset):
        return dataset._info.get("group", "N/A")
    
    def get_dataset_submitter(self, dataset):
        return dataset._info.get("submitter", "N/A")
    
    def get_dataset_analyzer(self, dataset):
        return dataset._metadata["MS_Analysis"].get("Analyzer", "N/A")
    
    def get_dataset_condition(self, dataset):
        return dataset._info.get("condition", "N/A")
    
    def get_dataset_growthconditions(self, dataset):
        return dataset._info.get("growthConditions", "N/A")
    
    def get_dataset_ionisationsource(self, dataset):
        return dataset._info.get("ionisationSource", "N/A")
    
    def get_dataset_maldimatrix(self, dataset):
        return dataset._info.get("maldiMatrix", "N/A")
    
    def get_dataset_metadatatype(self, dataset):
        return dataset._info.get("metadataType", "N/A")
    
    def get_dataset_organism(self, dataset):
        return dataset._info.get("organism", "N/A")
    
    def get_dataset_organismpart(self, dataset):
        return dataset._info.get("organismPart", "N/A")
    
    def get_dataset_polarity(self, dataset):
        return dataset._info.get("polarity", "N/A")
    
    def get_dataset_resolvingpower(self, dataset):
        return dataset._info["analyzer"].get("resolvingPower", "N/A")
    
    def get_dataset_additionalinfo(self, dataset):
        return dataset._metadata.get("Additional_Information", "N/A")
    
    def get_dataset_pixelsize(self, dataset):
        return dataset._metadata["MS_Analysis"].get("Pixel_Size", "N/A")
    
    def get_dataset_adducts(self,dataset):
        return dataset.adducts
    
    def get_dataset_mzvalue(self, dataset):
        return dataset._metadata["MS_Analysis"]["Detector_Resolving_Power"].get("mz", "N/A")
    
    def get_dataset_maldimatrixapp(self, dataset):
        return dataset._metadata["Sample_Preparation"].get("MALDI_Matrix_Application", "N/A")
    
    def get_dataset_sample_stabilisation(self, dataset):
        return dataset._metadata["Sample_Preparation"].get("Sample_Stabilisation", "N/A")
    
    def get_dataset_solvent(self, dataset):
        return dataset._metadata["Sample_Preparation"].get("Solvent", "N/A")
    
    def get_dataset_tissue_modification(self, dataset):
        return dataset._metadata["Sample_Preparation"].get("Tissue_Modification", "N/A")
    
    
    def set_download_pathname(self, pathName):
        self.__downloadPathName = pathName
        
    def get_download_pathname(self):
        return self.__pathName
    
    #Currently does not download datasets, but prints the object
    def dataset_selection(self, df: pd.DataFrame(), selected_Datasets: list  = [], 
                          df_Column: str = "Name", download_All: bool = False):
        '''
        Download a list of selected datasets from a selected dataframe column, or download all.
        Currently does not download datasets, but prints the object.

        Parameters
        ----------
        df : pd.DataFrame()
            A dataframe of SMObjects/datasets.
        selected_Datasets : list, optional
            A list of selected datasets to download. The default is [].
        df_Column : str, optional
            A column to selecte the datasets from. The default is "Name".
        download_All : bool, optional
            Make "True" to download all datasets from the given dataframe. The default is False.

        Returns
        -------
        None.

        '''
        
        #runs if the given dataframe is empty 
        if (df.empty):
            print("Dataframe is emtpy")
            
        else:
            #when true it will download all datasets currently in the dataframe
            if(download_All):        
                downloadDatasets = df["SMDataset Object"]
                for dataset in downloadDatasets.items():
                    print(dataset[1])
                    #self.__download_dataset(dataset[1])
            #runs when download_All is false
            else:
                for dataset in selected_Datasets:
                    curr_DS = df.loc[df[df_Column] == dataset, "SMDataset Object"]
                    curr_DS = curr_DS.iloc[0]
                    print(curr_DS)
                    #self.__download_dataset(curr_DS)

    def __download_dataset(self, dataset):
        '''
        Download a given dataset, setup file name and directory

        Parameters
        ----------
        dataset : SMDataset object
            An object that represents a dataset on METASPACE.

        Returns
        -------
        None.

        '''
        
        dataset_Name = self.get_dataset_name(dataset)
        dir_path_name = self.create_dir(dataset_Name, self.__downloadPathName)
        dataset.download_to_dir(dir_path_name)

    


    def __create_dir(self, fileName: str, pathName: str):
        '''
        Make a directory to store downloaded dataset

        Parameters
        ----------
        fileName : str
            The directory name.
        pathName : str
            The path name to the directory.

        Returns
        -------
        path : str
            A path name to the directory. 

        '''
        
        #creates a path name with the file name and the path
        path = os.path.join(pathName,fileName)
        #if the path does not exist then make it
        if not os.path.exists(path):
            os.mkdir(path)
            return path
        return path