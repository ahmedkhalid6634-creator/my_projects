import pandas as pd
import unicodedata
import numpy as np
import re
def convert_to_badges(skills_list):
    return " ".join([f":red-badge[{skill}]" for skill in skills_list])
def rem_hidden(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize('NFKC', text)
    hidden_chars = r'[\x00-\x1f\x7f-\x9f\xad\xa0\u200b\u200c\u200d\u200e\u200f\u2028\u2029]'
    text = re.sub(hidden_chars, '', text)
    return re.sub(r'\s+', ' ', text).strip()
def data_refine(data):
    mostaql_jobs = data
    mostaql_jobs=mostaql_jobs.apply(rem_hidden, axis=1)
    #refining
    ## Budget
    mostaql_jobs["Budget"]=mostaql_jobs["Budget"].str.strip()
    mostaql_jobs[["Minimum Budget","Maximum Budget"]] = mostaql_jobs["Budget"].str.extract(r"\$(\d+\.?\d*)\s*-\s*\$(\d+\.?\d*)")
    mostaql_jobs.drop(columns=["Budget"], inplace=True, axis=1)
    ## proposes
    subs={r"أضف":0,
          r"عرضان":2,
          r"واحد":1,}
    mostaql_jobs["Number of Proposals"]=mostaql_jobs["Number of Proposals"].replace(subs , regex=True)
    mostaql_jobs["Number of Proposals"]=mostaql_jobs["Number of Proposals"].str.replace( r'[\u0600-\u06FF]+',"", regex=True)
    ##time intervals
    mostaql_jobs["Time Interval (Days)"]=mostaql_jobs["Time Interval (Days)"].str.replace(r'[\u0600-\u06FF]+',"", regex=True)
    ##accepting rate or percentage
    mostaql_jobs["Accepting Percentage"]=mostaql_jobs["Accepting Percentage"].mask(mostaql_jobs["Accepting Percentage"]=="لم يحسب بعد", "0.00")
    mostaql_jobs["Accepting Percentage"]=mostaql_jobs["Accepting Percentage"].str.replace(r'%','',regex=True)
    #Data correct formats
    mostaql_jobs["Minimum Budget"]=pd.to_numeric(mostaql_jobs["Minimum Budget"],errors="coerce" , downcast="float")
    mostaql_jobs["Maximum Budget"] = pd.to_numeric(mostaql_jobs["Maximum Budget"], errors="coerce", downcast="float")
    mostaql_jobs["Accepting Percentage"]=pd.to_numeric(mostaql_jobs["Accepting Percentage"], errors="coerce", downcast="float")
    mostaql_jobs["Posted Date"]=pd.to_datetime(mostaql_jobs["Posted Date"])
    # removing NAs
    mostaql_jobs.dropna(subset=["Title"], inplace=True, axis=0)
    #NAN handling
    mostaql_jobs["Accepting Percentage"] = mostaql_jobs["Accepting Percentage"].fillna(0.00)
    mostaql_jobs["Description"] = mostaql_jobs["Description"].fillna("No Description Provided")
    mostaql_jobs["Status"] = mostaql_jobs["Status"].fillna("Unknown")
    mostaql_jobs["Number of Proposals"] = mostaql_jobs["Number of Proposals"].fillna(mostaql_jobs["Number of Proposals"].mean())
    mostaql_jobs["Minimum Budget"] = mostaql_jobs["Minimum Budget"].fillna(mostaql_jobs["Minimum Budget"].mean())
    mostaql_jobs["Maximum Budget"] = mostaql_jobs["Maximum Budget"].fillna(mostaql_jobs["Maximum Budget"].mean())
    mostaql_jobs["Time Interval (Days)"] = mostaql_jobs["Time Interval (Days)"].fillna(mostaql_jobs["Time Interval (Days)"].mean())
    # correct formats
    mostaql_jobs["Time Interval (Days)"] = pd.to_numeric(mostaql_jobs["Time Interval (Days)"], errors="coerce",downcast="integer")
    mostaql_jobs["Number of Proposals"] = pd.to_numeric(mostaql_jobs["Number of Proposals"], errors="coerce",downcast="integer")
    #creating in need columns
    mostaql_jobs["Average Budget"] = (mostaql_jobs["Minimum Budget"] + mostaql_jobs["Maximum Budget"]) / 2
    mostaql_jobs["Fin. Urgency"] = (mostaql_jobs["Average Budget"]/mostaql_jobs["Time Interval (Days)"]).astype(float)
    mostaql_jobs["Fin. Urgency"]=mostaql_jobs["Fin. Urgency"].replace(np.inf, np.nan).fillna(0)
    mostaql_jobs["Posted Time"]=mostaql_jobs["Posted Date"].dt.time
    mostaql_jobs["Posted Date"]=mostaql_jobs["Posted Date"].dt.date
    # formatting the whole data frame
    mostaql_jobs=mostaql_jobs[["Title",
                               "Description",
                               "Client Name",
                               "Minimum Budget",
                               "Average Budget",
                               "Maximum Budget",
                               "Fin. Urgency",
                               "Status",
                               "Posted Date",
                               "Posted Time",
                               "Accepting Percentage" ,
                               "Skill Sets" ,
                               "Number of Proposals",
                               "Time Interval (Days)",
                               "Platform",
                               "URL"]]
    url = mostaql_jobs.pop("URL")
    desc = mostaql_jobs.pop("Description")
    skills = mostaql_jobs.pop("Skill Sets")
    badged_skills=skills.apply(convert_to_badges)
    print(mostaql_jobs)
    return mostaql_jobs, url, desc, skills , badged_skills