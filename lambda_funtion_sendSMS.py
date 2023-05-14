import logging
import pymysql
import os
import datetime
import boto3
import time

def lambda_handler(event, context):
    
    records = []
    rds_host  = os.environ['rds_host']
    user_name = os.environ['user_name']
    password = os.environ['password']
    db_name =  os.environ['db_name']
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        print("Trying to connect")
        conn = pymysql.connect(host=rds_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()
    
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    
    with conn.cursor() as cur:
        cur.execute("select * from Birthday")
        for row in cur:
            records.append(list(row))
            logger.info(row)
    conn.commit()
    
    re = [datetime.datetime.strptime(i[-1], '%Y-%m-%d') for i in records]
    tom = datetime.date.today() + datetime.timedelta(days=1)
    birthdays = []
    for index, i in enumerate(re):
      if i.day == tom.day and i.month == tom.month:
        birthdays.append([index, tom.year - i.year])
    
    messages = []
    for j in birthdays:
      messages.append(f"Happy Birthday!! {records[j[0]][1]} is turning {j[1]} tomorrow! Wish them well")
    
    
    print(messages)
    sns = boto3.client('sns', region_name="eu-north-1")
    for i in messages:
        response = sns.publish(TopicArn='arn:aws:sns:eu-north-1:651243252920:BirthdayApp_Messaging_Topic',Message=i)
        time.sleep(1)
        print(response)
        

