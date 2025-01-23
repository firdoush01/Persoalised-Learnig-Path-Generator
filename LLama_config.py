from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
import asyncio
from textprocessor import TextPreprocessor

class LLM_Config:
    def __init__(self):
        os.environ["GROQ_API_KEY"] = "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"
        self.model = ChatGroq(
            api_key=os.environ.get("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile",
            temperature=0.7,
            max_tokens=2048,
            model_kwargs={
                "top_p": 0.9,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.3,
            },
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )


class GoalQuiz(LLM_Config):
    def __init__(self):
        super().__init__()

    async def __get_quiz_response_async(self, user_input, chat_history, current_user):
        # Define the quiz template prompt with questions related to the user's goals
        quiz_temp = ChatPromptTemplate.from_messages([
            ("system", """You are a goal-assistant quiz bot. Ask questions to test user's knowledge in the subject or goal user specified. Provide four options for each question, with the fourth option allowing for custom input.

            Current user: {current_user}

            Recent chat history of questions and answers:
            {chat_history}

            Analyze the chat history to understand the context of previous questions under the "question" key and the user's answers under the "response" key. Use this information to generate a relevant follow-up question that builds upon the user's previous responses.

            Your response must be strictly in JSON format with the following structure, and nothing else:
            {{
                "question": "[Your follow-up quiz question, based on the user's goals]",
                "options": [
                    "[Option 1]",
                    "[Option 2]",
                    "[Option 3]",
                    "Other: Please specify your answer."
                ]
            }}

            Ensure that your follow-up question and options are logically connected to the previous interactions and the user's latest response.

            User's latest response to last question: {input}
            """), 
            ("human", "{input}"),
        ])

        # Chain the template with the model to process the quiz logic
        chain = quiz_temp | self.model
        return await chain.ainvoke({"input": user_input, "chat_history": chat_history, "current_user": current_user})

    def get_quiz_response(self, user_input, chat_history, current_user):
        # Run the async method in a synchronous manner
        return asyncio.run(self.__get_quiz_response_async(user_input, chat_history, current_user))


class Analyzer(LLM_Config):
    def __init__(self):
        super().__init__()

    async def __analyze_async(self, quiz_type, chat_history):
        analysis_template = ChatPromptTemplate.from_messages([
            ("system", f"""You are an expert {quiz_type} analyst. Based on the provided chat history, analyze the user's responses to determine their potential strengths, interests, and natural inclinations. Provide a comprehensive analysis of their {quiz_type.lower()} and suggest potential career paths that align with these traits.

            Chat history:
            {{chat_history}}

            Provide your analysis as a simple string response.
            """),
            ("human", "Please analyze the chat history and provide insights.")
        ])
        chain = analysis_template | self.model
        response = await chain.ainvoke({"chat_history": chat_history})
        return response.content

    def get_analysis(self, quiz_type, chat_history):
        return asyncio.run(self.__analyze_async(quiz_type, chat_history))



class RoadmapGenerator(LLM_Config):
    def __init__(self):
        super().__init__()

    async def __generate_roadmap_async(self, quiz_analysis):
        roadmap_template = ChatPromptTemplate.from_messages([
            (
                "system", 
                """You are a career development expert and academic helper. Based on the provided analyses of the quiz taken for the user's goal, create a comprehensive roadmap for the user's career development. This roadmap should integrate insights from analyses and provide actionable steps for the user to pursue their optimal career path. Always provide the steps in a structured sequence from what the user should do first to the next actions.

                Quiz Analysis:
                {quiz_analysis}

                Provide your roadmap in this JSON format as a string that can later be used for visualization, outlining key steps and recommendations:

                {{
                "career_path": [
                    {{
                    "path": "<Career Path Name>",
                    "steps": [
                        {{
                        "step": <Step Number>,
                        "action": "<Action Description>",
                        "resources": ["<Resource 1>", "<Resource 2>", ...],
                        "duration": "<Estimated Duration>"
                        }},
                        ...
                    ]
                    }}
                ]
                }}
                """
            ),
            (
                "human", 
                "Please generate a career roadmap based on the analyses."
            )
        ])

        chain = roadmap_template | self.model
        response = await chain.ainvoke({
            "quiz_analysis": quiz_analysis
        })
        return response.content

    def get_roadmap(self, quiz_analysis):
        return asyncio.run(self.__generate_roadmap_async(quiz_analysis))
