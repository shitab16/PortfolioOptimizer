# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import os
# from azure.storage.blob import BlobClient, ContentSettings
import json
from .transformfactory import Transformfactory
import traceback
import azure.function as func


def main(headers: dict) -> dict:

    # try:
    filepath = headers.get("FilePath")
    if filepath == None:
        raise Exception("filepath not found")
    
    root_tag = headers.get("MessageTypeKey")   # "ns0:EFACT_D96A_PRICAT_EAN006"
    if root_tag == None:
        raise Exception("MessageTypeKey not found")

    line_object_type = headers.get("LineObjectType")
    if line_object_type == None:
        raise Exception("LineObjectType not found")

    root_prefix = "ns0:EFACT_"
    root_key = root_prefix + root_tag

    # conn_str = os.environ.get("conn_str")
    # if conn_str == None:
    #     raise Exception("conn_str not found")
    
    # container_name = filepath.split('/')[1]
    # filename = '/'.join(filepath.split('/')[2:])

    # Read data from blob
    # blob_client = BlobClient.from_connection_string(conn_str, container_name, filename)
    # download_stream = blob_client.download_blob()
    # data = json.loads(download_stream.readall())
    with open(r'"C:\Users\mande\Downloads\merged-IN_16041ed3.json"') as t:
        data = json.loads(t)
    if len(data) == 0:
        raise Exception(f"Read file content size 0. Container name: {container_name}, Filename: {filename}")              

    
    transformer = transformfactory().get_transformer(line_object_type)
    output = transformer.transform(root_key, data) 


    if len(output) == 0:
        raise Exception(f"The file does not contain relevant Color and/or Product Object and sizes. Container name: {container_name}, Filename: {filename}")  

    fname = filename.split("/")[-1]
    fpath = "/".join(filename.split("/")[:-1])
    filename = fpath + "/transformed-" + fname.split("-")[0] + ".json"
    return func.HttpResponse(str(output))

    # blob_client = BlobClient.from_connection_string(conn_str, container_name, filename)
    # blob_client.upload_blob(json.dumps(output), overwrite=True, content_settings=ContentSettings(content_type='application/json'))

#     return {'StatusCode' : 200, 'Result': {'FilePath' : str('/' + container_name + '/' + filename)}}

# except Exception as e:
#     tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
#     tb_str = "".join(tb_str)
#     return {'StatusCode' : 500, 'Result': {'Message': str(e), 'StackTrace': tb_str}}
