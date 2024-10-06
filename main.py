# for the LociGraph Web App on Azure

from typing import Union
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import PlainTextResponse

# Import the necessary libraries
import class_gen_JSON_knwl_graph as cgjkg  # Import the class file
object = cgjkg.gen_json_kg()  # Create an object of the class

# set up an azure account to support this fastapi app
from azure.appconfiguration import AzureAppConfiguration
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load the configuration settings from the Azure App Configuration
app_config = AzureAppConfiguration(
    connect_str="Endpoint=https://config-knowledge-graph.azconfig.io;Id=3g6-l0-s0:6Dn8X8LwF4fQ6Qe4t7Q6;Secret=3
    credential=DefaultAzureCredential(),
)

app = FastAPI() 

async def unhandled_exception_handler(request: Request, exc: Exception) -> PlainTextResponse:
    # Log the exception details here
    return PlainTextResponse(str(exc), status_code=500)

@app.get("/")
def read_root():# Call the method generate_graph to generate the graph
    return {"Hello": "World"}

@app.get("/ai_utilities/{kg_datasource}")
def gen_JSON_kg(kg_datasource: str, data_string: str):
    # Call the method generate_graph to generate the graph
    myJSONkg = object.meth_gen_JSON_kg(data_string)
    return myJSONkg

@app.get("/kg/{kg_data_input}")
def read_item(kg_data_input: str, kg_source_data: Union[str, None] = None):
    #return {"kg_data_input": kg_data_input, "kg_source_data": kg_source_data}
    myJSONkg = object.meth_gen_JSON_kg(kg_source_data)
    return myJSONkg

