import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

from metaspace import SMInstance


#Class object for fetching metaspace datasets
class metaspaceFetch():
    
    def __init__(self):
        self.__dataset_DF = pd.DataFrame()
        self.__SM = self.setup_connection()
        
        
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
        The returned list will then be used to call the make_dataframe 
        function to make a dataframe out of the returned list of datasets.
        
        Parameters
        ----------
        keyword : TYPE, optional
            DESCRIPTION. The default is None.
        datasetID : TYPE, optional
            DESCRIPTION. The default is [].
        submitter_ID : TYPE, optional
            DESCRIPTION. The default is None.
        group_ID : TYPE, optional
            DESCRIPTION. The default is None.
        project_ID : TYPE, optional
            DESCRIPTION. The default is None.
        polarity : TYPE, optional
            DESCRIPTION. The default is None.
        ionisation_Source : TYPE, optional
            DESCRIPTION. The default is None.
        analyzer_Type : TYPE, optional
            DESCRIPTION. The default is None.
        maldi_Matrix : TYPE, optional
            DESCRIPTION. The default is None.
        organism : TYPE, optional
            DESCRIPTION. The default is None.
    
        Returns
        -------
        A dataframe object of metadata from Metaspace.
    
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
        
        #FIXME
        return temp_List
        #return self.make_dataframe(temp_List)
        
    
    

    def make_dataframe(self, list_of_datasets): 
        #FIXME Create the dataframe and enable user to download datasets of their chosing
                
        #if the list_of_datasets is not emtpy, then run
        if (list_of_datasets):
            column_List = ["Name", "ID", "Submitter", "Group",
                           "Analyzer", "Metadata Type", "Ionisation Source",
                           "Organism", "Organism Part", "Adducts","Condition",
                           "SMDataset Object"]
            
            return pd.concat([pd.DataFrame([[
                                         dataset.name,
                                         dataset.id,
                                         dataset._info["submitter"],
                                         dataset._info["group"],
                                         dataset._metadata["MS_Analysis"]["Analyzer"],
                                         dataset._info["metadataType"],
                                         dataset._info["ionisationSource"],
                                         dataset._info["organism"],
                                         dataset._info["organismPart"],
                                         dataset._info["adducts"],
                                         dataset._info["condition"],
                                         dataset]],
                                         columns= column_List) for dataset in list_of_datasets],
                                         ignore_index=True)
            
        #If the list_of_datasets is empty, then set __dataset_DF = None
        else:
            return pd.DataFrame()

        

    #FIXME
    def filter_search_results(self,
                           dataframe,
                           filterKeywords = list(),
                           filterParameter = None,
                           adducts = False,
                           analyzer = False,
                           condition = False,
                           group = False,
                           growthConditions = False,
                           ionisationSource = False,
                           maldiMatrix = False,
                           metadataType = False,
                           organism = False,
                           organismPart = False,
                           polarity = False,
                           pixelSize = False
                           ):
        '''
        Description
        ----------
        This function will filter a given dataframe of metadata.
        Choose what to filter by and provide appropriate arguments for the 
        required parameters.
        
        Note: To filter multiple times, you will need to call this function 
        multiple times for each desired filter.
        
        Parameters
        ----------
        dataframe : Pandas dataframe object
            A Dataframe you wish to filter.
            
        filterKeywords : List object, optional
            A list of str keywords to filter the dataframe. 
            The default is list().
            
        filterParameter : String object, optional
            The section in which you want to check. 
            The default is None.
            
        adducts : Bool value, optional
            When true it will filter the dataframe based on dataset's on adducts.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        analyzer : Bool value, optional
            When true it will filter the dataframe based on the analyzer.
            It requires an argument for parameter(s) filterKeywords, filterParameter.
            Available filterParameter values: "type", "resolvingPower"
            The default is False.
            
        condition : Bool value, optional
            When true it will filter the dataframe based on the condition.
            It requires an argument for parameter(s) filterKeywords
            The default is False.
            
        group : Bool value, optional
            When true it will filter the dataframe based on the group.
            It requires an argument for parameter(s) filterKeywords, filterParameter.
            Available filterParameter values: "id", "name", "shortName"
            The default is False.
            
        growthConditions : Bool value, optional
            When true it will filter the dataframe based on the growth conditions.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        ionisationSource : Bool value, optional
            When true it will filter the dataframe ased on the ionisation source.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        maldiMatrix : Bool value, optional
            When true it will filter the dataframe based on the maldi matrix.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        metadataType : Bool value, optional
            When true it will filter the dataframe based on the metadata type.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        organism : Bool value, optional
            When true it will filter the dataframe based on the organism.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        organismPart : Bool value, optional
            When true it will filter the dataframe based on the organism part.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        polarity : Bool value, optional
            When true it will filter the dataframe based on the polarity.
            It requires an argument for parameter(s) filterKeywords.
            The default is False.
            
        pixelSize : Bool value, optional
            When true it will filter the dataframe based on the pixel size of
            either the x-axis or y-axis.
            It requires an argument for parameter(s) filterKeywords, filterParameter.
            Available filterParameter values: "Xaxis", "Yaxis".
            The default is False
            

        Returns
        -------
        A dataframe object of metadata.

        '''
        
        search_Results = dataframe["SMDataset Object"]
        filtered_list = list()
        
        if (adducts):
            for keyword in filterKeywords:
                for item in search_Results.items():
                   adducts = self.get_dataset_adducts(item[1])
                   if(adducts.count(keyword) != 0):
                       SMObject = search_Results.pop(item[0])
                       filtered_list.append(SMObject)
                       
        elif(analyzer):
            #it only checks type and resolvingPower separatley
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(str(item[1]._info["analyzer"][filterParameter]) == str(keyword)):
                        SMObject = search_Results.pop(item[0])
                        filtered_list.append(SMObject)
                        
        elif(condition):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1]._info["condition"]):
                       SMObject = search_Results.pop(item[0])
                       filtered_list.append(SMObject) 
            
        elif(group):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1]._info["group"][filterParameter]):
                       SMObject = search_Results.pop(item[0])
                       filtered_list.append(SMObject)
            
        elif(growthConditions):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1]._info["growthConditions"]):
                       SMObject = search_Results.pop(item[0])
                       filtered_list.append(SMObject)
                       
        elif(ionisationSource):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1]._info["ionsationSource"]):
                       SMObject = search_Results.pop(item[0])
                       filtered_list.append(SMObject) 
                           
        elif(maldiMatrix):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1]._info["maldiMatrix"]):
                        SMObject = search_Results.pop(item[0])
                        filtered_list.append(SMObject)
        
        
        elif(metadataType):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1]._info["metadataType"]):
                         SMObject = search_Results.pop(item[0])
                         filtered_list.append(SMObject)   
     
        elif(organism):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1]._info["organism"]):
                         SMObject = search_Results.pop(item[0])
                         filtered_list.append(SMObject)
        
        elif(organismPart):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if (keyword == item[1]._info["organismPart"]):
                        SMObject = search_Results.pop(item[0])
                        filtered_list.append(SMObject)
        
        elif(polarity):
            for keyword in filterKeywords:
                for item in search_Results.items():
                    if(keyword == item[1].polarity):
                       SMObject = search_Results.pop(item[0])
                       filtered_list.append(SMObject) 
        
        elif(pixelSize): #FIXME
            pass
        
        
        else:
            pass
        
        return self.make_dataframe(filtered_list)
                   
        
        
    def dataset_selection(self,dataset_DF , selected_datasets = [], df_Column = "Name"):
        #FIXME param: df_Column is set to default "Name"
        #allow for other ways to select data. This needs more logic.
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
        if (dataset_DF.empty):
            print("Dataframe is emtpy")

        #Runs if the __dataset_DF is not None        
        else:
            #True when the list "chosen_datasets" is empty
            if not selected_datasets:        
                downloadDatasets = dataset_DF["SMDataset Object"]
                
                for dataset in downloadDatasets:
                    print(dataset.name)
                    
            #Runs when the list "chosen_datasets" is not emtpy    
            else:
                for dataset in selected_datasets:
                    print(dataset_DF.loc[dataset_DF[df_Column] == dataset, df_Column])

                
                

 
        

    
    def get_dataset_name(self, dataset):
        return dataset.name

    def get_dataset_id(self, dataset):
        return dataset.id
    
    def get_dataset_adducts(self,dataset):
        return dataset.adducts
    
    


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

