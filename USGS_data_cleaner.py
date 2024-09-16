# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 11:36:37 2019

@author: rmc33
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 21:27:06 2019

@author: rmc33
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from functools import reduce
#from RFs import getDuplicateColumns

# folder with data
myfile = os.path.join('results_phy.csv')
file2 = os.path.join('station_phy.csv')
stations= pd.read_csv(file2)
data = pd.read_csv(myfile)
columns_to_drop=[
 'OrganizationFormalName',
 'ActivityIdentifier',
 'ActivityTypeCode',
 'ActivityMediaName',
 'ActivityMediaSubdivisionName',
 'ActivityStartTime/Time',
 'ActivityStartTime/TimeZoneCode',
 'ActivityEndDate',
 'ActivityEndTime/Time',
 'ActivityEndTime/TimeZoneCode',
 'ActivityDepthHeightMeasure/MeasureValue',
 'ActivityDepthHeightMeasure/MeasureUnitCode',
 'ActivityDepthAltitudeReferencePointText',
 'ActivityTopDepthHeightMeasure/MeasureValue',
 'ActivityTopDepthHeightMeasure/MeasureUnitCode',
 'ActivityBottomDepthHeightMeasure/MeasureValue',
 'ActivityBottomDepthHeightMeasure/MeasureUnitCode',
 'ProjectIdentifier',
 'ActivityConductingOrganizationText',
 'ActivityCommentText',
 'SampleAquifer',
 'HydrologicCondition',
 'HydrologicEvent',
 'SampleCollectionMethod/MethodIdentifier',
 'SampleCollectionMethod/MethodIdentifierContext',
 'SampleCollectionMethod/MethodName',
 'SampleCollectionEquipmentName',
 'ResultDetectionConditionText',
 'MeasureQualifierCode',
 'StatisticalBaseCode',
 'ResultWeightBasisText',
 'ResultTimeBasisText',
 'ResultTemperatureBasisText',
 'ResultParticleSizeBasisText',
 'ResultCommentText',
 'USGSPCode',
 'ResultDepthHeightMeasure/MeasureValue',
 'ResultDepthHeightMeasure/MeasureUnitCode',
 'ResultDepthAltitudeReferencePointText',
 'SubjectTaxonomicName',
 'SampleTissueAnatomyName',
 'ResultAnalyticalMethod/MethodIdentifier',
 'ResultAnalyticalMethod/MethodIdentifierContext',
 'ResultAnalyticalMethod/MethodName',
 'MethodDescriptionText',
 'LaboratoryName',
 'AnalysisStartDate',
 'DetectionQuantitationLimitTypeName',
 'PreparationStartDate',
 'ProviderName']
columns_to_drop_existing=[col for col in columns_to_drop if col in data.columns]
if columns_to_drop_existing:
    data = data.drop(columns_to_drop_existing, axis=1)

#New column, combined to make an ID based on date and station
data["ID"] = data["MonitoringLocationIdentifier"].map(str) + data["ActivityStartDate"]
df=data[data['ResultStatusIdentifier']=='Accepted'].copy()
#Cr_df=df[df['CharacteristicName']=='Chromium'].copy()
#Cr_df['Cr']=Cr_df['ResultMeasureValue']
#V_df=df[df['CharacteristicName']=='Vanadium'].copy()
#V_df['V']=V_df['ResultMeasureValue']
#out_df=pd.merge(Cr_df, V_df, on='ID', how='outer')

species=data['CharacteristicName'].unique()
d={}
for i in species:
    frame=df[df['CharacteristicName']==i].copy()
    frame[i]=frame['ResultMeasureValue']
#    new_name = 'df{}'.format(i)
    d[i]=frame
    
chems=df.CharacteristicName.unique()
d2={}

for i in chems:
    a=d[i].copy()
    a2=a[(a['ResultSampleFractionText']=='Dissolved').copy()]
    a3=a2.fillna(0)
    d2[i]=a3


final_s=chems

d3={}

for i in final_s:
    df=d[i].copy()
    b=df.drop(columns=['OrganizationIdentifier',                       
                       'CharacteristicName',
                       'ResultSampleFractionText',
                       'ResultMeasureValue',
                       'ResultMeasure/MeasureUnitCode',
                       'ResultStatusIdentifier',
                       'ResultValueTypeName',
                       'ResultLaboratoryCommentText',
                       'DetectionQuantitationLimitMeasure/MeasureValue',
                       'DetectionQuantitationLimitMeasure/MeasureUnitCode']).copy()
    d3[i]=b

# data_frames=[d3['Arsenic'], d3['Chromium'], d3['Gross-Uranium'], d3['pH'],
#        d3['Oxygen'], d3['Vanadium'], d3['Iron'], d3['Ferrous ion']]

# Extract the DataFrames from the dictionary
dfs = list(d3.values())



# #Okay things seems fucked up so lets see what all the unique headers are in d3
# # Initialize an empty set to store unique column headers
# unique_columns = set()

# # Iterate over each DataFrame in the dictionary
# for df in d3.values():
#     # Update the set with the column headers of the current DataFrame
#     unique_columns.update(df.columns)

# # Convert the set to a list
# unique_columns_list = list(unique_columns)

# # Print the list of unique column headers
# print(unique_columns_list)

columns_to_drop = ['ResultDetectionQuantitationLimitUrl', 'ProjectName', 
                    'DataQuality/PrecisionValue', 
                    'ResultAnalyticalMethod/MethodUrl', 
                    'LabSamplePreparationUrl', 'MethodSpeciationName', 
                    'LastUpdated', 'DataQuality/BiasValue', 
                    'ActivityRelativeDepthName', 
                    'SampleCollectionMethod/MethodDescriptionText', 
                    'DataQuality/LowerConfidenceLimitValue', 
                    'DataQuality/ConfidenceIntervalValue', 
                    'ResultAnalyticalMethod/MethodDescriptionText', 
                    'ResultFileUrl', 'DataQuality/UpperConfidenceLimitValue', 
                    'BinaryObjectFileTypeCode', 'BinaryObjectFileName',
                    'MonitoringLocationName', 'ActivityLocation/LatitudeMeasure',
                    'ActivityLocation/LongitudeMeasure', 'ResultIdentifier']

for df_name, df in d3.items():
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

#get rid of those weird heading suffixes
for key, df in d3.items():
    # Rename the columns
    df.rename(columns=lambda x: x.split('_')[0], inplace=True)

    
###DEALING WITH TIME
time = d3.copy()
for key, df in time.items():
    time[key] = df[['ID', 'ActivityStartDate']]

# Create an empty DataFrame to store the merged information
merged_df = pd.DataFrame(columns=['ID', 'ActivityStartDate'])

# Loop through each key-value pair in the dictionary
for key, df in time.items():
    # Extract 'ID' and 'ActivityStartDate' columns from the DataFrame
    id_and_date_df = df[['ID', 'ActivityStartDate']]
    
    # Concatenate the extracted DataFrame with the merged DataFrame
    merged_df = pd.concat([merged_df, id_and_date_df], ignore_index=True)

# Drop duplicate rows based on the 'ID' column
merged_df.drop_duplicates(subset='ID', inplace=True)

# Optionally, sort the DataFrame by the 'ID' column
merged_df.sort_values(by='ID', inplace=True)

# Print the merged DataFrame
print(merged_df)


#####DEALING WITH PLACE
place = d3.copy()
for key, df in place.items():
    place[key] = df[['ID', 'MonitoringLocationIdentifier']]

# Create an empty DataFrame to store the merged information
merged_df2 = pd.DataFrame(columns=['ID', 'MonitoringLocationIdentifier'])

# Loop through each key-value pair in the dictionary
for key, df in place.items():
    # Extract 'ID' and 'ActivityStartDate' columns from the DataFrame
    id_and_date_df = df[['ID', 'MonitoringLocationIdentifier']]
    
    # Concatenate the extracted DataFrame with the merged DataFrame
    merged_df2 = pd.concat([merged_df2, id_and_date_df], ignore_index=True)

# Drop duplicate rows based on the 'ID' column
merged_df2.drop_duplicates(subset='ID', inplace=True)

# Optionally, sort the DataFrame by the 'ID' column
merged_df2.sort_values(by='ID', inplace=True)

# Print the merged DataFrame
print(merged_df2)


######DEALINGWITHCHEMICALS

chems = d3.copy()
conly = ['ActivityStartDate', 'MonitoringLocationIdentifier']
for df_name, df in chems.items():
    df.drop(columns=[col for col in conly if col in df.columns], inplace=True)

# Initialize a list to store the dataframes
dfs = []

# Loop through each dataframe in the dictionary
for df in chems.values():
    # Extract 'ID' and the unique column
    id_and_unique = df[['ID', df.columns[-1]]]  # Assuming the unique column is the last column
    
    # Append the extracted dataframe to the list
    dfs.append(id_and_unique)

# Merge the dataframes on 'ID'
merged_df3 = pd.concat(dfs, ignore_index=True).groupby('ID').first().reset_index()

# Print the merged dataframe
print(merged_df3)

# Merge merged_df1 and merged_df2 on 'ID'
merged_df12 = pd.merge(merged_df, merged_df2, on='ID', how='outer')

# Merge merged_df12 and merged_df3 on 'ID'
final_merged_df = pd.merge(merged_df12, merged_df3, on='ID', how='outer')

# Print the final merged dataframe
print(final_merged_df)

# Perform inner merge on 'MonitoringLocationIdentifier'
final_combined_df = pd.merge(final_merged_df, stations, on='MonitoringLocationIdentifier', how='inner')

# Print the final combined dataframe
print(final_combined_df)

final_combined_df.to_csv('dissolved_data_phy.csv', index=False)

# id_presence = []

# # Iterate over each DataFrame in the dictionary
# for df in d3.values():
#     # Check if the 'ID' column is present in the current DataFrame
#     id_present = 'ID' in df.columns
#     id_presence.append(id_present)

# # Check if 'ID' is present in all DataFrames
# if all(id_presence):
#     print("'ID' column is present in all DataFrames")
# else:
#     print("'ID' column is not present in all DataFrames")


# # Define the merge function
# def merge_dfs(left, right):
#     merged = pd.merge(left, right, on='ID', how='outer')
    
#     # Specify custom suffixes only for the columns you mentioned
#     for col in ["ResultIdentifier", "monitoring_location", "date"]:
#         if col + '_right' in merged.columns:
#             # Rename columns with custom suffixes
#             merged.rename(columns={col + '_left': col, col + '_right': col + '_duplicate'}, inplace=True)
    
#     return merged

# # Use reduce to merge all DataFrames
# merged_df = reduce(merge_dfs, dfs)


# #things are really fucked up with the duplicates so export the file at this
# #modify it offline, and then reimport it
# #df_reduced.to_csv(os.path.join('reduced.csv'))

# # file3 = os.path.join('reduced.csv')
# # reduced= pd.read_csv(file3)

# # reduced=reduced.sort_values(by=['ActivityStartDate'])
# # reduced['dup']=reduced.duplicated(subset='MonitoringLocationIdentifier',keep='last')
# # reduced=reduced[reduced['dup']==False]
# # ph_drop=reduced.dropna(subset=['pH'])
# # final0=ph_drop.dropna(thresh=8)
# # final=final0.merge(stations)
# # final.to_csv(os.path.join('USGS_chem.csv'))