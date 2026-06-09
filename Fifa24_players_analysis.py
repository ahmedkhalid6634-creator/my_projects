import pandas as pd #for cleaning and managing data
import data_profiling as dp #for EDA
from def_awareness_function import compute_defense_awareness #for fixing the column of 'marking'
from normalize import clean_text_column #to normalize and the names of the players and there clubs
#setting display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#import file
player_df=pd.read_csv('player_stats.csv',encoding='ISO-8859-1')
#observing
profile=dp.ProfileReport(player_df,title="Fifa analysis observation",html={"style":{"theme":"cosmo","full_width":True}},interactions={"targets":[]},correlations={"pearson":{"calculate":False},"spearman":{"calculate":True},"phi_k":{"calculate":True},},missing_diagrams={"bar":False,"matrix":False,"heatmap":False})
profile.to_file("fifa_data_report.html")
#correcting data types and formats
player_df["marking"]=pd.to_numeric(player_df["marking"],errors='coerce').fillna(0).astype(int)
player_df['value'] = player_df['value'].str.replace('$', '', regex=False).str.replace('.', '', regex=False)
player_df["value"]=pd.to_numeric(player_df["value"],errors='coerce').astype(int)
#correcting player column typos
player_df["player"]=clean_text_column(player_df["player"])
#correcting club column typos
player_df["club"]=clean_text_column(player_df["club"])
#correcting the values and renaming the column marking
player_df.rename(columns={'marking':"defense_awareness"}, inplace=True)
player_df=compute_defense_awareness(player_df)
#cleaning duplicates and ordering
player_df.sort_values(by="age",ascending=False,inplace=True,ignore_index=True)
player_df=player_df.drop_duplicates(subset=['player'],keep='first',ignore_index=True)
#EDA
profile=dp.ProfileReport(player_df,title="Fifa Footballers Analysis 2024",html={"style":{"theme":"cosmo","full_width":True}},interactions={"targets":[]},correlations={"pearson":{"calculate":False},"spearman":{"calculate":True},"phi_k":{"calculate":True},},missing_diagrams={"bar":False,"matrix":False,"heatmap":False})
profile.to_file("fifa_data_report.html")
player_df.to_csv('Fifa_players_stats.csv',index=False)