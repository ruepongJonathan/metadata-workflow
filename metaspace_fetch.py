import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import numpy as np

from metaspace import SMInstance


#Class object for fetching metaspace datasets
class metaspaceFetch():
    
    def __init__(self, pathName="./data/"):
        self.__SM = self.setup_connection()
        self.__pathName = pathName
        
        
    def setup_connection(self):
        '''
        This functions returns an instance of SMInstance().
        This object is used to connect to the Metaspace website
        '''
        return SMInstance()



    def search_metaspace(self,
                         keyword = None,
                         datasetID = [],
                         submitter_ID = None,
                         group_ID = None,
                         project_ID = None,
                         polarity = None,
                         ionisation_Source = None,
                         analyzer_Type = None,
                         maldi_Matrix = None,
                         organism = None): 
        '''
        Description
        ----------
        This calls the datasets function from the Metaspace package to return 
        a list of available datasets on Metaspace with the given parameters.
        
        Parameters
        ----------
        keyword : string, optional
            Search by key word on METASPACE, which is by name. 
            The default is None.
        datasetID : A list object, optional
            Given a list of dataset IDs, it will search METASPACE by ID. 
            The default is [].
        submitter_ID : string, optional
            Search datasets by submitter ID. 
            The default is None.
        group_ID : string, optional
            Search datasets by group ID. 
            The default is None.
        project_ID : string, optional
            Search datasets by project ID. 
            The default is None.
        polarity : string literal, optional
            Search datasets by polarity by using "POSITIVE" or "NEGATIVE". 
            The default is None.
        ionisation_Source : string, optional
            Search datasets by ionisation source. 
            The default is None.
        analyzer_Type : string, optional
            Search datasets by analyzer. 
            The default is None.
        maldi_Matrix : string, optional
            Search datasets by the maldi matrix. 
            The default is None.
        organism : string, optional
            Search datasets by organism. 
            The default is None.
    
        Returns
        -------
        A list of SMObjects which each object is a dataset on METSPACE.
    
        '''
        
        #makes a function call to make_dataframe to make a dataframe based on the list that 
        #is returned from datasets function
        temp_List =  self.__SM.datasets(nameMask=(keyword),
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
        return temp_List
        #return self.make_dataframe(temp_List)
        
    

    def make_dataframe(self, list_of_datasets): 
        '''
        Description
        ----------
        This function makes a daaframe from a list of SMObjects/datasets.
        
        Parameters
        ----------
        list_of_datasets : list()
            A list of SMObjects/datasets are required to make the dataframe.

        Returns
        -------
        dataframe
            A dataframe which contains information the datasets given from 
            the list.

        '''        
        #if the list_of_datasets is not emtpy, then run
        if (list_of_datasets):
            column_List = ["Name", "ID", "Submitter", "Group",
                           "Analyzer", "Metadata Type", "Ionisation Source",
                           "Organism", "Organism Part", "Adducts","Condition",
                           "Maldi Matrix","Growth Conditions","Polarity",
                           "Resolving Power","Pixel Size","MZ Value",
                           "MALDI Matrix Application","Sample Stabilisation",
                           "Solvent","Tissue Modification",
                           "Additional Information","SMDataset Object"]
            
            return pd.concat([pd.DataFrame([[
                                         self.get_dataset_name(dataset),
                                         self.get_dataset_id(dataset),
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
                                         self.get_dataset_additionalinfo(dataset),
                                         dataset]],
                                         columns= column_List) for dataset in list_of_datasets],
                                         ignore_index=True)
            
        #If the list_of_datasets is empty, then return an empty dataframe
        else:
            return pd.DataFrame()
        

    #FIXME
    def filter_metadata(self,
                        df,
                        adducts = None,
                        analyzer = None,
                        condition = None,
                        groupID = None,
                        groupShortName = None,
                        growthConditions = None,
                        ionisationSource = None,
                        maldiMatrix = None,
                        metadataType = None,
                        organism = None,
                        organismPart = None,
                        polarity = None,
                        resolvingPower = None,
                        pixelSize_Xaxis = None,
                        pixelSize_Yaxis = None,
                        mzValue = None):
        '''
        Description
        ----------
        This function filters through a dataframe of SMObjects/datasets based 
        on the given parameters. Where each parameter takes in an argument of a list
        of keywords, or values to filter by. 

        Parameters
        ----------
        df : dataframe object
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
        resolvingPower : list, optional
            Given a list of keywords or values to filter by resolving power. 
            The default is None.
        pixelSize_Xaxis : list, optional
            Given a list of keywords or values to filter by pixel size (Xaxis). 
            The default is None.
        pixelSize_Yaxis : list, optional
            Given a list of keywords or values to filter by pixel size (Yaxis). 
            The default is None.
        mzValue : list, optional
            Given a list of keywords or values to filter by mz value. 
            The default is None.

        Returns
        -------
        dataframe
            A dataframe which contains information on datasets.
            This will be a new dataframe after filtering.

        '''
        
        
        curr_Datasets = df["SMDataset Object"]
        filtered_List = list()
        
        #filter to find matching datasets with the given list
        if(adducts):
            for dataset in curr_Datasets.items():
                list_of_Adducts = self.get_dataset_adducts(dataset[1])
                #Runs each adduct given to find a match
                #when found a match, it stops to prevent duplications
                for key in adducts:
                    if(list_of_Adducts.count(key) != 0):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break 
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
        
        if(groupID):
            #Work in progress
            pass
        
        if(groupShortName):
            #Work in progress
            pass
        
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
        
        #Filtering by organism is case sensitive.
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
            
        if(resolvingPower):
            for dataset in curr_Datasets.items():
                curr_ResolvingPower = self.get_dataset_resolvingpower(dataset[1])
                if(curr_ResolvingPower != "N/A"):
                    for key in resolvingPower:
                        key = float(key)
                        curr_ResolvingPower = float(curr_ResolvingPower)
                        if(key <= curr_ResolvingPower):
                            filtered_List.append(curr_Datasets[dataset[0]])
                            break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
        
        if(pixelSize_Yaxis):
            for dataset in curr_Datasets.items():
                for key in pixelSize_Yaxis:
                    pixelSize = self.get_dataset_pixelsize(dataset[1])
                    if(pixelSize == "N/A"):
                        break
                    elif(int(key) <= int(pixelSize["Yaxis"])):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()
            
        if(mzValue):
            for dataset in curr_Datasets.items():
                for key in mzValue:
                    mz = self.get_dataset_mzvalue(dataset[1])
                    if(mz == "N/A"):
                        break
                    elif(int(key) <= int(mz)):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        break
            curr_Datasets = pd.Series(data = filtered_List)
            filtered_List = list()

        return self.make_dataframe(curr_Datasets.tolist())
    
    
    
    def filter_by_molecule(self, df, molecule):
        '''
        Description
        ----------
        The function filters a dataframe of SMObject/datasets by molecules.

        Parameters
        ----------
        df : dataframe
            A dataframe of SMObjects/datasets to filter.
        molecule : list
            A list of molecule formulas to filter by.

        Returns
        -------
        dataframe
            A dataframe which contains information on datasets.
            This will be a new dataframe after filtering.

        '''
        curr_Datasets = df["SMDataset Object"]
        filtered_List = list()
        
        for dataset in curr_Datasets.items():
            annotations = self.get_dataset_annotation(dataset[1])
            results = self.get_dataset_results(dataset[1])
            
            for key in molecule:
                #Marker to signal is a match was found 
                #which stops the loop from searching any further
                stopMark = False
                for annotation in annotations:
                    if(re.search(pattern=key, string=annotation)):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        stopMark = True
                        break
                if(stopMark):
                    break
                
                for result in results:
                    if(re.search(pattern=key, string=result)):
                        filtered_List.append(curr_Datasets[dataset[0]])
                        stopMark = True
                        break
                if(stopMark):
                    break
            
                
        return self.make_dataframe(filtered_List)
        
    
    def get_dataset_annotation(self,dataset):
        '''
        Returns a list of all annotations from a given SMObject/dataset.
        '''
        databases = dataset.database_details
        annotations = list()
        
        for database in databases:
            database_Tuple = (database["name"],database["version"])
            annotationList = dataset.annotations(database = database_Tuple,fdr = 1.0)#FIXME
            
            temp_Str = str()
            for annotation in annotationList:
                temp_Str = temp_Str + annotation[0] + ":"
        
            annotations.append(temp_Str)
        
        return annotations
   
    def get_dataset_results(self,dataset):
        '''
        Returns a list of all results from a given SMObject/dataset.
        '''
        databases = dataset.database_details
        results = list()
        
        for database in databases:
            database_Tuple = (database["name"],database["version"])
            results_DF = dataset.results(database = database_Tuple, fdr = 1.0)#FIXME
            #If the DF is empty, return an empty list
            if(results_DF.empty):
                return list()
            results_DF = results_DF["ionFormula"].tolist()
            temp_Str = str()
            for result in results_DF:
                temp_Str = temp_Str + result + ":"
        
            results.append(temp_Str)
        
        return results
   
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
    
    def set_dir_pathname(self, pathName):
        self.__pathName = pathName
    
    
    def dataset_selection(self, df, selected_Datasets = [], df_Column = "Name"):
        #FIXME param: df_Column is set to default "Name"
        #allow for other ways to select data. This needs more logic.
        #should not print all with None
        #current only prints the name, does not download anything
        
        '''
        Description
        ----------
        This function takes in a dataframe of datasets from metaspace and
        downloads them based on a given list of names.
        (It does not download the dataset. It prints out the dataset for testing)
        
        Parameters
        ----------            
        selected_datasets : list, optional
            A list of selected datasets to download. 
            The default is an empty list object [].
    
        Returns
        -------
        None.
    
        '''    
        #Runs if the __dataset_DF is None, then print out "Dataframe is empty" 
        if (df.empty):
            print("Dataframe is emtpy")

        #Runs if the __dataset_DF is not None        
        else:
            #True when the list "selected_Datasets" is empty
            if not selected_Datasets:        
                downloadDatasets = df["SMDataset Object"]
                
                for dataset in downloadDatasets:
                    print(dataset.name)
                    
            #Runs when the list "selected_Datasets" is not emtpy    
            else:
                for dataset in selected_Datasets:
                    print(df.loc[df[df_Column] == dataset, df_Column])
  
    


    def create_dir(self, filename,pathname): #FIXME (return a none if the dir exists)
        '''
        Description:
            This function takes in a filename and pathname and creates a new
            directory if it does not exists
        Input:
            filename:the desired filename (string)
            pathname:the desired location/path to create the directory
        Output:
            a return value of the newly/exisiting path name to the directory
        '''
        path = os.path.join(pathname,filename)
        if not os.path.exists(path):
            os.mkdir(path)
            return path
        return path



    def download_dataset(self, dataset_object,path_to_dir): #FIXME (use the dataset name, not database)
        '''
        Description:
            This function takes in a dataset_object (SMDataset) and path_to_dir
            to download and setup the directory for that dataset on file
        Input:
                dataset_object: a SMDataset object that contains information on a 
                Metaspace dataset
                path_to_dir: a path to the desired Directory where the downloaded dataset
                will be in
        Output: None
        '''
        dataset_Name = dataset_object.name
        dir_path_name = self.create_dir(dataset_Name, path_to_dir)
        dataset_object.download_to_dir(dir_path_name)





    def get_download_links(self, dataset):
        '''
        Description
        ----------
        A function that returns download links from a specified dataset.
        
        Parameters
        ----------
        dataset : SMDataset object
            A object that contains a dataset from Metaspace.
    
        Returns
        -------
        A data structure
            Contains links to downloadthe dataset's files.
        '''
        return dataset.download_links()

