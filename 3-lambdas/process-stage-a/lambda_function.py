import awswrangler as wr
import boto3, os, json
import pandas as pd
import logging

def init_logger(file_name, log_level=None):
    if not log_level:
        log_level = "INFO"
    logging.basicConfig()
    logger = logging.getLogger(file_name)
    logger.setLevel(getattr(logging, log_level))
    return logger

def getObjectList(s3PathKey):
    return wr.s3.list_objects(s3PathKey)

def s3FilesProcessing(csvObjects, dataset, s3OutputPath): 
    df_array = []
    for f_name in csvObjects:
        logging.info(f"Reading s3 File: {f_name}")
        df = wr.s3.read_json(path=f_name, 
                         orient = 'records'
                        )
        
        if dataset == 'three-sixty':
            filenameValue = f_name.split('/')[-1].replace('.json', '')
            df['filename'] = filenameValue

        if dataset == 'events': 
            filenameValue = f_name.split('/')[-1].replace('.json', '')
            df['filename'] = filenameValue
            
            df['tactics'] = df['tactics'].apply(json.dumps)
            df['type'] = df['type'].apply(json.dumps)
            df['possession_team'] = df['possession_team'].apply(json.dumps)
            df['play_pattern'] = df['play_pattern'].apply(json.dumps)
            df['team'] = df['team'].apply(json.dumps)
            
            dftactics = pd.json_normalize(df.tactics.apply(json.loads)).add_prefix('tactics.')
            dftype = pd.json_normalize(df.type.apply(json.loads)).add_prefix('type.')
            dfpossession_team = pd.json_normalize(df.possession_team.apply(json.loads)).add_prefix('possession_team.')
            dfplay_pattern = pd.json_normalize(df.play_pattern.apply(json.loads)).add_prefix('play_pattern.')
            dfteam = pd.json_normalize(df.team.apply(json.loads)).add_prefix('team.')
            
            df = pd.concat([df, dftactics, dftype, dfpossession_team, dfplay_pattern, dfteam], axis=1)
    
    #df_array.append(df)
    #logging.info(f"Concatination of Dataframe Array")
    #df_concat = pd.concat(df_array)
    
        wr.s3.to_csv(
            df=df,
            path= s3OutputPath,
            dataset = True,
            mode = 'overwrite_partitions',
            partition_cols = ['filename']
        )



#Iniciando Ejecucion de Lambda
ssmClient = boto3.client('ssm', region_name = 'us-east-1')
rawBucket = ssmClient.get_parameter(Name='/Master/S3/CentralBucket')['Parameter']['Value']
stageBucket = ssmClient.get_parameter(Name='/Master/S3/StageBucket')['Parameter']['Value']

logger = init_logger(__name__)

def lambda_handler(event, context):
    try:
        dataset = event['dataset']
        s3RawPath = f"s3://{rawBucket}/datalake/{dataset}/"
        logging.info(f"Using tha following Raw bucket Path: {s3RawPath}")
        s3StagePath = f"s3://{stageBucket}/datalake/{dataset}"
        logging.info(f"Using tha following Stage bucket Path: {s3StagePath}")        
        ObjectList = getObjectList(s3RawPath)
        s3FilesProcessing(ObjectList, dataset, s3StagePath)
    except Exception as e: 
        logging.error(f"Error on LambdaHandler has ocurred: {str(e)}")