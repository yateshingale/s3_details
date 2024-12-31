from flask import Flask, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


app = Flask(__name__)
s3 = boto3.client('s3')
bucket_name = 'file-upload-notification'

@app.route('/list-bucket-content', defaults={'path': ''}, methods=['GET'])
@app.route('/list-bucket-content/<path>', methods=['GET'])
def list_bucket_content(path):
    try:
       
        if path:
            
            result = s3.list_objects_v2(Bucket=bucket_name, Prefix=path, Delimiter='/')
        else:
            
            result = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')

        
        content = []
        if 'CommonPrefixes' in result:
            content.extend([prefix['Prefix'].split('/')[-2] for prefix in result['CommonPrefixes']])
        if 'Contents' in result:
            content.extend([content_item['Key'].split('/')[-1] for content_item in result['Contents']])

        return jsonify({"content": content}), 200

    except (NoCredentialsError, PartialCredentialsError):
        return jsonify({"error": "AWS credentials not configured properly"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
