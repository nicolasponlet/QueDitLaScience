from openai import OpenAI


class PromptManager:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
        
    def create_prompt(self, personna, task, context, response_format):
        personna_text = f"\nAs a: {personna}; "
        task_text = f"\nYou have to: {task}; "
        context_text = f"\nContext: {context}; "
        format_text = f"\nFormat response : {response_format}; "
        return personna_text + task_text + format_text + context_text


    def get_response_lines(self, prompt):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            temperature=0
        )

        result = response.choices[0].message.content
        
        result = result.replace("\n\n", "\n")
        
        return result.splitlines()

