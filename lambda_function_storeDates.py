import sys
import logging
import pymysql
import json
import random
import os

def lambda_handler(event, context):
    '''
    Description:
    This function is used to handle incoming events from API Gateway and store the form data into a MySQL database instance hosted on Amazon RDS.

    Parameters:

    event: An event object that contains data passed to the function.
    context: An object containing information about the current execution context.
    Returns:
    A dictionary with a status code and response message.

    Example Usage:
    This function can be deployed as an AWS Lambda function and used to handle form submissions from a web application.
    '''
    # rds settings
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
    
    formData = json.loads(event["body"])
    id = random.randint(10**(5), 10**6-1)
    name = str(formData['Name'])
    dob = str(formData['Birthdate'])
    
    sql_string = f"insert into Birthday (ID, Name, Birthdate) values({id}, '{name}', '{dob}')"
    print(sql_string)
    with conn.cursor() as cur:
        cur.execute(sql_string)
        conn.commit()
        cur.execute("select * from Birthday")
        logger.info("The following items have been added to the database:")
        for row in cur:
            logger.info(row)
    conn.commit()

    response = {
        'statusCode': 200,
        'body': json.dumps('Form data received successfully!')
    }
    
    return response
