import os
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

class Groq_Service:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv('GROQ_CLOUD_KEY'),
            model=os.getenv('GROQ_MODEL'),
            temperature=0.7,
        )

    def get_answer(self, question):
        """
        Generating response from the question asked by the user.
        """
        prompt_template = PromptTemplate.from_template(
            "The following is a conversation. The assistant provides answers based on the context provided:\n\nQuestion: {question}\nAnswer:"
        )

        # Format the prompt with the question
        formatted_prompt = prompt_template.format(question=question)

        # Invoke the LLM chain with the formatted prompt
        response = self.llm.invoke(formatted_prompt)
        print(response.content)
        return response
        
        

