import os 
import json
import pandas as pd
import traceback
from src.mcqGenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqGenerator.MCQGenerator import generate_evaluate_chain
from src.mcqGenerator.logger import logging


# loading json file
with open(r'Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

# creating a title for the app
    st.title("MCQ Creator Application with Langchain")

#create a form using st.form
    with st.form("user_inputs"):
        #file upload
        uploaded_file=st.file_uploader("Upload a PDF or txt file")

        #input fields
        mcq_counter = st.number_input("No OF MCQs",min_value=3,max_value=50)

        #subject
        subject=st.text_input("subject",max_chars=20)

        #quiz tone
        tone=st.text_input("Complexity Level of Questions",max_chars=20,placeholder="Simple")

        #add button
        button=st.form_submit_button("Create MCQs")

        #check if button is clicked and all fields have input
        if button and uploaded_file is not None and mcq_counter and subject and tone:
            with st.spinner("loading..."):
                try:
                    text=read_file(uploaded_file)
                    #count tokens and the cost of api call
                    with get_openai_callback() as cb:
                        response=generate_evaluate_chain(
                            {
                                "text": text,
                                "number": mcq_counter,
                                "subject":tone,
                                "tone": button,
                                "response_json": json.dumps(RESPONSE_JSON)
                            }
                        )
                except Exception as e:
                    traceback.print_exception(type(e),e,e.__traceback__)
                    st.error("Error")

                else:
                    print(f"Total Tokens:{cb.total_tokens}")
                    print(f"Prompt Tokens:{cb.prompt_tokens}")
                    print(f"Completion Tokens:{cb.completion_tokens}")
                    print(f"Total Cost:{cb.total_cost}")
                    if isinstance(response,dict):
                        #extract the quiz from the response
                        quiz=response.get("quiz",None)
                        if quiz is not None:
                            table_data=get_table_data(quiz)
                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1
                                st.table(df)
                                #display the review in a text box as well
                                st.text_area(label="Review",value=response["review"])
                            else:
                                st.error("Error in the table data")


                    else:
                        st.write(response)
                            








































