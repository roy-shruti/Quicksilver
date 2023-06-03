
from fastapi import FastAPI
import openai
import concurrent.futures
import requests
from Quicksilver.subcategories import subcategories,units
 
app = FastAPI()
openai.api_key = 'API_KEY'
@app.get("/get-ingredients/{query}")
def getIngredients(query: str):
       
    # user_queries = [
    #     " Give me the list of ingredients for making "+ query +" in json format " + format +". Label the ingredient categories only from the list of given subcategoreis " + str(subcategories) +"  .The response should only contain the json object and in the same format as provided.",
    #     " Give me the list of ingredients for making "+ query +" in json format " + format +". Label the ingredient categories only from the list of given subcategoreis " + str(subcategories) +"  .The response should only contain the json object and in the same format as provided.",
    #     " Give me the list of ingredients for making "+ query +" in json format " + format +". Label the ingredient categories only from the list of given subcategoreis " + str(subcategories) +"  .The response should only contain the json object and in the same format as provided."
    # ]
    # api_endpoint = "https://api.openai.com/v1/chat/completions"
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     # Submit each API call as a separate task
    #     api_tasks = [
    #         executor.submit(requests.post, api_endpoint, headers={"Authorization": f"Bearer {openai.api_key}"}, json={"messages": [{"role": "system", "content": "gaa"}]} )
    #         for query in user_queries
    #     ]

    #     # Wait for all tasks to complete and retrieve their results
    #     api_responses = [task.result() for task in concurrent.futures.as_completed(api_tasks)]

    # # Process the API responses and return the combined result
    # result = [response.json() for response in api_responses]
    # print(result)
    # return result
    response = process_user_input(ingredient_query(query))
    print(f"ChatGPT: {response}")
    json_data = json_from_response(response)
    print(response)
    recipe_query = "give me the recipe of " + query
    response = process_user_input(recipe_query)
    print("working")
   # upload_response_to_local_host(response)
    print(f"ChatGPT: {response}")
    return (json_data)
    #return response 
def process_user_input(user_input):
    messages = [{"role": "system", "content": "You are acting as a chef. So You must provide me with the list ingredients for the given dish in the mentioned json format {\"name\": \"Dummy Item\",\"quantity\": 5}"}]
    if user_input:
        messages.append({"role": "user", "content": user_input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply
def ingredient_query(query:str):
    format = "{\"request\": [{\"Ingredient\": \"Dummy item\", \"Measurement\": \"Gram\", \"Quantity\": 500, \"Categories\": [\"category1\", \"category2\"]}], \"reciepe\": \"Kuch bhi string\"}"
    
    if query:
        #response = "Give me the list of ingredients for making " + query + "in json format with key as name of ingredient for each ingredient"
        #response = "Give me the list of ingredients for making "+ query +" in json format " + format +". Label the ingredient categories only from the list of given subcategories list "+ str(subcategories) +" .The response should only contain the json object and in the same format as provided."
        response = " Give me the list of ingredients for making "+ query +" in json format " + format +". Label the ingredient categories only from the list of given subcategoreis " + str(subcategories) +"  .The response should only contain the json object and in the same format as provided."
 
        #response = "Give me the list of ingredients for making "+ query +" in json format with four columns (Ingredient,Measurement unit only from "+ str(units) +", Quantity  and a list of all the possible Categories from the list " + str(subcategories) +"that the product can possibly belong to) for each ingredient. The response should only contain the json object."
    return response

def json_from_response(input_string):
    start_index = input_string.find('[')
    end_index = input_string.rfind(']')
    
    if start_index != -1 and end_index != -1 and end_index > start_index:
        extracted_text = input_string[start_index  : end_index +1]
        return extracted_text
    
    return None
