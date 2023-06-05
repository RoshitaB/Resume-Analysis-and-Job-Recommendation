from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def datframe_gen(professions):
    counter=0
    l=[]
    skills="hi"
    print("CHECKING 1")
    df = pd.DataFrame(columns=['Title','Company','Ratings','Salary','Location','Job_Post_History','URL', 'Skills', "Profession"])

    for i in professions:
        counter=counter+1
        for j in range(1,3):
            a=i.replace(" ","-")
            b=i.replace(" ","%20")
            url = f"https://www.naukri.com/{a}-jobs-{j}?k={b}"

            driver = webdriver.Chrome("models/chromedriver.exe")
            driver.get(url)
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source,'html5lib')

            driver.close()

            results = soup.find(class_='listContainer fleft')
            job_elems = results.find_all('article',class_='jobTuple')

            for job_elem in job_elems:

                # URL to apply for the job     
                URL = job_elem.find('a',class_="title").get('href')
                print(URL)

                # Post Title
                Title = job_elem.find('a',class_='title').get('title')
                print(Title)
    #             print("naukri title",Title.text)

                # Company Name
                Company = job_elem.find('a',class_='subTitle ellipsis fleft').get('title')
                print(Company)
    #             print("naukri company",Company.text)

                # Ratings
                rating_span = job_elem.find('span',class_='starRating fleft')
                if rating_span is None:
                    Ratings=0
                else:
                    Ratings = rating_span.text
                # print("naukri ratings",Ratings)

                # Salary offered for the job
                Sal = job_elem.find('li',class_='fleft br2 placeHolderLi salary')
                Sal_span = Sal.find('span',class_='ellipsis fleft')
                if Sal_span is None:
                    pass
                else:
                    Salary = Sal_span.text

                # Location for the job post
                Loc = job_elem.find('li',class_='fleft br2 placeHolderLi location')
                Loc_exp = Loc.find('span',class_='ellipsis fleft locWdth')
                if Loc_exp is None:
                    pass
                else:
                    Location = Loc_exp.text

                # Number of days since job posted
                Hist = job_elem.find("div", "jobTupleFooter")
                Post_Hist = Hist.find('span',class_='fleft postedDate')
                if Post_Hist is None:
                    pass
                else:
                    Post_History = Post_Hist.text
                    
                #Skills
    #             skills=job_elem.find_all("ul", ["tags has-description"])
    #             print("naukri skills",skills)
                # print("before skills ",skills)
                # print(soup.find_all(class_='keySkills'))
                skills=job_elem.find_all("ul", ["tags has-description"])
                # print("naukri skills",skills)
                # for div1 in soup.find_all(class_='skill'):
                #     print(div1)
                #     skills=div1.text
                #     print("skills",skills)
                # print("after skills ",skills)

            #   Appending data to the DataFrame 
                
                print("CHECKING 2")
                l.append({'URL':URL,'Title':Title,'Company':Company,'Ratings':Ratings,'Location':Location,'Salary':Salary,'Job_Post_History':Post_History, "Profession":i,"Profession_key":counter, "Skills":skills})
                
    #             vertical_concat = pd.concat([df1, df], axis=0)
    #         print(df)
    print(l)
    df = pd.DataFrame(l)
    return df

def convert_list(ls):
    ls=np.array(ls)
    l=[]
    return ls.flatten()

def score(ls,user_skills):
    cv = CountVectorizer()
    JobText=' '.join(ls)
    text=[user_skills,JobText]
    count_matrix = cv.fit_transform(text)
    matchPercentage=cosine_similarity(count_matrix)[0][1] * 100
    return round(matchPercentage, 2)

def jobs(professions,data):
    df=datframe_gen(professions)
    df["Skills"]=df["Skills"].apply(convert_list)
    user_skills=" ".join(data["skills"])
    df["score"]=df["Skills"].apply(lambda x: score(x,user_skills))
    print(df)
    df_sorted=df.sort_values('score',ascending=False)
    top15=df_sorted[:15]
    top5_2 = df_sorted[df_sorted['Profession_key'] == 2.0 ][:5]
    top5_3=df_sorted[df_sorted['Profession_key'] == 3.0 ][:5]
    return top15

