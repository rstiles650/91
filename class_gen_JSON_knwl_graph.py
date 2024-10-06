import base64   # Import the base64 module to encode and decode base64 strings
from urllib.parse import urlparse, parse_qs, urlencode, quote_plus, unquote_plus
import requests # Import the requests module to make HTTP requests
import os       # Import the os module to access the environment variables
from openai import OpenAI # Import the OpenAI class from the openai module
import json     # Import the json module to work with JSON data

chatgpt_model_target = "gpt-4o-2024-08-06"
#chatgpt_model_target =  = "o1-preview",
#chatgpt_model_target =  = "o1-preview-2024-09-12",
#chatgpt_model_target =  = "o1-mini",
#chatgpt_model_target  = "o1-mini-2024-09-12",

def gen_JSON_kg_from_string(string_input):
    client = OpenAI()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts structured data from a string."
        },
        {
            "role": "user",
            "content": "extract a knowledge graph from the following text " + string_input,
        }
    ]

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "extracted_data",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "edges": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": { "type": "string" },
                                "locitype": { "type": "string" },
                                "start_node": { "type": "string" },
                                "end_node": { "type": "string" },
                                "starttime": { "type": "string" },
                                "endtime": { "type": "string" },
                                "created": { "type": "string" },
                                "modified": { "type": "string" },
                                "color": { "type": "string" },
                                "id": { "type": "string" },
                                "origin": { "type": "string" },
                                "exists": { "type": "string" },
                                "derived": { "type": "string" }
                            },
                            "required": ["type", "locitype", "start_node", "end_node", "starttime", "endtime", "created", "modified", "color", "id", "origin", "exists", "derived"],
                            "additionalProperties": False
                        }
                    },
                    "nodes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": { "type": "string" },
                                "locitype": { "type": "string" },
                                "latitude": { "type": "string" },
                                "longitude": { "type": "string" },
                                "starttime": { "type": "string" },
                                "endtime": { "type": "string" },
                                "criteria": { "type": "string" },
                                "id": { "type": "string" },
                                "color": { "type": "string" },
                                "textcolor": { "type": "string" },
                                "created": { "type": "string" },
                                "folded": { "type": "string" },
                                "showimage": { "type": "string" },
                                "link": { "type": "string" },
                                "modified": { "type": "string" },
                                "name": { "type": "string" },
                                "richcontent": { "type": "string" },
                                "text": { "type": "string" },
                                "image": { "type": "string" },
                                "imagedata": { "type": "string" },
                                "origin": { "type": "string" },
                                "scale": { "type": "string" },
                                "iconscale": { "type": "string" },
                                "rotation": { "type": "string" },
                                "x": { "type": "string" },
                                "y": { "type": "string" },
                                "z": { "type": "string" },
                                "pinned": { "type": "string" },
                                "freeze": { "type": "string" },
                                "exists": { "type": "string" },
                                "derived": { "type": "string" }
                            },
                            "required": [ "type", "locitype", "latitude", "longitude", "starttime", "endtime", "criteria", "id", "color", "textcolor", "created", "folded", "showimage", "link", "modified", "name", "richcontent", "text", "image", "imagedata", "origin", "scale", "iconscale", "rotation", "x", "y", "z", "pinned", "freeze", "exists", "derived" ],
                            "additionalProperties": False
                        }
                    },
                    "graphname": { "type": "string" }
                },
                "required": ["edges", "nodes", "graphname"],
                "additionalProperties": False
            }
        }
    }

    chat_completion = client.chat.completions.create(
        model = chatgpt_model_target,
        messages=messages,
        response_format=response_format
    )
    # Romove the escape character '/' from the JSON string with json.loads
    myJson = json.loads(chat_completion.choices[0].message.content)
    return myJson   

# Create a class that takes in a string parameter to generate and return a JSON graph of nodes and edges
# The class should have a method that takes in a string parameter and returns a JSON grapclass 
# Staff: def __init__ (self, pPosition, pName, pPay):
class gen_json_kg:

    # Method to generate graph from TEXT
    def meth_JSON_kg_text(self, stringText): # PASSED TEST

        myJSON = gen_JSON_kg_from_string(stringText)
        return myJSON

    # Define the method to generate the graph
    def meth_JSON_kg_web_URL(self, targetyURL): # PASSED TEST

        #import requests 
        from bs4 import BeautifulSoup
        print("BEFORE call to : response = requests.get(targetyURL)")
        response = requests.get(targetyURL)
        print("AFTER call to : response = requests.get(targetyURL)")
        soup = BeautifulSoup(response.text, 'html.parser')
        stringText = soup.get_text()
            
        myJSON = gen_JSON_kg_from_string(stringText)
        return myJSON

    # Method to generate graph from IMAGE on local machine
    def meth_JSON_kg_image(self, image_path): # PASSED TEST
        # Get the OpenAI API key from the environment variable
        api_key = os.environ["OPENAI_API_KEY"]

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": chatgpt_model_target,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "whate are the entities and their relationships to each other in this image?" #"What’s in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # extract the message content text from the response.json()
        imageDescription = response.json()['choices'][0]['message']['content']

        myJSON = gen_JSON_kg_from_string(imageDescription)

        return myJSON
    
    # Method to generate graph from IMAGE on the web
    def meth_JSON_kg_image_URL(self, imageURL):

        api_key = os.environ["OPENAI_API_KEY"]
        client = OpenAI()

        response = client.chat.completions.create(
        model = chatgpt_model_target,
        messages=[
            {
            "role": "user",
            "content": [
                # what are the entities and their relationships to each other in this image (try)
                {"type": "text", "text": " whate are the entities and their relationships to each other in this image?"},
                {
                "type": "image_url",
                "image_url": {
                    "url": imageURL,
                },
                },
            ],
            }
        ],
        )

        imageDescription = response.choices[0].message.content

        myJSON = gen_JSON_kg_from_string(imageDescription)
        return myJSON
    
    # Method to determine the type of the input
    def get_input_type(self, myInput):  
    
        client = OpenAI()

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "answer the following question with the following options: image url, webpage url, text, or image file and path",
                },
                {
                    "role": "user",
                    "content": "what is the followng user input? " + myInput,
                }
            ],
            model = chatgpt_model_target,
        )

        myResponse = (chat_completion.choices[0].message.content)
        return myResponse
    
    # Method to generate graph from various inputs
    def meth_gen_JSON_kg(self, myInput):

        myInput = unquote_plus(myInput)
        myInput = myInput.strip()

        # Determine the type of the input
        myType = self.get_input_type(myInput)   

        if myType == "image url":
            return self.meth_JSON_kg_image_URL(myInput)
        elif myType == "webpage url":
            return self.meth_JSON_kg_web_URL(myInput)
        elif myType == "text":
            return self.meth_JSON_kg_text(myInput)
        elif myType == "image file and path":
            return self.meth_JSON_kg_image(myInput)
        else:
            return self.meth_JSON_kg_text(myInput)