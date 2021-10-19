import json
import boto3
from botocore.client import Config
import StringIO



def lambda_handler(event,context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-2:462554666803:water2-ohio')
    
    try:
    
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        temp = StringIO.StringIO()
        downloadbucket = s3.Bucket('chadzi-ch1')
        downloadbucket.download_fileobj('message', temp)
        f=temp.getvalue()
        print(f)
        
        gal = 0.0
        totalGal = 0.0
        galString = " "
        zeros = int(0)
        arr = []
        line = f
        x=line.find(",")
        while(x!=-1):
          x=line.find(",")
          if(x!=-1):
            if((line[:x]).find("-")>0):
              arr.append(line[:x])
            line=line[x+1:]
        z=len(arr)
        arr2=[]
        for ele in arr:
          ind=ele.find("-")
          arr2.append(int(ele[ind+1:]))
        
        y = len(arr2)
        for x in range(y):
          val = arr2[x]
          if(val == 0):
            zeros = zeros + 1
          gal = val * .075
          gal = gal / 2
          totalGal += gal
          print(gal)
          galString += str(x)+ "--" + str(gal) + str(",  ")
        print(zeros)
        print(totalGal)
        print(galString)
        if(zeros >= 1):    
            MessageVal = "System OK # zeros found = " + str(zeros)  + " total gallons = "+ str(totalGal) + str("  ") + galString + str("    ") + f 
        else :
            MessageVal = "Probable leak, no zeros found  "  + " total gallons = "+ str(totalGal) + str("  ") + galString + str("    ") + f 
        
        
        topic.publish(Subject="water2 Deployed", Message=MessageVal)
    except:
        topic.publish(Subject="water Deploy Failed", Message="The water did not run successfully")
        raise
    return "water done"            

