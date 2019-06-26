#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[17]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
schools = "Resources/schools_complete.csv"
students = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames

#read the csv
schools_df = pd.read_csv(schools)
students_df = pd.read_csv(students)
students_df.head()
schools_df


# In[28]:


#merge df
renamed = schools_df.rename(columns={"name":"school_name"})
merged = pd.merge(renamed, students_df, on="school_name")
merged


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[36]:


#Calculate the total number of schools
total_schools = schools_df["School ID"].count()
total_schools


# In[37]:


#Calculate the total number of students
total_students = students_df["Student ID"].count()
total_students


# In[38]:


#Calculate the total budget
total_budget = schools_df["budget"].sum()
total_budget


# In[59]:


#Calculate budget per student
budget_per_student = (total_budget / total_students)
budget_per_student


# In[39]:


#Calculate the average math score
average_math = students_df['math_score'].mean()
average_math


# In[40]:


#Calculate the average reading score
average_reading = students_df['reading_score'].mean()
average_reading


# In[41]:


#Math Passing Rate
pass_math = (students_df['math_score']>=70).sum()/total_students
pass_math*100


# In[42]:


#Reading Passing Rate
pass_reading = (students_df['reading_score']>=70).sum()/total_students
pass_reading*100


# In[45]:


#Calculate the overall passing rate
pass_overall = (pass_math+pass_reading)/2
pass_overall*100


# In[46]:


district_overview_df = pd.DataFrame({
    "Total Schools":[total_schools],
    "Total Budget":[total_budget],
    "Total Students":[total_students],
    "Avg Math Score":[average_math],
    "Avg Reading Score":[average_reading],
    "Percentage Passing Math":[pass_math],
    "Percentage Passing Reading":[pass_reading],
    "Percentage Passing Overall":[pass_overall]
})
district_overview_df


# ## School Summary

# In[60]:


school = schools_df["school_name"]
school_type = schools_df["type"]
students = schools_df["size"]
budget = schools_df["budget"]
budget_student = schools_df["budget_per_student"]
math_average = merged.groupby(["school_name"])["math_score"].mean()
reading_average = merged.groupby(["school_name"])["reading_score"].mean()
math_passing = merged[students_df.math_score>=70].groupby('school_name')['math_score'].count()/merged.groupby(["school_name"])["Student ID"].count()
math_passing = math_passing *100
reading_passing = merged[students_df.reading_score>=70].groupby('school_name')['reading_score'].count()/merged.groupby(["school_name"])["Student ID"].count()
reading_passing = reading_passing*100
overall_passing = (math_passing + reading_passing)/2


# In[89]:


school_overview1_df = pd.DataFrame({
    "School_name":school_name,
    "School Type":school_type,
    "Total Students":students,
    "Total Budget":total_budget,
    "Budget Per School":budget,
})


# In[92]:


school_overview2_df = pd.DataFrame({
    "Budget Per Student":budget_per_student,
    "Avg Math Score":math_average,
    "Avg Reading Score":reading_average,
    "Percentage Passing Math":math_passing,
    "Percentage Passing Reading":reading_passing,
    "Percentage Passing Overall":overall_passing
})


# In[93]:


#merge overview table for School Summary
school_overview = school_overview1_df.join(school_overview2_df,on='School_name',how='inner')
school_overview


# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[95]:


top5_df = school_overview.sort_values("Percentage Passing Overall", ascending=False)
top5_df = top5_df.head()
top5_df


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[96]:


bottom5_df = school_overview.sort_values("Percentage Passing Overall", ascending=True)
bottom5_df = bottom5_df.head()
bottom5_df


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[98]:


ninth = merged[(merged["grade"] == "9th")]
tenth = merged[(merged["grade"] == "10th")]
eleventh = merged[(merged["grade"] == "11th")]
twelfth = merged[(merged["grade"] == "12th")]

ninth_math = ninth.groupby("school_name")["math_score"].mean()
tenth_math = tenth.groupby("school_name")["math_score"].mean()
eleventh_math = eleventh.groupby("school_name")["math_score"].mean()
twelfth_math = twelfth.groupby("school_name")["math_score"].mean()

mathscores=pd.DataFrame({
    "9th":ninth_math,
    "10th":tenth_math,
    "11th":eleventh_math,
    "12th":twelfth_math
})
mathscores


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[100]:



nineth_read = ninth.groupby("school_name")["reading_score"].mean()
tenth_read = tenth.groupby("school_name")["reading_score"].mean()
eleventh_read = eleventh.groupby("school_name")["reading_score"].mean()
twelfth_read = twelfth.groupby("school_name")["reading_score"].mean()

readingscores=pd.DataFrame({
    "9th":nineth_read,
    "10th":tenth_read,
    "11th":eleventh_read,
    "12th":twelfth_read
})
readingscores


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[107]:


# Sample bins. Feel free to create your own bins.
budget_per_student = budget/students
bins = [0, 585, 615, 645, 675]
labels = ["<$585", "$585-615", "$615-645", "$645-675"]
school_overview["Spending Ranges"] = pd.cut(budget_per_student,bins,labels=labels)

spendingmath = school_overview.groupby("Spending Ranges").mean()["Avg Math Score"]
spendingreading = school_overview.groupby("Spending Ranges").mean()["Avg Reading Score"]
spendingmathpass = school_overview.groupby("Spending Ranges").mean()["Percentage Passing Math"]
spendingreadpass = school_overview.groupby("Spending Ranges").mean()["Percentage Passing Reading"]
spendingoverallpass = (spendingmath+spendingreading)/2

spending_summary = pd.DataFrame({
    "Average Math Score":spendingmath,
    "Average Reading Score":spendingreading,
    "Passing Math":spendingmathpass,
    "Passing Reading":spendingreadpass,
    "Passing Overall":spendingoverallpass
})
spending_summary


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[108]:


size_bins = [0,1000,2000,5000]
size_labels = ["Small <1000","Medium 2000-5000","Large >5000"]
school_overview["Size Type"]=pd.cut(students,size_bins,labels=size_labels)

sizemath = school_overview.groupby("Size Type").mean()["Avg Math Score"]
sizeread = school_overview.groupby("Size Type").mean()["Avg Reading Score"]
sizemathpass = school_overview.groupby("Size Type").mean()["Percentage Passing Math"]
sizereadpass = school_overview.groupby("Size Type").mean()["Percentage Passing Reading"]
sizeoverallpass = (sizemathpass+sizereadpass)/2

size_summary = pd.DataFrame({
    "Average Math Score":sizemath,
    "Average Reading Score":sizeread,
    "Passing Math":sizemathpass,
    "Passing Reading":sizereadpass,
    "Passing Overall":sizeoverallpass
})
size_summary


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[20]:


schooltype_bins = [0,1000,2000,5000]
schooltype_labels = ["Small <1000","Medium 2000-5000","Large >5000"]
school_overview["Size Type"]=pd.cut(students,size_bins,labels=size_labels)

sizemath = school_overview.groupby("Size Type").mean()["Avg Math Score"]
sizeread = school_overview.groupby("Size Type").mean()["Avg Reading Score"]
sizemathpass = school_overview.groupby("Size Type").mean()["Percentage Passing Math"]
sizereadpass = school_overview.groupby("Size Type").mean()["Percentage Passing Reading"]
sizeoverallpass = (sizemathpass+sizereadpass)/2

size_summary = pd.DataFrame({
    "Average Math Score":sizemath,
    "Average Reading Score":sizeread,
    "Passing Math":sizemathpass,
    "Passing Reading":sizereadpass,
    "Passing Overall":sizeoverallpass
})
size_summary


# In[ ]:




