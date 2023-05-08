import pandas as pd
from glob import glob
import json
import os
import numpy as np
import pyarrow.parquet as pq
import pyarrow as pa

eventsFiles = r'C:\Users\amagana1\Documents\personal\Master\Projecto\open-data-master\data\events'
eventsFileCsv = r'C:\Users\amagana1\Documents\personal\Master\Projecto\open-data-master\data-csv'
df_array = []
totalfil=glob(eventsFiles + '\*.json')
cuenta=0
for f_name in totalfil:
    cuenta=cuenta+1
    print(str(cuenta) + '/' + str(len(totalfil)))

    f = open (f_name, "r", encoding="utf8")
    df = pd.json_normalize(json.loads(f.read()) 
                            #record_path =['lineup'] 
                            #meta=['team_id', 'team_name']
                        )
    file_name = os.path.splitext(os.path.basename(f_name))[0]
    df['match_id']=file_name
    #print(file_name)
    df=df[(df['period']!=5)]
    #print(df.columns.values)
    df[['loc_x','loc_y']]=df["location"].apply(lambda x: pd.Series(str(x).strip('[]').split(",")))
    df['loc_x']=df['loc_x'].replace("NaN", value=np.nan).astype(float)
    df['loc_y']=df['loc_y'].replace("NaN", value=np.nan).astype(float)
    df['loc_x'] = df['loc_x'].fillna(-1)
    df['loc_y'] = df['loc_y'].fillna(-1)
    #df['shot.end_location']=df['shot.end_location'].apply(lambda x: x if len(x)==3 else x.append('0'))
    print(df['shot.end_location'])        
    df[['gol_x','gol_y', 'gol_z']]=df["shot.end_location"].apply(lambda x: pd.Series(str(x).strip('[]').split(",")))
    print(df['gol_x'])
    print(df['gol_y'])
    print(df['gol_z'])
    df['gol_x']=df['gol_x'].replace("NaN", value=pd.np.nan).astype(float)
    df['gol_y']=df['gol_y'].replace("NaN", value=pd.np.nan).astype(float)
    df['gol_x'] = df['gol_x'].fillna(-1)
    df['gol_y'] = df['gol_y'].fillna(-1)
    #df['shot.dangerous'] = np.where(((df['loc_x'].astype(int)>=94) & (df['loc_y'].astype(int)>=25) & (df['loc_y'].astype(int)<=60)) | ((df['loc_x'].astype(int)<=25) & (df['loc_y'].astype(int)>=25) & (df['loc_y'].astype(int)<=60)), True, False)
    df['shot.dangerous'] = np.where(((df['loc_x'].astype(int)>=94) & (df['loc_y'].astype(int)>=25) & (df['loc_y'].astype(int)<=60)), True, False)
    for (cc), group_poss in df.groupby('possession'):
        
        if True in set(group_poss['shot.dangerous']):
            group_poss['possession.dangerous']= 'True'
            group_poss['possession']= cc
            #print(cc)
            #shot_pass_name=group_poss[(group_poss['type.name']=='Shot')]
            shot_pass_name=group_poss[['id','player.name','loc_x','loc_y','pass.length','pass.angle', 'pass.height.name', 'pass.body_part.name']]
            shot_pass_name.rename(columns={'id':'shot.key_pass_id', 'player.name':'pase_nombre', 'loc_x':'loc_x_pass', 'loc_y':'loc_y_pass', 'pass.length':'length_pass', 'pass.angle':'angle_pass'}, inplace = True)#nombre=shot_pass_name['shot.key_pass_id'].to_list()
            #print(group_poss[['type.name']])              
            group_poss=pd.merge(group_poss, shot_pass_name, how="left", on=["shot.key_pass_id"])
            #print(group_poss[['pase_nombre', 'type.name', 'loc_x_pass', 'loc_y_pass', 'length_pass', 'angle_pass']])
              
        else:
            group_poss['possession.dangerous']= 'False'
            group_poss['possession']= cc
        groupo=group_poss[(group_poss['possession.dangerous']=='True')]
        df_array.append(groupo)
df_concat_events = pd.concat(df_array)
print('Done')
#pd.set_option('display.max_columns', None)
#df_concat_events.head()
#df_concat_events = df_concat_events.drop(columns=['goalkeeper.penalty_saved_to_post', 'half_end.early_video_end'])

df_concat_events.to_csv("eventsDf_V7_newFormat.csv", sep=";", header=True, doublequote=True, decimal='.', index=False)
df_concat_events.to_parquet('eventsDf_V7_newFormat.parquet', compression='GZIP')

#table = pa.Table.from_pandas(df_concat_events)

""" pq.write_table(table, 'eventsDf_v4.parquet')
write('eventsDf_v4_.parq', df_concat_events, compression='GZIP', file_scheme='hive')#df_array = []
#for f_name in glob(eventsFiles):
#    f = open (f_name, "r", encoding="utf8")
#    df = pd.json_normalize(json.loads(f.read()) 
#                            #record_path =['lineup'] 
#                            #meta=['team_id', 'team_name']
#                        )
#    file_name = os.path.splitext(os.path.basename(f_name))[0]
#    df['match_id']=file_name
#
#    df_array.append(df)
#df_concat_events = pd.concat(df_array)
#print(df_concat_events)
write('eventsDf_v4_izq.parq', df_concat_events, compression='GZIP', file_scheme='hive')
#df_concat_events = df_concat_events.drop(columns=['goalkeeper.penalty_saved_to_post', 'half_end.early_video_end'])
#table = pa.Table.from_pandas(df_concat_events)
pq.write_table(table, 'eventsDf_v4_izq.parquet')
#df_concat_events.to_csv(f"eventsDf_v4_izq.csv", sep=",", header=True, doublequote=True, decimal='.', index=False) """