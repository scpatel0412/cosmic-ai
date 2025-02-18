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
            """
            The following is a conversation. The assistant provides answers strictly related to the cosmos, universe, and outer space.

            Question: {question}
            Answer:

            - If the question is related to the cosmos, universe, or outer space, provide an answer.  
            - If asked about a 'model', 'who are you', 'who created you', or any personal details about the assistant, respond with: 'I am Cosmic AI, developed by Sagar Patel.'  
            - For any other topics, respond with: 'I have no knowledge regarding that. Ask me anything about the cosmos.'
            """
        )

        # Format the prompt with the question
        formatted_prompt = prompt_template.format(question=question)

        # Invoke the LLM chain with the formatted prompt
        response = self.llm.invoke(formatted_prompt)
        print(response.content)
        return response
        
        

