'''P1 - pull data from api'''

import json
import requests


def initial_data_pull(state):
    # get csv files for all states in Rocky Mountains and West Coast 
    url = 'https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=monthly&data[0]=consumption-for-eg-btu&data[1]=generation&facets[location][]='+state+'&facets[fueltypeid][]=COL&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=PET&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&start=2001-01&end=2020-01&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000&api_key=[InsertYourOwnAPIKeyHere]'
    
    response = requests.get(url)
    data = json.loads(response.text)
      
    # change null values to 0         
    for dictionary in data["response"]["data"]:
        if dictionary["generation"] == None:
            dictionary["generation"] = "0"
            
    for dictionary in data["response"]["data"]:
        if dictionary["consumption-for-eg-btu"] == None:
            dictionary["consumption-for-eg-btu"] = "0"
    
    # save into csv file
    with open("/home/ubuntu/environment/Homework/final_proj/"+state+".csv", "w") as file:
    
        for dictionary in data["response"]["data"]:
            file.write(
            (dictionary["period"]+","+
             dictionary["fueltypeid"]+","+
             dictionary["generation"]+","+
             dictionary["generation-units"]+","+
             dictionary["consumption-for-eg-btu"]+","+
             dictionary["consumption-for-eg-btu-units"]+","+"\n"))
    
    
def append_data(state):
    # pull data from API
    url = 'https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?frequency=monthly&data[0]=consumption-for-eg-btu&data[1]=generation&facets[location][]='+state+'&facets[fueltypeid][]=COL&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=PET&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&start=2020-01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key=k2JhsSL7CEVPHHpFpufa3EihiGUEIOI3dfdAxPfN'
    
    response = requests.get(url)
    data = json.loads(response.text)
      
      
    # read lines in
    with open("/home/ubuntu/environment/Homework/final_proj/"+state+".csv") as csv_file:
        csv_lines = csv_file.readlines()
        last_period = csv_lines[0].split(",")[0]
      
    # change null values to 0         
    for dictionary in data["response"]["data"]:
        if dictionary["generation"] == None:
            dictionary["generation"] = "0"
            
    for dictionary in data["response"]["data"]:
        if dictionary["consumption-for-eg-btu"] == None:
            dictionary["consumption-for-eg-btu"] = "0" 
    
    # append new lines w/date checker 
    new_lines = []
    
    with open("/home/ubuntu/environment/Homework/final_proj/"+state+".csv", "a") as file:
    
        for dictionary in data["response"]["data"]:
            # date checker 
            if dictionary["period"] == last_period:
                break
            else:
                new_lines.append(
                (dictionary["period"]+","+
                 dictionary["fueltypeid"]+","+
                 dictionary["generation"]+","+
                 dictionary["generation-units"]+","+
                 dictionary["consumption-for-eg-btu"]+","+
                 dictionary["consumption-for-eg-btu-units"]+","+"\n"))
        file.writelines(new_lines[::-1])        
     
def usage_and_efficieny(states):
    # variables
    dateCounter = 0
    fuelTypeCounter = 0
    outputTotal = 0
    inputTotal = 0
    usage = 0
    efficieny = 0
    
    
    # read in lines from csv files 
    lsts = [line.split(",") for line in open("/home/ubuntu/environment/Homework/final_proj/"+state+".csv").readlines()]
    
    # pull dates - need empty list
    dates = []
    lenOfDatesLst = 0
    
    # pull distinct date index from list and append to list
    for lst in lsts:
        for i in dates:
            if lst[0] == i:
                break
        else: 
            if lst[0] != dates[:]:
                dates.append(lst[0])
                lenOfDatesLst += 1
           
    # dict setup for state (dict in dict for each state)
    results[state] = {}
    
    # loop through fuel type
    for fuel in fuelType:
       
        # index out of range check
        if fuelTypeCounter >= 5:
            break
        
        print("Fuel Type:", fuelType[fuelTypeCounter])
        
        # dict set up for each fuel type 
        results[state][fuel] = {}
        
        # loop through list with data 
        for lst in lsts:
            # index out of range check
            if dateCounter >= lenOfDatesLst:
                break
            
            # date and fuel type checker
            if lst[0] == dates[dateCounter] and lst[1] == fuelType[fuelTypeCounter]:

                print("Date:", dates[dateCounter])
                
                # the math setup
                outputTotal += float(lst[2])
                inputTotal += float(lst[4])
                
                # check for division by 0
                if outputTotal == 0:
                    usage = 0   
                    efficiency = 0
                else:
                    # the math 
                    usage = round((inputTotal/outputTotal),4)
                    efficiency = round(((inputTotal/outputTotal)*100),3)
            
                print("Usage Intake vs Output Production:", usage, "BTU/Watthour",efficiency,"% efficient")
                
                # save math & date into dict
                results[state][fuel][dates[dateCounter]] = {
                    "usage" : usage, 
                    "efficiency" : efficiency 
                    }
                
                # increment date
                dateCounter += 1 
                
        # reset for each fuel type & increment counter
        outputTotal = 0
        inputTotal = 0
        usage = 0
        efficieny = 0
        dateCounter = 0
        fuelTypeCounter += 1
        print()
    print()
    print()   
        
 

def save_results(results):
    # json file
    json.dump(results, open("/home/ubuntu/environment/Homework/final_proj/results.json", "w"), indent=4)
    
# do I need another result for append results?? - no 

states = ["UT", "MT", "ID", "WY", "CO", "CA", "AZ", "NV", "OR", "WA"]

fuelType = ["COL", "PET", "NG", "HYC", "WND", "SUN"]
# coal, petroleum, natural gas, conventional hydroelectric, wind, sun

results = {}

# project explanation
print(" In this project we are measuring how much heat is required to product one watt per hour of electricity for different fuel types in different states. NOTE: the data updates on the 23rd of each month with the new months information.", "\n")
# note: data from previous months may be revised in each update. 
    
for state in states:
    # pull data from api
    #initial_data_pull(state)  #I must only use this once
    
    # add new data to csv
    append_data(state)
    
    print("State:", state)
    
    # the math
    usage_and_efficieny(state)
    
    
# save results into json
save_results(results)
        
       
