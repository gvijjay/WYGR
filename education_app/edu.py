import os
import time
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from wygr.agents.teaching_agent import teaching_agent_fun
from wygr.tools.generating_syllabus import generate_syllabus

# import your OpenAI key (put in your .env file)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.5, api_key=api_key)
teaching_agent=teaching_agent_fun(llm)

with gr.Blocks() as demo:
    gr.Markdown("# Your AI Instructor")
    with gr.Tab("Input Your Information"):

        def perform_task(input_text):
            # Perform the desired task based on the user input
            task = (
                "Generate a course syllabus to teach the topic: " + input_text
            )
            syllabus = generate_syllabus(llm,input_text, task)
            teaching_agent.seed_agent(syllabus, task)
            return syllabus

        text_input = gr.Textbox(
            label="State the name of topic you want to learn:"
        )
        text_output = gr.Textbox(label="Your syllabus will be showed here:")
        text_button = gr.Button("Build the Bot!!!")
        text_button.click(perform_task, text_input, text_output)
    with gr.Tab("AI Instructor"):
        #       inputbox = gr.Textbox("Input your text to build a Q&A Bot here.....")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="What do you concern about?")
        clear = gr.Button("Clear")

        def user(user_message, history):
            teaching_agent.human_step(user_message)
            return "", history + [[user_message, None]]

        def bot(history):
            bot_message = teaching_agent.instructor_step()
            history[-1][1] = ""
            for character in bot_message:
                history[-1][1] += character
                time.sleep(0.05)
                yield history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
demo.queue().launch(debug=True, share=True)

