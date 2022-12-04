import json
import boto3
import urllib.request as request, urllib.parse as parse
import requests as r

def lambda_handler(event, context):
    client = boto3.client('rekognition')
    request_data = event['queryStringParameters']
    print(request_data)
    action = request_data['action']
    oracle_id = request_data['oracle_id']
    result = dict()
    
    result["oracle_id"] = oracle_id
    
    if action == 'I':
        filename = request_data['filename']
        #Get AWS Rekognition labels
        img = request.urlopen('https://objectstorage.us-ashburn-1.oraclecloud.com/n/id5bhhnsvcbs/b/standard_vinny_dev/o/'+filename)
        image = bytearray(img.read())
        
        response = client.detect_labels(
            Image={
                'Bytes': image
            },
            MaxLabels=5
        )
    
        new_response = response["Labels"]
        result["filename"] = filename
        name = []
        confidence = []
        for i in range(len(new_response)):
            name.append(new_response[i]["Name"])
            confidence.append(new_response[i]["Confidence"])
        
        result["name"] = name
        result["confidence"] = confidence
        result["calorias"] = 0
        result["porciones"] = 0
        result["calorias_totales"] = 0
        result["fecha_consumo"] = ""
    
        print(result)
    
        x = r.post("http://193.122.201.123:8000/book", json = result)
        if not x.ok:
            print(f"Failed to post {x} - {result}")
    
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    if action == 'D':
        x = r.delete("http://193.122.201.123:8000/book/"+oracle_id, json = result)
        if not x.ok:
            print(f"Failed to delete {x} - {result}")
            return {
                'statusCode': 201,
                'body': json.dumps(result)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
    
    if action == 'U':
        calorias = request_data['calorias']
        porciones = request_data['porciones']
        fecha = request_data['fecha']
        
        result["calorias"] = int(calorias)
        result["porciones"] = int(porciones)
        result["calorias_totales"] = result["calorias"] * result["porciones"]
        result["fecha_consumo"] = fecha
        
        x = r.put("http://193.122.201.123:8000/book/"+oracle_id, json = result)
        if not x.ok:
            print(f"Failed to update {x} - {result}")
            return {
                'statusCode': 201,
                'body': json.dumps(result)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
    
    if action == 'G':
        x = r.get("http://193.122.201.123:8000/book/"+oracle_id)
        res = dict()
        res["items"] = x.json()
        print(res)
        if not x.ok:
            print(f"Failed to get {x} - {oracle_id}")
            return {
                'statusCode': 201,
                'body': json.dumps(res)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(res)
            }
