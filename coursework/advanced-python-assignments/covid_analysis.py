# Hw5 - web json covid cases

# PRE WORKS
import requests
import json
import numpy as np 
import datetime as dt # so our dates can be pretty

# VARIABLES
states_territory_ticker = ["al", "ar", "as", "az", "ca", "co", "ct", "dc", "de", "fl",
                           "ga", "gu", "hi", "ia", "id", "il", "in", "ks", "ky", "la",
                           "ma", "md", "me", "mi", "mn", "mo", "mp", "ms", "mt", "nc",
                           "nd", "ne", "nh", "nj", "nm", "nv", "ny", "oh", "ok", "or",
                           "pa", "pr", "ri", "sc", "sd", "tn", "tx", "ut", "va", "vi",
                           "vt", "wa", "wi", "wv", "wy"]
temp_list = ["ut"] # for testing 
positive_daily_cases = [] # need to divide by the length

# KEYS NEEDED
key_state = "state"
key_daily_pos_cases = "positiveIncrease" #append all to positive_daily_cases list
key_date = "date"

month_spelled_out = ["January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"]

# FUNCTIONS
def initial_get_JSON_data(url):
  request = requests.get(url)
  dct_full = json.loads(request.text)
  return dct_full

def formt_dte_numb(key_date):
  date_str = str(key_date)
  date_obj = dt.datetime.strptime(date_str, '%Y%m%d') # add datetime back 
  prtty_date_frmt = date_obj.strftime('%m-%d-%Y')
  return prtty_date_frmt

def get_key_sort_dict(one_dctnry):
  return one_dctnry[key_date] # Need this for .sort() 

def month_total_per_year(dctnry):
  global jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec # make it global or it won't work - can't access it
  num_of_pos = dctnry[key_daily_pos_cases]
  if month == "01":
    if jan is None: # add check for none / null values 
      jan = num_of_pos
    else:
      jan += num_of_pos
  elif month == "02":
    if feb is None:
      feb = num_of_pos
    else:
      feb += num_of_pos
  elif month == "03":
    if mar is None:
      mar = num_of_pos
    else:
      mar += num_of_pos
  elif month == "04":
    if apr is None:
      apr = num_of_pos
    else:
      apr += num_of_pos
  elif month == "05":
    if may is None:
      may = num_of_pos
    else:
      may += num_of_pos
  elif month == "06":
    if jun is None:
      jun = num_of_pos
    else:
      jun += num_of_pos
  elif month == "07":
    if jul is None:
      jul = num_of_pos
    else:
      jul += num_of_pos
  elif month == "08":
    if aug is None:
      aug = num_of_pos
    else:
      aug += num_of_pos
  elif month == "09":
    if sep is None:
      sep = num_of_pos
    else:
      sep += num_of_pos
  elif month == "10":
    if oct is None:
      oct = num_of_pos
    else:
      oct += num_of_pos
  elif month == "11":
    if nov is None:
      nov = num_of_pos
    else:
      nov += num_of_pos
  elif month == "12":
    if dec is None:
      dec = num_of_pos
    else:
      dec += num_of_pos
  return [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec] # return list of pos cases per month

# BODY OF CODE

# Get JSON data -> load into dictionary 
for state in states_territory_ticker:
  url = 'https://api.covidtracking.com/v1/states/'+state+'/daily.json'
  all_data = initial_get_JSON_data(url)  

  # sort data - pre step to make finding the highest and lowest month/year
  all_data.sort(key=get_key_sort_dict)
 
  # reset var for all states 
  positive_daily_cases = []
  max_pos_cases = 0
  max_pos_cases_date = 0
  no_pos_cases_date = 0

  # setting months to none instead of 0 - check to see if we actually have data for x month 
  jan = None
  feb = None
  mar = None
  apr = None
  may = None
  jun = None
  jul = None
  aug = None
  sep = None
  oct = None
  nov = None
  dec = None

  # setting lists to empty
  pos_cases_2020 = []
  pos_cases_2021 = []
  pos_cases_2022 = []

  # year switch yet? - check
  current_year = "2020"

# Analysis 
   
  for dctnry in all_data:
    
    # Average number of new daily confirmed cases p1
    positive_daily_cases.append(dctnry[key_daily_pos_cases])

    # Date with highest new num of covid cases
    if dctnry[key_daily_pos_cases] > max_pos_cases:
      max_pos_cases = dctnry[key_daily_pos_cases] # update logic
      max_pos_cases_date = dctnry[key_date] # update logic
     
    # most recent date with no new covid cases
    if dctnry[key_daily_pos_cases] == 0 and dctnry[key_date] > no_pos_cases_date:
      no_pos_cases = dctnry[key_daily_pos_cases] # update logic
      no_pos_cases_date = dctnry[key_date] # update logic
    
    # month / year highest total cases & lowest total cases 
    date_str = str(dctnry[key_date]) 
    year = date_str[0:4] # get year alone
    month = date_str[4:6] # get month alone

    #print("cy before check:", current_year, "y before check:", year)
    if current_year != year: #check if years have switched yet
      #print("cy", current_year, "y", year)

      # trigger year switched
      # save before resetting
      if current_year == "2020":
        pos_cases_2020 = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
        #print("current year = 2020:", pos_cases_2020 )

      if current_year == "2021":
        pos_cases_2021 = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec] # add monthly totals to empty list
        #print("current year = 2021:", pos_cases_2021 )

      elif current_year == "2022":
        pos_cases_2022 = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
        #print("current year = 2022:", pos_cases_2022 )

      
    
      #reset 
      jan = None
      feb = None
      mar = None
      apr = None
      may = None
      jun = None
      jul = None
      aug = None
      sep = None
      oct = None
      nov = None
      dec = None

      current_year = year #update
      #print("update current year / year switch", current_year, type(current_year))
      month_total_per_year(dctnry) # add first val for xx year to function variable - all variables in function should be empty now. 
      
    month_total_per_year(dctnry) # add positive cases to monthly total
  
  # clause for end of dictioanry - the last year in the dict won't append because we never hit a new year, it just ends - logic to catch that and add up monthly totals when we have no new dicts
  if current_year == "2020":
    pos_cases_2020 = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
  elif current_year == "2021":
    pos_cases_2021 = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
  elif current_year == "2022":
    pos_cases_2022 = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

  # find max value and min value - save the month and year for analysis - add all lists to this 
  all_data_analysis = []

 # Add all values that are not "none" and the info - do this for all lists
  for i in range(len(pos_cases_2020)):
      if pos_cases_2020[i] is not None: # don't want nones
          all_data_analysis.append((pos_cases_2020[i], month_spelled_out[i], "2020"))

  for i in range(len(pos_cases_2021)):
      if pos_cases_2021[i] is not None:
          all_data_analysis.append((pos_cases_2021[i], month_spelled_out[i], "2021"))

  for i in range(len(pos_cases_2022)):
      if pos_cases_2022[i] is not None:
          all_data_analysis.append((pos_cases_2022[i], month_spelled_out[i], "2022"))


  # Find max and min
  max_data = max(all_data_analysis)
  min_data = min(all_data_analysis) #####

  # Average number of new daily confirmed cases p2
  daily_avg = np.mean(positive_daily_cases)

  # THE OUTPUT
  print("Covid confirmed cases statistics: ")
  print("State Name: ", state.upper()) # Make abbreviated state upper bc lower is ugly
  
  print("\t", "Average number of new daily confirmed cases: ", round(daily_avg, 2)) 
  if max_pos_cases_date != 0:
    print("\t", "Date with the highest new number of cases: ", formt_dte_numb(max_pos_cases_date))
  else:
    print("\t", "Not Available")
  if no_pos_cases_date != 0:
    print("\t", "Most recent date with no new cases: ", formt_dte_numb(no_pos_cases_date))
  else:
    print("\t", "Not Available")
  print("\t", "The month and year with the overall highest new number of cases: ", 
        max_data[1], max_data[2], f"({max_data[0]} cases)")
  print("\t", "The month and year with the overall lowest new number of cases: ", 
        min_data[1], min_data[2], f"({min_data[0]} cases)")

  # Create the combined data structure
  analysis_summary = {
      "state": state.upper(),
      "average_daily_cases": round(daily_avg, 2),
      "highest_cases_date": max_pos_cases_date,
      "highest_cases_count": max_pos_cases,
      "most_recent_no_cases_date": no_pos_cases_date,
      "highest_month_year": f"{max_data[1]} {max_data[2]}",
      "highest_month_cases": max_data[0],
      "lowest_month_year": f"{min_data[1]} {min_data[2]}",
      "lowest_month_cases": min_data[0]
  }

  state_data = {
      "analysis": analysis_summary,
      "raw_data": all_data
  }

  # Use your existing save code
  file = open(state + ".json", "w")
  json.dump(state_data, file)  # Save state_data instead of just all_data
  file.close()

  # counter += 1

# print("counter:", counter)  - check to make sure all states & territories print
# pull json in , save it as dictionary, do analysis, append analysis to dictionary per state, save dictionary per state as json file.
