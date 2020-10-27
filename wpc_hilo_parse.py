#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 01:57:55 2020

@author: Justin Richling
"""

import pandas as pd

def front_parse_latlon(latlon_code="0560149",print_on=True):
    '''Grab lat and lon from coded values from WPC frontal analysis data
    
    Arguments
    ---------
    code : string
        ***** required - 7 digit string *****
        * format in XXXYYYY, with:
        XXX : 3-digit latitude; with a period in front of last digit
            ex. 384 -> 38.4 -> 38.4 deg north
            ex. 045 -> 04.5 -> 4.5 deg north
            ex. 009 -> 00.9 -> 0.9 deg north
        YYYY : 4-digit longitude; with a period in front of last digit
            ex. 1147 -> 114.7 -> 114.7 deg west
            ex. 0979 -> 097.9 -> 97.9 deg west
            ex. 0035 -> 003.5 -> 3.5 deg west
            
    Returns
    -------
    lat : str
        converted latitude
    lon : str
        converted longitude
    '''
    if len(latlon_code) != 7:
        raise Exception(f"Wrong number of digits in coded lat/lon: {latlon_code}\n\n"+\
                        f"Coded lat/lon number of digits: {len(latlon_code)}\n"+\
                        
                       "\nPlease check data and ensure you are given coded lat/lon pairs with 7 digits.\n"+\
                    "\nsee docs\n")
    lat_raw = latlon_code[0:3]
    lon_raw = latlon_code[3:]
    if print_on == True:
        print("-----------------------------------------------------")
        print(f"raw latitude: {lat_raw}\nraw longitude: {lon_raw}\n")
    
    lat = f"{latlon_code[0:2]}.{latlon_code[2:3]}".strip("00")
    lon = f"{latlon_code[3:-1]}.{latlon_code[-1:]}".strip("00")
    if print_on == True:
        print(f"converted latitude (N): {float(lat)}\nconverted longitude (W): {float(lon)}\n")
    
    return lat,lon


def get_HiLo_lat_lon(hilo_points):
    
    '''
    
    hilo_points : list or like type
        all row index numbers for group
    
    Add function to check subsequent lines for values if they are
    contained in multiple rows in the dataframe
    '''
    
    hilo = [front_parse_latlon(i,print_on=False) for i in hilo_points]
    
    lats_hilo = [float(i[0]) for i in hilo]
    # make the longitudes negative since they are in degrees west
    lons_hilo = [-float(i[1]) for i in hilo]
    return lats_hilo,lons_hilo




def parse_hilo(filename,name):
    '''Some high/low data continue on new rows, this function will
    append the data from new lines
    
    Parameters
    ----------
    name : str
        name of high/low from text file;
        ie "HIGHS" OR "LOWS"
    
    Returns
    -------
    '''
    fronts_data = pd.read_fwf(filename,
                          header=None)
    hilo_data_merged = []
    for i in range(fronts_data.shape[0]):
        #print(i)
        if name in fronts_data.iloc[i][0][:5]:

            hilo_data_merged.append(fronts_data.iloc[i][0])

            for j in range(i+1,fronts_data.shape[0]-1):
                if fronts_data.iloc[j][0][0].isdigit():
                    if len(fronts_data.iloc[j][0].split()[0]) > 3:
                        hilo_data_merged.append(fronts_data.iloc[j][0])
                if fronts_data.iloc[j][0][0].isalpha():
                    break
    
    
    hilo_data_joined = ', '.join(hilo_data_merged)
    hilo_data = hilo_data_joined.replace(",","")
    hilo_data = hilo_data.replace(f"{name} ","")
    return hilo_data


