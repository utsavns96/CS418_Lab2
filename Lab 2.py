#!/usr/bin/env python
# coding: utf-8

# # Lab 2
# UIC CS 418, Spring 2023
# 
# ## Academic Integrity Policy
# 
# According to the Academic Integrity Policy of this course, all work submitted for grading must be done individually, unless otherwise specified. While we encourage you to talk to your peers and learn from them, this interaction must be superficial with regards to all work submitted for grading. This means you cannot work in teams, you cannot work side-by-side, you cannot submit someone else’s work (partial or complete) as your own. In particular, note that you are guilty of academic dishonesty if you extend or receive any kind of unauthorized assistance. Absolutely no transfer of program code between students is permitted (paper or electronic), and you may not solicit code from family, friends, or online forums. Other examples of academic dishonesty include emailing your program to another student, copying-pasting code from the internet, working in a group on a homework assignment, and allowing a tutor, TA, or another individual to write an answer for you. 
# If you have questions, please ask us on Piazza.
# You must reference (including URLs) of any resources other than those linked to in the assignment, or provided by the professor or TA.
# 
# Academic dishonesty is unacceptable, and penalties range from failure to expulsion from the university; cases are handled via the official student conduct process described at https://dos.uic.edu/conductforstudents.shtml._
# 
# We will run your code through MOSS software to detect copying and plagiarism.
# 
# ##To submit this assignment:
# 1. Execute all commands and complete this notebook	
# 2. Download your Python Notebook (**.ipynb** file) and upload it to Gradescope
# under *Lab 2*. **Make sure you check that your **ipynb** file includes all parts of your solution (including the outputs).**
# 2.	Export your Notebook as a python file (**.py** file) and upload it to Gradescope under *.py file for Lab 2*. 
# 

# ### Part 1 - Questions (50%)
# 
# The practice problems below use the department of transportation's "On-Time" flight data for all flights originating from SFO or OAK in January 2016. Information about the airports and airlines are contained in the comma-delimited files `airports.dat` and `airlines.dat`, respectively.  Both were sourced from http://openflights.org/data.html.
# 
# Disclaimer: There is a more direct way of dealing with time data that is not presented in these problems.  This activity is merely an academic exercise.

# #### Setup

# In[1]:


import pandas as pd
import numpy as np
import math


# In[2]:


flights = pd.read_csv("flights.dat", dtype={'sched_dep_time': 'f8', 'sched_arr_time': 'f8'})
# show the first few rows, by default 5
flights.head(3) 


# In[3]:


airports_cols = [
    'openflights_id',
    'name',
    'city',
    'country',
    'iata',
    'icao',
    'latitude',
    'longitude',
    'altitude',
    'tz',
    'dst',
    'tz_olson',
    'type',
    'airport_dsource'
]

airports = pd.read_csv("airports.dat", names=airports_cols)
airports.head(3)


# #### Question 1.1 **(20%)**
# It looks like the departure and arrival in `flights` were read in as floating-point numbers.  Write two functions, `extract_hour` and `extract_mins` that converts military time to hours and minutes, respectively. Hint: You may want to use modular arithmetic and integer division. Keep in mind that the data has not been cleaned and you need to check whether the extracted values are valid. Replace all the invalid values with `NaN`. The documentation for `pandas.Series.where` provided [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.where.html) should be helpful.

# In[4]:


def extract_hour(time):
    """
    Extracts hour information from military time.
    
    Args: 
        time (float64): series of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): series of input dimension with hour information.  
          Should only take on integer values in 0-23
    """
    # [YOUR CODE HERE] 
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    hour=pd.Series([], dtype='float64') #initialize empty series
    for t in time: #iterate through all items in time
        if(~np.isnan(t)): # if the value isn't already nan
            t = "%06.1f"%t #add padding 0s so that our substring method works for time like 630
            if(int(str(t)[0:2])>=0 and int(str(t)[0:2])<24): #if the first 2 digits are between 0 and 23 inclusive
                temp = pd.Series([float(str(t)[0:2])]) #create a temp series of just the hour digits
                hour = hour.append(temp, ignore_index=True) #append our temp series to hour, ignoring the index of temp
            else: # if the value of the first 2 digits is not between 0 and 23 inclusive
                temp = pd.Series([np.nan]) #create a temp series of nan
                hour = hour.append(temp, ignore_index=True) #append our temp series to hour, ignoring the index of temp
        else: #if the value is already nan
            temp = pd.Series([np.nan]) #create a temp series of nan
            hour = hour.append(temp, ignore_index=True) #append our temp series to hour, ignoring the index of temp
    return hour

# test your code to receive credit
test_ser = pd.Series([1030.0, 1259.0, np.nan, 2400], dtype='float64')
extract_hour(test_ser)

# 0    10.0
# 1    12.0
# 2     NaN
# 3     NaN
# dtype: float64


# In[5]:


def extract_mins(time):
    """
    Extracts minute information from military time
    
    Args: 
        time (float64): series of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): series of input dimension with minute information.  
          Should only take on integer values in 0-59
    """
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    mins=pd.Series([], dtype='float64') #initialize empty series
    for t in time: #iterate through all items in time
        if(~np.isnan(t)): # if the value isn't already nan
            t = "%06.1f"%t #add padding 0s so that our substring method works for time like 630
            if(int(str(t)[2:4])>=0 and int(str(t)[2:4])<60): #if the minutes digits are between 0 and 59 inclusive
                temp = pd.Series([float(str(t)[2:4])]) #create a temp series of just the hour digits
                mins = mins.append(temp, ignore_index=True) #append our temp series to mins, ignoring the index of temp
            else: # if the value of the minutes digits is not between between 0 and 59 inclusive
                temp = pd.Series([np.nan]) #create a temp series of nan
                mins = mins.append(temp, ignore_index=True) #append our temp series to mins, ignoring the index of temp
        else: #if the value is already nan
            temp = pd.Series([np.nan]) #create a temp series of nan
            mins = mins.append(temp, ignore_index=True) #append our temp series to mins, ignoring the index of temp
    return mins 


# test your code to receive credit
test_ser = pd.Series([1030.0, 1259.0, np.nan, 2475], dtype='float64')
extract_mins(test_ser)

# 0    30.0
# 1    59.0
# 2     NaN
# 3     NaN
# dtype: float64


# #### Question 1.2 **(20%)**
# 
# Using your two functions above, filter the `flights` data for flights that departed 20 or more minutes later than scheduled by comparing `sched_dep_time` and `actual_dep_time`.  You need not worry about flights that were delayed to the next day for this question.

# In[6]:


def convert_to_minofday(time):
    """
    Converts military time to minute of day
    
    Args:
        time (float64): series of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): series of input dimension with minute of day
    
    Example: 1:03pm is converted to 783.0
    """
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    hours = extract_hour(time) #extract the hours into a series
    mins = extract_mins(time) # extract the mins into a series
    minofday = pd.Series([], dtype='float64') #initialize an empty series to hold our result
    for i in range(len(hours)): #loop to iterate through both series
        temp = pd.Series((hours[i]*60)+mins[i]) #create a temp series with 1 value of our minutes of day calculation
        minofday = minofday.append(temp, ignore_index=True) #append temp to minofday, ignoring the index of temp
    return minofday 

# Test your code  to receive credit
ser = pd.Series([1303, 1200, 2400], dtype='float64')
convert_to_minofday(ser)

# 0    783.0
# 1    720.0
# 2      NaN
# dtype: float64


# In[7]:


def calc_time_diff(x, y):
    """
    Calculates delay times y - x
    
    Args:
        x (float64): series of scheduled time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
        y (float64): series of same dimensions giving actual time
    
    Returns:
        array (float64): series of input dimension with delay time
    """
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    schedmins = convert_to_minofday(x) #convert sched series to minutes of day
    actualmins = convert_to_minofday(y) # convert actual series to mins of day
    timediff=pd.Series([], dtype='float64') #initialize a new series for our result
    for i in range(len(schedmins)): #loop
        temp = pd.Series(actualmins[i]-schedmins[i]) #create temp series with our difference value
        timediff = timediff.append(temp, ignore_index=True) #append temp series to timediff, ignoring index of temp.
    return timediff
    
#Test your code  to receive credit
sched = pd.Series([1303, 1210], dtype='float64')
actual = pd.Series([1304, 1215], dtype='float64')
calc_time_diff(sched, actual)

# 0    1.0
# 1    5.0
# dtype: float64


# In[8]:


### Apply your functions here to calculate delay between `sched_dep_time` and `actual_dep_time` on flights, to receive credit.
# [YOUR CODE HERE]
# You MUST add comments explaining your thought process,
# and the resources you used to solve this question (if any)
delay = calc_time_diff(flights['sched_dep_time'],flights['actual_dep_time']) # Series object showing delay time
#passing the relevant columns from flights to our function
delay

# 0         -2.0
# 1         -7.0
# 2         -4.0
# 3         -4.0
# 4         -8.0
#          ...  
# 16856     56.0
# 16857     74.0
# 16858    196.0
# 16859    169.0
# 16860    137.0
# Length: 16861, dtype: float64


# #### Question 1.3 **(10%)**
# 
# Using your answer from question 1.2, find the full name of every destination city with a flight from SFO or OAK that was delayed by 60 or more minutes.  The airport codes used in `flights` are IATA codes.  Sort the cities alphabetically. Make sure you remove duplicates. (You may find `drop_duplicates` and `sort_values` helpful.)

# In[9]:


# Complete code here to receive credit.
# HINT: You will need to use `delayed20` and `airport` dataframes
# [YOUR CODE HERE]
# You MUST add comments explaining your thought process,
# and the resources you used to solve this question (if any)
citylist = ['SFO','OAK'] #create a list of origin cities to filter on
sfo_oak_flights = flights[flights.origin.isin(citylist)] #filter our dataframe
#add column for delay
sfo_oak_flights['delay'] = (calc_time_diff(sfo_oak_flights['sched_dep_time'],sfo_oak_flights['actual_dep_time']).values)
#remove fligts delayed by less than 60 minutes
sfo_oak_flights = sfo_oak_flights[sfo_oak_flights.delay>59]
delayed_destinations_iata = sfo_oak_flights[['destination']]#We only need destinations from this dataframe
delayed_destinations_iata = delayed_destinations_iata.drop_duplicates()#remove duplicates just in case
#merging and sorting 
delayed_airports = delayed_destinations_iata.merge(airports, left_on='destination',right_on='iata').sort_values(by=['city']) # Dataframe showing airports that satisfy above conditions
#removing duplicates and resetting the index
delayed_airports= delayed_airports.drop_duplicates(subset=['city']).reset_index()
#We only need cities in the output
delayed_destinations = delayed_airports['city'] # Unique and sorted destination cities
delayed_destinations

# 0     Albuquerque
# 1       Anchorage
# 2       Arcata CA
# 3           Aspen
# 4         Atlanta
#          ...     
# 65        Seattle
# 66        Spokane
# 67      St. Louis
# 68         Tucson
# 69     Washington
# Name: city, Length: 70, dtype: object


# ## Part 2: Web scraping and data collection (50%)

# ### Note and Setup

# Here, you will practice collecting and processing data in Python. By the end of this exercise hopefully you should look at the wonderful world wide web without fear, comforted by the fact that anything you can see with your human eyes, a computer can see with its computer eyes. In particular, we aim to give you some familiarity with:
# 
# * Using HTTP to fetch the content of a website
# * HTTP Requests (and lifecycle)
# * RESTful APIs
#     * Authentication (OAuth)
#     * Pagination
#     * Rate limiting
# * JSON vs. HTML (and how to parse each)
# * HTML traversal (CSS selectors)
# 
# Since everyone loves food (presumably), the ultimate end goal of this homework will be to acquire the data to answer some questions and hypotheses about the restaurant scene in Chicago (which we will get to later). We will download __both__ the metadata on restaurants in Chicago from the Yelp API and with this metadata, retrieve the comments/reviews and ratings from users on restaurants.
# 
# **Library Documentation:**
# 
# For solving this part, you need to look up online documentation for the Python packages you will use:
# 
# * Standard Library: 
#     * [io](https://docs.python.org/3/library/io.html)
#     * [time](https://docs.python.org/3/library/time.html)
#     * [json](https://docs.python.org/3/library/json.html)
# 
# * Third Party
#     * [requests](https://requests.readthedocs.io/en/latest/)
#     * [Beautiful Soup (version 4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
#     * [yelp-fusion](https://www.yelp.com/developers/documentation/v3/get_started)
# 
# **Note:** You may come across a `yelp-python` library online. The library is deprecated and incompatible with the current Yelp API, so do not use the library.

# First, import necessary libraries:

# In[10]:


import io, time, json
import requests
from bs4 import BeautifulSoup


# ### Authentication and working with APIs

# 
# 
# There are various authentication schemes that APIs use, listed here in relative order of complexity:
# 
# * No authentication
# * [HTTP basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)
# * Cookie based user login
# * OAuth (v1.0 & v2.0, see this [post](http://stackoverflow.com/questions/4113934/how-is-oauth-2-different-from-oauth-1) explaining the differences)
# * API keys
# * Custom Authentication
# 
# For the NYT example below (**Q2.1**), since it is a publicly visible page we did not need to authenticate. HTTP basic authentication isn't too common for consumer sites/applications that have the concept of user accounts (like Facebook, LinkedIn, Twitter, etc.) but is simple to setup quickly and you often encounter it on with individual password protected pages/sites. 
# 
# Cookie based user login is what the majority of services use when you login with a browser (i.e. username and password). Once you sign in to a service like Facebook, the response stores a cookie in your browser to remember that you have logged in (HTTP is stateless). Each subsequent request to the same domain (i.e. any page on `facebook.com`) also sends the cookie that contains the authentication information to remind Facebook's servers that you have already logged in.
# 
# Many REST APIs however use OAuth (authentication using tokens) which can be thought of a programmatic way to "login" _another_ user. Using tokens, a user (or application) only needs to send the login credentials once in the initial authentication and as a response from the server gets a special signed token. This signed token is then sent in future requests to the server (in place of the user credentials).
# 
# A similar concept common used by many APIs is to assign API Keys to each client that needs access to server resources. The client must then pass the API Key along with _every_ request it makes to the API to authenticate. This is because the server is typically relatively stateless and does not maintain a session between subsequent calls from the same client. Most APIs (including Yelp) allow you to pass the API Key via a special HTTP Header: `Authorization: Bearer <API_KEY>`. Check out the [docs](https://www.yelp.com/developers/documentation/v3/authentication) for more information.

# ### Question 2.1: Basic HTTP Requests w/o authentication **(5%)**

# First, let's do the "hello world" of making web requests with Python to get a sense for how to programmatically access web pages: an (unauthenticated) HTTP GET to download a web page.
# 
# Fill in the funtion to use `requests` to download and return the raw HTML content of the URL passed in as an argument. As an example try the following NYT article (on Youtube's algorithmic recommendation): [https://www.nytimes.com/2019/03/29/technology/youtube-online-extremism.html](https://www.nytimes.com/2019/03/29/technology/youtube-online-extremism.html)
# 
# Your function should return a tuple of: (`<status_code>`, `<text>`). (Hint: look at the **Library documentation** listed earlier to see how `requests` should work.) 

# In[11]:


def retrieve_html(url):
    """
    Return the raw HTML at the specified URL.

    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """

    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    r = requests.get(url)
    status_code = r.status_code
    text = r.text

    return status_code, text


# In[12]:


#  test your function here to receive credit
test = retrieve_html('https://martinheinz.dev/blog/31')
print(test)
#(200, '<!DOCTYPE html>\n<html  data-head-attrs="">\n\n<head >\n  <title>Scraping News and Articles From Public APIs with Python | Martin Heinz .....


# Now while this example might have been fun, we haven't yet done anything more than we could with a web browser. To really see the power of programmatically making web requests we will need to interact with an API. For the rest of this lab we will be working with the [Yelp API](https://www.yelp.com/developers/documentation/v3/get_started) and Yelp data (for an extensive data dump see their [Academic Dataset Challenge](https://www.yelp.com/dataset_challenge)). 

# ### Yelp API Access

# The reasons for using the Yelp API are 3 fold:
# 
# 1. Incredibly rich dataset that combines:
#     * entity data (users and businesses)
#     * preferences (i.e. ratings)
#     * geographic data (business location and check-ins)
#     * temporal data
#     * text in the form of reviews
#     * and even images.
# 2. Well [documented API](https://www.yelp.com/developers/documentation/v3/get_started) with thorough examples.
# 3. Extensive data coverage so that you can find data that you know personally (from your home town/city or account). This will help with understanding and interpreting your results.
# 
# Yelp used to use OAuth tokens but has now switched to API Keys. **For the sake of backwards compatibility Yelp still provides a Client ID and Secret for OAuth, but you will not need those for this assignment.** 
# 
# To access the Yelp API, we will need to go through a few more steps than we did with the first NYT example. Most large web scale companies use a combination of authentication and rate limiting to control access to their data to ensure that everyone using it abides. The first step (even before we make any request) is to setup a Yelp account if you do not have one and get API credentials.
# 
# 1. Create a [Yelp](https://www.yelp.com/login) account (if you do not have one already)
# 2. [Generate API keys](https://www.yelp.com/developers/v3/manage_app) (if you haven't already). You will only need the API Key (not the Client ID or Client Secret) -- more on that later.
# 
# Now that we have our accounts setup we can start making requests! 
# 

# ### Question 2.2: Authenticated HTTP Request with the Yelp API **(15%)**

# 
# 
# First, store your Yelp credentials in a local file (kept out of version control) which you can read in to authenticate with the API. This file can be any format/structure since you will fill in the function stub below.
# 
# For example, you may want to store your key in a file called `yelp_api_key.txt` (run in terminal):
# ```bash
# !echo 'YOUR_YELP_API_KEY' > yelp_api_key.txt
# ```
# 
# **KEEP THE API KEY FILE PRIVATE AND OUT OF VERSION CONTROL (and definitely do not submit them to Gradescope!)**
# 
# You can then read from the file using:

# In[13]:


with open('yelp_api_key.txt', 'r') as f:
    api_key = f.read().replace('\n','')
    print(api_key)
    # verify your api_key is correct
# DO NOT FORGET TO CLEAR THE OUTPUT TO KEEP YOUR API KEY PRIVATE


# In[14]:


def read_api_key(filepath):
    """
    Read the Yelp API Key from file.
    
    Args:
        filepath (string): File containing API Key
    Returns:
        api_key (string): The API Key
    """
    
    # feel free to modify this function if you are storing the API Key differently
    with open(filepath, 'r') as f:
        return f.read().replace('\n','')


# Using the Yelp API, fill in the following function stub to make an authenticated request to the [search](https://www.yelp.com/developers/documentation/v3/business_search) endpoint. Remember Yelp allows you to pass the API Key via a special HTTP Header: `Authorization: Bearer <API_KEY>`. Check out the [docs](https://www.yelp.com/developers/documentation/v3/authentication) for more information.

# In[15]:


def location_search_params(api_key, location, **kwargs):
    """
    Construct url, headers and url_params. Reference API docs (link above) to use the arguments
    """
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    # What is the url endpoint for search?
    url = 'https://api.yelp.com/v3/businesses/search' #the base url
    # How is Authentication performed?
    headers = {'Authorization':'Bearer '+api_key} #passing the api_key for authorization
    # SPACES in url is problematic. How should you handle location containing spaces?
    #adding all our other details in url_params
    url_params = {'location': location,'offset':kwargs.get('offset'),'limit':kwargs.get('limit')}
    # Include keyword arguments in url_params
    
    return url, headers, url_params


# Hint: `**kwargs` represent keyword arguments that are passed to the function. For example, if you called the function `location_search_params(api_key, location, offset=0, limit=50)`. The arguments `api_key` and `location` are called *positional arguments* and key-value pair arguments are called **keyword arguments**. Your `kwargs` variable will be a python dictionary with those keyword arguments.

# In[16]:


# Test your code here to receive credit.
api_key = "test_api_key_xyz"
location = "Chicago"
url, headers, url_params = location_search_params(api_key, location, offset=0, limit=50)
url, headers, url_params
# ('https://api.yelp.com/v3/businesses/search',
#  {'Authorization': 'Bearer test_api_key_xyz'},
#  {'location': 'Chicago', 'offset': 0, 'limit': 50})


# Now use `location_search_params(api_key, location, **kwargs)` to actually search restaurants from Yelp API. Most of the code is provided to you. Complete the `api_get_request` function given below. 

# In[17]:


def api_get_request(url, headers, url_params):
    """
    Send a HTTP GET request and return a json response 
    
    Args:
        url (string): API endpoint url
        headers (dict): A python dictionary containing HTTP headers including Authentication to be sent
        url_params (dict): The parameters (required and optional) supported by endpoint
        
    Returns:
        results (json): response as json
    """
    http_method = 'GET'
    # See requests.request?
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    response = requests.request(http_method,url,headers=headers,params=url_params)#creating the request to send
    return response.json()
    

def yelp_search(api_key, location, offset=0):
    """
    Make an authenticated request to the Yelp API.

    Args:
        api_key (string): Your Yelp API Key for Authentication
        location (string): Business Location
        offset (int): param for pagination

    Returns:
        total (integer): total number of businesses on Yelp corresponding to the location
        businesses (list): list of dicts representing each business
    """
    url, headers, url_params = location_search_params(api_key, location, offset=0)
    response_json = api_get_request(url, headers, url_params)
    return response_json["total"], list(response_json["businesses"])

# test your code here to receive credit
# [YOUR CODE HERE]
# You MUST add comments explaining your thought process,
# and the resources you used to solve this question (if any)
api_key = read_api_key('C:/Users/utsav/OneDrive/UIC/Spring 2023/CS 418/Lab 2/yelp_api_key.txt')
num_records, data = yelp_search(api_key, 'Chicago')
print(num_records)
#7700
print(len(data))
#20
print(list(map(lambda x: x['name'], data)))
#['Girl & The Goat', 'Wildberry Pancakes and Cafe', 'Au Cheval', 'The Purple Pig', 'Art Institute of Chicago', "Lou Malnati's Pizzeria" .....


# ### Parameterization and Pagination

# Now that we have completed the "hello world" of working with the Yelp API, we are ready to really fly! The rest of the exercise will have a bit less direction since there are a variety of ways to retrieve the requested information but you should have all the component knowledge at this point to work with the API. Yelp being a fairly general platform actually has many more business than just restaurants, but by using the flexibility of the API we can ask it to only return the restaurants.
# 
# 
# 
# And before we can get any reviews on restaurants, we need to actually get the metadata on ALL of the restaurants in Chicago. Notice above that while Yelp told us that there are ~240, the response contained fewer actual `Business` objects. This is due to pagination and is a safeguard against returning __TOO__ much data in a single request (what would happen if there were 100,000 restaurants?) and can be used in conjuction with _rate limiting_ as well as a way to throttle and protect access to Yelp data.
# 
# > As a thought exercise, consider: If an API has 1,000,000 records, but only returns 10 records per page and limits you to 5 requests per second... how long will it take to acquire ALL of the records contained in the API?
# 
# One of the ways that APIs are an improvement over plain web scraping is the ability to make __parameterized__ requests. Just like the Python functions you have been writing have arguments (or parameters) that allow you to customize its behavior/actions (an output) without having to rewrite the function entirely, we can parameterize the queries we make to the Yelp API to filter the results it returns.

# ### Question 2.3: Acquire all of the restaurants in Chicago on Yelp **(10%)**

# 
# 
# Again using the [API documentation](https://www.yelp.com/developers/documentation/v3/business_search) for the `search` endpoint, fill in the following function to retrieve all of the _Restuarants_ (using categories) for a given query. Again you should use your `read_api_key()` function outside of the `all_restaurants()` stub to read the API Key used for the requests. You will need to account for __pagination__ and __[rate limiting](https://www.yelp.com/developers/faq)__ to:
# 
# 1. Retrieve all of the Business objects (# of business objects should equal `total` in the response). **Paginate by querying 10 restaurants each request.**
# 2. Pause slightly (at least 200 milliseconds) between subsequent requests so as to not overwhelm the API (and get blocked).  
# 
# As always with API access, make sure you follow all of the [API's policies](https://www.yelp.com/developers/api_terms) and use the API responsibly and respectfully.
# 
# **DO NOT MAKE TOO MANY REQUESTS TOO QUICKLY OR YOUR KEY MAY BE BLOCKED**

# In[18]:


import math 

def paginated_restaurant_search_requests(api_key, location, total):
    """
    Returns a list of tuples (url, headers, url_params) for paginated search of all restaurants
    Args:
        api_key (string): Your Yelp API Key for Authentication
        location (string): Business Location
        total (int): Total number of items to be fetched
    Returns:
        results (list): list of tuple (url, headers, url_params)
    """
    # HINT: Use total, offset and limit for pagination
    # You can reuse function location_search_params(...)
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    limit = 10
    offset = 0 #initial offset
    results = [] #creating a list for results
    counter = total #initial value to track how many requests to send
    while counter>0: #loop
        #fetch our url details
        url, headers, url_params = location_search_params(api_key, location, offset=offset, limit=10)
        #add category to the request
        category = {'category': 'restaurants'}
        url_params.update(category)
        #combine our variables into one request
        new_url = [(url,headers,url_params)]
        #adding the new url to the list
        results = results + new_url
        #updating the offset
        offset = offset+limit
        #update the counter
        counter = counter - limit
    return results


# Test your code here to receive credit.
api_key = read_api_key('C:/Users/utsav/OneDrive/UIC/Spring 2023/CS 418/Lab 2/yelp_api_key.txt')
location = "Chicago"
all_restaurants_requests = paginated_restaurant_search_requests(api_key, location, 15)
all_restaurants_requests

# [('https://api.yelp.com/v3/businesses/search',
#   {'Authorization': 'Bearer test_api_key_xyz'},
#   {'location': 'Chicago',
#    'offset': 0,
#    'limit': 10,
#    'categories': 'restaurants'}),
#  ('https://api.yelp.com/v3/businesses/search',
#   {'Authorization': 'Bearer test_api_key_xyz'},
#   {'location': 'Chicago',
#    'offset': 10,
#    'limit': 10,
#    'categories': 'restaurants'})]


# In[19]:


from time import sleep
def all_restaurants(api_key, location):
    """
    Construct the pagination requests for ALL the restaurants on Yelp for a given location.

    Args:
        api_key (string): Your Yelp API Key for Authentication
        location (string): Business Location

    Returns:
        results (list): list of dicts representing each restaurant
    """
    # What keyword arguments should you pass to get first page of restaurants in Yelp
    url, headers, url_params = location_search_params(api_key, location, offset=0, limit=10)
    # 
    response_json = api_get_request(url, headers, url_params)
    total_items = response_json["total"]
    all_restaurants_request = paginated_restaurant_search_requests(api_key, location, total_items)
    
    # Use returned list of (url, headers, url_params) and function api_get_request to retrive all restaurants
    # REMEMBER to pause slightly after each request.
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    results=[] #initialise results
    for i in all_restaurants_request: #loop
        response_json = api_get_request(i[0], i[1], i[2]) #passing the request to api_get_request
        results = results + response_json['businesses'] #adding the response to our results
        time.sleep(0.2) #sleep to not flood API with requests
    return results


# You can test your function with an individual neighborhood in Chicago (for example, Greektown). Chicago itself has a lot of restaurants... meaning it will take a lot of time to download them all.

# In[20]:


# test your function here to receive credit.
api_key = read_api_key('yelp_api_key.txt')
data = all_restaurants(api_key, 'Greektown, Chicago, IL')
print(len(data))
# 94
print(list(map(lambda x:x['name'], data)))
#['Greek Islands Restaurant', 'Artopolis', 'Meli Cafe & Juice Bar', 'Athena Greek Restaurant', 'WJ Noodles', .....]


# Now that we have the metadata on all of the restaurants in Greektown (or at least the ones listed on Yelp), we can retrieve the reviews and ratings. The Yelp API gives us aggregate information on ratings but it doesn't give us the review text or individual users' ratings for a restaurant. For that we need to turn to web scraping, but to find out what pages to scrape we first need to parse our JSON from the API to extract the URLs of the restaurants.
# 
# In general, it is a best practice to separate the act of __downloading__ data and __parsing__ data. This ensures that your data processing pipeline is modular and extensible (and autogradable ;). This decoupling also solves the problem of expensive downloading but cheap parsing (in terms of computation and time).

# 
# ### Question 2.4: Parse the API Responses and Extract the URLs **(5%)**

# 
# 
# 
# Because we want to separate the __downloading__ from the __parsing__, fill in the following function to parse the URLs pointing to the restaurants on `yelp.com`. As input your function should expect a string of [properly formatted JSON](http://www.json.org/) (which is similar to __BUT__ not the same as a Python dictionary) and as output should return a Python list of strings. Hint: print your `data` to see the JSON-formatted information you have. The input JSON will be structured as follows (same as the [sample](https://www.yelp.com/developers/documentation/v3/business_search) on the Yelp API page):
# 
# ```json
# {
#   "total": 8228,
#   "businesses": [
#     {
#       "rating": 4,
#       "price": "$",
#       "phone": "+14152520800",
#       "id": "four-barrel-coffee-san-francisco",
#       "is_closed": false,
#       "categories": [
#         {
#           "alias": "coffee",
#           "title": "Coffee & Tea"
#         }
#       ],
#       "review_count": 1738,
#       "name": "Four Barrel Coffee",
#       "url": "https://www.yelp.com/biz/four-barrel-coffee-san-francisco",
#       "coordinates": {
#         "latitude": 37.7670169511878,
#         "longitude": -122.42184275
#       },
#       "image_url": "http://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg",
#       "location": {
#         "city": "San Francisco",
#         "country": "US",
#         "address2": "",
#         "address3": "",
#         "state": "CA",
#         "address1": "375 Valencia St",
#         "zip_code": "94103"
#       },
#       "distance": 1604.23,
#       "transactions": ["pickup", "delivery"]
#     }
#   ],
#   "region": {
#     "center": {
#       "latitude": 37.767413217936834,
#       "longitude": -122.42820739746094
#     }
#   }
# }
# ```

# In[21]:


def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    results=[] #initializing results list
    for d in data['businesses']:
        results.append(d['url']) #fetching the url details and adding it to our results
    return results
    
# test your code here to receive credit 
url, headers, url_params = location_search_params(api_key, "Bridgeport, Chicago, IL", offset=0)
response_text = api_get_request(url, headers, url_params)
parse_api_response(response_text)
# ['https://www.yelp.com/biz/nana-chicago?adjust_creative=RYmY_QnZRP74oo4eNQbazg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=RYmY_QnZRP74oo4eNQbazg',
#  'https://www.yelp.com/biz/jackalope-coffee-and-tea-house-chicago?adjust_creative=RYmY_QnZRP74oo4eNQbazg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=RYmY_QnZRP74oo4eNQbazg',
#  .....
# ]


# As we can see, JSON is quite trivial to parse (which is not the case with HTML as we will see in a second) and work with programmatically. This is why it is one of the most ubiquitous data serialization formats (especially for ReSTful APIs) and a huge benefit of working with a well defined API if one exists. But APIs do not always exists or provide the data we might need, and as a last resort we can always scrape web pages...

# ### Working with Web Pages (and HTML)

# Think of APIs as similar to accessing an application's database itself (something you can interactively query and receive structured data back). But the results are usually in a somewhat raw form with no formatting or visual representation (like the results from a database query). This is a benefit _AND_ a drawback depending on the end use case. For data science and _programatic_ analysis this raw form is quite ideal, but for an end user requesting information from a _graphical interface_ (like a web browser) this is very far from ideal since it takes some cognitive overhead to interpret the raw information. And vice versa, if we have HTML it is quite easy for a human to visually interpret it, but to try to perform some type of programmatic analysis we first need to parse the HTML into a more structured form.
# 
# > As a general rule of thumb, if the data you need can be accessed or retrieved in a structured form (either from a bulk download or API) prefer that first. But if the data you want (and need) is not as in our case we need to resort to alternative (messier) means.
# 
# Going back to the "hello world" example of question 2.1 with the NYT, we will do something similar to retrieve the HTML of the Yelp site itself (rather than going through the API programmatically) as text. 
# > However, we will use saved HTML pages to reduce excessive traffic to the Yelp website.

# ### Question 2.5: Parse a Yelp restaurant Page **(10%)**

# Using `BeautifulSoup`, parse the HTML of a single Yelp restaurant page to extract the reviews in a structured form as well as the URL to the next page of reviews (or `None` if it is the last page). Fill in following function stubs to parse a single page of reviews and return:
# * the reviews as a structured Python dictionary
# * the HTML element containing the link/url for the next page of reviews (or None).
# 
# For each review be sure to structure your Python dictionary as follows (to be graded correctly). The order of the keys doesn't matter, only the keys and the data type of the values:
# 
# ```python
# {
#     'author': str
#     'rating': float
#     'date': str ('yyyy-mm-dd')
#     'description': str
# }
# 
# {
#     'author': 'Topsy Kretts'
#     'rating': 4.7
#     'date': '2016-01-23'
#     'description': "Wonderful!"
# }
# ```
# 
# There can be issues with Beautiful Soup using various parsers, for maximum compatibility (and fewest errors) initialize the library with the default (and Python standard library parser): `BeautifulSoup(markup, "html.parser")`.
# 
# Most of the function has been provided to you:

# In[22]:


url_lookup = {
"https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=225":"parse_page_test1.html",
"https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=245":"parse_page_test2.html"
}

def html_fetcher(url):
    """
    Return the raw HTML at the specified URL.
    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    html_file = url_lookup.get(url)
    with open(html_file, 'rb') as file:
        html_text = file.read()
        return 200, html_text


def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.
    
    Args:
        html (string): String of HTML corresponding to a Yelp restaurant

    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """
    soup = BeautifulSoup(html,'html.parser')
    url_next = soup.find('link',rel='next')
    if url_next:
        url_next = url_next.get('href')
    else:
        url_next = None

    reviews = soup.find_all('div', itemprop="review")
    reviews_list = []
    # HINT: print reviews to see what http tag to extract
    # [YOUR CODE HERE]
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    #print(reviews)
    #print(soup.find_all('meta', itemprop="author"))
    divs = soup.find_all('div', itemprop='review')
    #print(divs)
    #authors = div.find_all('meta', itemprop="author")
    #ratings = soup.find_all('meta', itemprop="ratingValue")
    #dates = soup.find_all('meta', itemprop="datePublished")
    #description = soup.find_all('p', itemprop="description")
    for i in divs:
        authors = i.find('meta', itemprop="author")
        #print(authors['content'])
        ratings = i.find('meta', itemprop="ratingValue")
        dates = i.find('meta', itemprop="datePublished")
        description = i.find('p', itemprop="description")
        #print(authors.get_text())
        #print(authors['content'],ratings['content'],dates['content'],description.get_text())
        temp = {'author':authors['content'],'rating':ratings['content'],'date':dates['content'],'description':description.get_text()}
        reviews_list.append(temp)
    #print(reviews_list)
    return reviews_list, url_next

# Test your implementation here to receive credit.
code, html = html_fetcher("https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=225")
reviews_list, url_next = parse_page(html)
print(len(reviews_list)) # 20
print(url_next) #https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=245


# ### Question 2.6: Extract all Yelp reviews for a Single Restaurant **(5%)**

# 
# 
# So now that we have parsed a single page, and figured out a method to go from one page to the next we are ready to combine these two techniques and actually crawl through web pages! 
# 
# Using the provided `html_fetcher` (for a real use-case you would use `requests`), programmatically retrieve __ALL__ of the reviews for a __single__ restaurant (provided as a parameter). Just like the API was paginated, the HTML paginates its reviews (it would be a very long web page to show 300 reviews on a single page) and to get all the reviews you will need to parse and traverse the HTML. As input your function will receive a URL corresponding to a Yelp restaurant. As output return a list of dictionaries (structured the same as question 2.5) containing the relevant information from the reviews. You can use `parse_page()` here.

# In[23]:


def extract_reviews(url, html_fetcher):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.
        html_fetcher (function): A function that takes url and returns html status code and content
    
    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """
    reviews = []
    # [YOUR CODE HERE]
    # HINT: Use function `parse_page(html)` multiple times until no next page exists
    # You MUST add comments explaining your thought process,
    # and the resources you used to solve this question (if any)
    code, html = html_fetcher(url)
    reviews_list, url_next = parse_page(html)
    reviews = reviews + reviews_list
    while(url_next):
        code, html = html_fetcher(url_next)
        reviews_list, url_next_2 = parse_page(html)
        url_next=url_next_2
        reviews = reviews + reviews_list
    return reviews


# You can test your function with this code:

# In[24]:


# test your function here to receive credit.
data = extract_reviews('https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=225', html_fetcher=html_fetcher)
print(len(data))
# 35
print(data[0])
# {'author': 'Jason S.', 'rating': 5.0, 'date': '2016-05-02', 'description': "This was one of my favorite food trucks ..."}


# ## Submission
# 
# You're almost done! 
# 
# After executing all commands and completing this notebook, download your Python Notebook (.IPYNB file) and Python file (.PY file) upload it to Gradescope under *Lab 2*. Make sure you check that your **ipynb** file includes all parts of your solution **(including the outputs)**.
