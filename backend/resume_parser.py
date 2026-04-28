import re

def clean_resume(text):
  
    text = re.sub(r'\s+', ' ', text)

 
    text = re.sub(r'\S+@\S+', '', text)

   
    text = re.sub(r'\d{10}', '', text)

    return text.strip()