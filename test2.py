# load the library
from bs4 import BeautifulSoup as Soup
import urllib.request
import requests, re, pandas as pd

# indeed.com url
base_url = 'http://www.indeed.ca/jobs?q=software+engineer&jt=fulltime&sort='
sort_by = 'date'          # sort by data
start_from = '&start='    # start page number

pd.set_option('max_colwidth',5000)    # to remove column limit (Otherwise, we'll lose some info)
df = pd.DataFrame()   # create a new data frame
df_received = df
print ('hello2'+df_received)
for i in range(0,len(df_received)):  # get all the company details (
    target_comp_name = df_received.iloc[i]['comp_name']

    url_2nd = df.iloc[i]['overall_link'] 
    if url_2nd != None:
        target_2nd = Soup(urllib.request.urlopen(url_2nd), "lxml")
        
        comp_logo = target_2nd.find("div", {"id": "cmp-header-logo"}).find('img')
        if comp_logo != None:
            comp_logo = target_2nd.find("div", {"id": "cmp-header-logo"}).find('img').attrs['src']
        else: comp_logo = None
          
        # total 6 ratings: overall rating, work-life balance rating, compensation / benefit rating, job security rating, management rating, company culture rating
        comp_rating_overall = target_2nd.find("span", {"class": "cmp-star-large-on"}).attrs['style']
        wl_bal_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[0].attrs['style'] 
        benefit_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[1].attrs['style'] 
        jsecurity_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[2].attrs['style'] 
        mgmt_rating =  target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[3].attrs['style'] 
        culture_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[4].attrs['style'] 

        # Some regular expression stuffs to remove unnecessary characters
        comp_rating_overall = re.sub('[width: ]', '', comp_rating_overall)
        comp_rating_overall = re.sub('[px;]', '', comp_rating_overall)
        comp_rating_overall = round((float(comp_rating_overall)*5.0)/120, 1)

        wl_bal_rating = re.sub('[width: ]', '', wl_bal_rating)
        wl_bal_rating = re.sub('[px]', '', wl_bal_rating)
        wl_bal_rating = round((float(wl_bal_rating)*5.0)/86, 1) # 86 pixel

        benefit_rating = re.sub('[width: ]', '', benefit_rating)
        benefit_rating = re.sub('[px]', '', benefit_rating)
        benefit_rating = round((float(benefit_rating)*5.0)/86, 1)

        jsecurity_rating = re.sub('[width: ]', '', jsecurity_rating)
        jsecurity_rating = re.sub('[px]', '', jsecurity_rating)
        jsecurity_rating = round((float(jsecurity_rating)*5.0)/86, 1)

        mgmt_rating = re.sub('[width: ]', '', mgmt_rating)
        mgmt_rating = re.sub('[px]', '', mgmt_rating)
        mgmt_rating = round((float(mgmt_rating)*5.0)/86, 1)

        culture_rating = re.sub('[width: ]', '', culture_rating)
        culture_rating = re.sub('[px]', '', culture_rating)
        culture_rating = round((float(culture_rating)*5.0)/86, 1)
    
        # Store cleaned characters into data frame
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'overall_rating'] = comp_rating_overall
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'wl_bal_rating'] = wl_bal_rating
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'benefit_rating'] = benefit_rating
       # df_received.loc[ df_received['comp_name'] == target_comp_name, 'jsecurity_rating'] = security_rating
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'mgmt_rating'] = mgmt_rating
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'culture_rating'] = culture_rating

print ('hello3')

for i in range(0,len(df_received)):  # get all the company details (
    target_comp_name = df_received.iloc[i]['comp_name']

    url_2nd = df.iloc[i]['overall_link'] 
    if url_2nd != None:
        target_2nd = Soup(urllib.request.urlopen(url_2nd), "lxml")
        
        comp_logo = target_2nd.find("div", {"id": "cmp-header-logo"}).find('img')
        if comp_logo != None:
            comp_logo = target_2nd.find("div", {"id": "cmp-header-logo"}).find('img').attrs['src']
        else: comp_logo = None
          
        # total 6 ratings: overall rating, work-life balance rating, compensation / benefit rating, job security rating, management rating, company culture rating
        comp_rating_overall = target_2nd.find("span", {"class": "cmp-star-large-on"}).attrs['style']
        wl_bal_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[0].attrs['style'] 
        benefit_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[1].attrs['style'] 
        jsecurity_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[2].attrs['style'] 
        mgmt_rating =  target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[3].attrs['style'] 
        culture_rating = target_2nd.find("dl", {"id": "cmp-reviews-attributes"}).find_all("span", {"class": "cmp-star-on"})[4].attrs['style'] 

        # Some regular expression stuffs to remove unnecessary characters
        comp_rating_overall = re.sub('[width: ]', '', comp_rating_overall)
        comp_rating_overall = re.sub('[px;]', '', comp_rating_overall)
        comp_rating_overall = round((float(comp_rating_overall)*5.0)/120, 1)

        wl_bal_rating = re.sub('[width: ]', '', wl_bal_rating)
        wl_bal_rating = re.sub('[px]', '', wl_bal_rating)
        wl_bal_rating = round((float(wl_bal_rating)*5.0)/86, 1) # 86 pixel

        benefit_rating = re.sub('[width: ]', '', benefit_rating)
        benefit_rating = re.sub('[px]', '', benefit_rating)
        benefit_rating = round((float(benefit_rating)*5.0)/86, 1)

        jsecurity_rating = re.sub('[width: ]', '', jsecurity_rating)
        jsecurity_rating = re.sub('[px]', '', jsecurity_rating)
        jsecurity_rating = round((float(jsecurity_rating)*5.0)/86, 1)

        mgmt_rating = re.sub('[width: ]', '', mgmt_rating)
        mgmt_rating = re.sub('[px]', '', mgmt_rating)
        mgmt_rating = round((float(mgmt_rating)*5.0)/86, 1)

        culture_rating = re.sub('[width: ]', '', culture_rating)
        culture_rating = re.sub('[px]', '', culture_rating)
        culture_rating = round((float(culture_rating)*5.0)/86, 1)
    
        # Store cleaned characters into data frame
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'overall_rating'] = comp_rating_overall
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'wl_bal_rating'] = wl_bal_rating
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'benefit_rating'] = benefit_rating
        #df_received.loc[ df_received['comp_name'] == target_comp_name, 'jsecurity_rating'] = security_rating
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'mgmt_rating'] = mgmt_rating
        df_received.loc[ df_received['comp_name'] == target_comp_name, 'culture_rating'] = culture_rating
print ('hello1')
# Save the result to CSV
df_received.to_csv('C:/Users/Rajwinder/Desktop/indeed_companies.csv', encoding='utf-8')
print ('hello')