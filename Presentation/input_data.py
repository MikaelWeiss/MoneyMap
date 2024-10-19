import streamlit as st
from openai import OpenAI
import pandas as pd
import time
from supabase import create_client
from io import StringIO
import json

url = st.secrets.connections.supabase['SUPABASE_URL']
key = st.secrets.connections.supabase['SUPABASE_KEY']
supabase = create_client(url, key)

# Initialize session state for messages if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []  # Initialize as an empty list

# Initialize OpenAI client using secrets
client = OpenAI(
    api_key=st.secrets['openai']['api_key'],
    organization=st.secrets['openai']['organization'],
    project=st.secrets['openai']['project']
)

# Create financial assistant
# Create financial assistant
assistant = client.beta.assistants.create(
    name="Fin",
    instructions="""
As a financial expert, your task is to help the average person understand foundational categories of finance and guide them towards achieving financial freedom.

Highlight key financial categories such as savings, income, expenses, and debt, providing clear explanations and actionable advice in each area.

# Steps

1. **Explain Financial Categories:**
   - Define savings, income, expenses, and debt in simple terms.
   - Illustrate the importance of each category in personal finance.

2. **Actionable Advice:**
   - Offer practical tips and strategies to manage each financial category effectively.
   - Suggest specific actions individuals can take to improve their financial health.

3. **Path to Financial Freedom:**
   - Assemble the advice into a coherent plan aimed at achieving long-term financial stability and freedom.
   - Highlight the importance of budgeting, saving, investing, and debt management in the journey towards financial freedom.

# Output Format

The response should be a well-organized paragraph or bullet points, providing a concise explanation and actionable advice for each financial category.

# Examples

**Example 1: Understanding Savings**

- **Explanation**: Savings is the portion of your income that you set aside for future use. It is crucial for emergencies and future expenses.
- **Actionable Advice**: Start saving 10% of your income, gradually increasing this percentage as you become more comfortable.

**Example 2: Managing Expenses**

- **Explanation**: Expenses are the costs incurred for goods and services. It's important to track and control them to avoid overspending.
- **Actionable Advice**: Create a monthly budget to track expenses. Identify areas where you can reduce spending to save more.

# Notes

- Focus on simplicity and clarity to ensure the advice is accessible to individuals with minimal financial knowledge.
- Encourage the habit of regular financial reviews and adjustments to plans as needed.
- Address common misconceptions or challenges people face in each category.
  """,
    tools=[{"type": "file_search"}],
    model="gpt-4o",
)

# Functions for assistant interaction


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant_id
    )


def get_response(thread):
    # Convert to list
    return list(client.beta.threads.messages.list(thread_id=thread.id, order="asc"))


def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id=assistant.id,
                         thread=thread, user_message=user_input)
    return thread, run


def wait_on_run(run, thread):
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id)
        time.sleep(0.5)
    return run


def build_plan(messages, uploaded_file):  # Add thread as a parameter
    # Collect messages and files
    user_messages = "\n".join([msg['content']
                               for msg in messages if msg['role'] == 'user'])
    assistant_messages = "\n".join(
        [msg['content'] for msg in messages if msg['role'] == 'assistant'])

    # Generate JSON data using the assistant
    prompt = f"""
    Respond in JSON only
    User messages: {user_messages}
    Assistant messages: {assistant_messages}
    Uploaded file: {uploaded_file}
    Generate a JSON with the following keys: Month, Income, Expenses, Savings, Debt.
    Include at least 2 years worth of data starting from the current month.
    Make the month be of type int, and have it start at 1 and increment by 1 for each month.
    """

    # Interact with assistant
    thread, run = create_thread_and_run(prompt)
    wait_on_run(run, thread)

    # Retrieve assistant's response
    messages = get_response(thread)

    # Ensure that the assistant's response is a string
    json_data = messages[-1].content[0].text.value if messages else ""

    # Check if json_data is empty
    if not json_data:
        st.error("The assistant's response is empty.")
        # Log the raw messages for debugging
        st.write("Assistant's raw response:", messages)
        return

    # Log the response for debugging
    if not isinstance(json_data, str):
        st.error("Unexpected response format from the assistant.")
        # Log the raw response
        st.write("Assistant's raw response:", json_data)
        return

    # Clean up the JSON data
    json_data = json_data.replace("```json", "").replace("```", "").strip()

    # Convert JSON data to a list of dictionaries
    try:
        financial_data = json.loads(json_data)  # Parse JSON data
    except json.JSONDecodeError:
        st.error("Failed to decode JSON data from the assistant's response.")
        # Log the response for debugging
        st.write("Assistant's response:", json_data)
        return

    # Get general data
    count = supabase.table("user_financial_data").select(
        "month", count="exact").execute().count

    # Insert data into Supabase
    for row in financial_data:
        count += 1
        supabase.table("user_financial_data").insert({
            "month": row["Month"],
            "savings": row["Savings"],
            "income": row["Income"],
            "expenses": row["Expenses"],
            "debt": row["Debt"]
        }).execute()
        response = (
            supabase.table("user_financial_data")
            .insert({"id": 1, "name": "Denmark"})
            .execute()
        )


# Title
st.title("Personal Finance Helper")

# Handle file uploads
uploaded_file = st.file_uploader(
    "Upload your financial spreadsheet (CSV, Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("Uploaded File Preview:")
        st.dataframe(df)

        # Extract and summarize key financial data
        file_data_summary = ""
        if "expenses" in df.columns:
            file_data_summary += f"Total Expenses: {df['expenses'].sum()}\n"
        if "income" in df.columns:
            file_data_summary += f"Total Income: {df['income'].sum()}\n"
        if "savings" in df.columns:
            file_data_summary += f"Total Savings: {df['savings'].sum()}\n"

        # Prepare data for the assistant
        file_data = df.to_string()
        assistant_input = f"{file_data_summary}\nHere is the raw data:\n{file_data}\nCan you help interpret this personal finance data?"

        # Interact with assistant
        thread2, run2 = create_thread_and_run(assistant_input)
        wait_on_run(run2, thread2)

        # Retrieve assistant's response
        messages = get_response(thread2)

        if messages:
            assistant_response = messages[-1]  # Get last message
            st.write("Assistant's Interpretation:")
            st.write(assistant_response.content)

    except Exception as e:
        st.error(f"Error processing file: {e}")

# Chat Input Section
st.subheader(
    "Hi! I'm Fin, your personal finance assistant. How can I help you today?")
if st.session_state.messages.count({"role": "assistant"}) == 0:
    st.caption("You have a couple of options. You can either upload a file, or directly tell Fin things like monthly expenses, income, savings, and debt.")
col = st.columns(2)
with col[0]:
    st.caption(
        "When you're ready, click this button to submit your financial data, and Fin will help you build a financial plan.")
with col[1]:
    st.button("Submit & Build Plan", on_click=build_plan, args=(
        st.session_state.messages, uploaded_file))  # Pass messages and uploaded_file


# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Create a new thread for this conversation and submit the user message
        thread3, run3 = create_thread_and_run(prompt)
        wait_on_run(run3, thread3)

        # Retrieve assistant's response
        messages = get_response(thread3)
        if messages:
            assistant_response = messages[-1]  # Get last message
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response.content[0].text.value})
            st.chat_message("assistant").write(
                assistant_response.content[0].text.value)

    except Exception as e:
        st.error(f"Error getting response from the assistant: {e}")
