import pandas as pd
from verispy import VERIS
class DataCollector:
    def __init__(self):
        self.data_dir = "./validated/" #replace with your own path for data 
        self.v = VERIS(json_dir = self.data_dir)
        self.veris_df = self.v.json_to_df(verbose=True)
    def getCountries(self):
        """
        collected data:
             US = 70.3001
             GB = 54.3333
             CA = 66.159
             AU = 54.888
             IN = 2
             NZ = 23.5
             IE = 75.9
             JP = 40
             CN = 70.4286
             DE = 127.4286
        """
        countries = ['US', 'GB', 'CA', 'AU', 'IN', 'NZ', 'IE', 'JP', 'CN', 'DE']
        for country in countries:
            country = self.veris_df.loc[self.veris_df[f'victim.country.{country}']]
            self.getDuration(country)
            #used in the further analysis
            self.getColumnStats(country, "action")
            self.getColumnStats(country, "victim.employee_count")
            self.getColumnStats(country, "victim.industry2")
        
    def getColumnStats(self, frame, column):
        print(self.v.enum_summary(frame, column))

    def getIndustries(self):
        RT, RT1 = "44", "45" # Retail services 
        FS = "52" # Finance services 
        IS = "51" # Information Services 
        ED = "61" # Education 
        HCSS = "62" # Healthcare and social services 

        retail = self.veris_df.loc[self.veris_df[f'victim.industry2.{RT}']]
        retail1 = self.veris_df.loc[self.veris_df[f'victim.industry2.{RT1}']]
        #we need to merge 44 and 45 because they are both retail
        frame = [retail, retail1]
        retail_trade = pd.concat(frame)
        information = self.veris_df.loc[self.veris_df[f'victim.industry2.{IS}']]
        finance = self.veris_df.loc[self.veris_df[f'victim.industry2.{FS}']]
        education = self.veris_df.loc[self.veris_df[f'victim.industry2.{ED}']]
        healthcare = self.veris_df.loc[self.veris_df[f'victim.industry2.{HCSS}']]
        #set whatever industry you want to get the duration for there
        self.getDuration(retail_trade)
        self.getDuration(information)
        self.getDuration(finance)
        self.getDuration(education)
        self.getDuration(healthcare)

    def getRevenue(self):
        #get the information about the revenue
        #self.getColumnStats(self.veris_df, "victim.revenue")
        indices = self.veris_df["victim.revenue.amount"].dropna().index
        newFrame = self.veris_df.loc[indices].copy()
        #less than 10million  
        category1 = []
        #10 million but less then a billion
        category2 = []
        #more than a billion
        category3 = []

        for index in indices:
            amount = self.veris_df._get_value(index, "victim.revenue.amount")
            if amount < 10000000:
                category1.append(index)
            elif amount < 1000000000:
                category2.append(index)
            else:
                category3.append(index)
            
        small_revenue = self.veris_df.iloc[category1]
        medium_revenue = self.veris_df.iloc[category2]
        large_revenue = self.veris_df.iloc[category3]
        #set whatever revenue size you want to get the duration from 
        self.getDuration(small_revenue)
        self.getDuration(medium_revenue)
        self.getDuration(large_revenue)

    def getOrgSize(self):
        #used this command to the see all the different sizes
        #self.getColumnStats(self.veris_df, 'victim')
        sizes = []
        #gets all the different sizes of organisation
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.1 to 10']])
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.11 to 100']])
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.101 to 1000']])
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.1001 to 10000']])
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.10001 to 25000']])
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.25001 to 50000']])
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.50001 to 100000']])
        sizes.append(self.veris_df.loc[self.veris_df['victim.employee_count.Over 100000']])

        for size in sizes:
            #set whatever company size you want to get the duration from 
            self.getDuration(size)
            #get the column statistic of some organisation size
            self.getColumnStats(size, "action")

    def getDuration(self, frame):
        #calculates and prints out the duration of a frame
        hours = frame.loc[self.veris_df['timeline.discovery.unit.Hours']]
        sumHours = hours[['timeline.discovery.value']].sum()
        numHours = hours[['timeline.discovery.value']].shape[0]

        days = frame.loc[self.veris_df['timeline.discovery.unit.Days']]
        sumDays = days[['timeline.discovery.value']].sum()
        numDays = days[['timeline.discovery.value']].shape[0]

        weeks = frame.loc[self.veris_df['timeline.discovery.unit.Weeks']]
        sumWeeks = weeks[['timeline.discovery.value']].sum()
        numWeeks = weeks[['timeline.discovery.value']].shape[0]

        months = frame.loc[self.veris_df['timeline.discovery.unit.Months']]
        sumMonths = months[['timeline.discovery.value']].sum()
        numMonths = months[['timeline.discovery.value']].shape[0]
        
        # For the sake of analysis, all Months are 30 days
        totalMonths = sumMonths * 30 * 24 
        totalWeeks = sumWeeks * 7 * 24
        totalDays = sumDays * 24
        totalHours = totalMonths + totalWeeks + totalDays + sumHours
        totalInstances = numMonths + numWeeks + numDays + numHours
        actualAverage = (totalHours / totalInstances) / 24

        print("Total Hours ", totalHours)
        print("Total Instances ", totalInstances)
        print("Average Discovery Time (Days) ", actualAverage)

