from openai import OpenAI
from flask import current_app


def ask_ai_coach(user, message, history, memories):

    try:

        client = OpenAI(
            api_key=current_app.config["OPENAI_API_KEY"]
        )


        profile = f"""
User Profile

Name:
{user.full_name}

Email:
{user.email}

Bio:
{user.bio or "Not provided"}

Location:
{user.location or "Not provided"}

Skills:
{user.skills or "Not provided"}

Completed Tasks:
{getattr(user, "completed_tasks", 0)}

Rating:
{getattr(user, "rating", 0)}
"""


        memory_context = "\n".join(
            [
                f"- {memory.memory_key}: {memory.memory_value}"
                for memory in memories
            ]
        ) or "No saved memories yet."



        messages = [

            {
                "role": "system",

                "content": f"""
You are Upvanta AI Coach.

You are a professional career assistant.

Help users with:

- Career advice
- Resume improvement
- Interview preparation
- Scholarships
- Job searching
- Freelancing
- Learning paths
- Professional development


Always personalize answers using the user's information.


{profile}


Long-term User Memory:

{memory_context}


Guidelines:

- Give practical answers.
- Be encouraging.
- Recommend realistic next steps.
- Consider the user's background.
- Keep answers clear and useful.
"""
            }

        ]



        for item in history[-50:]:

            role = "assistant"

            if item.role == "user":
                role = "user"


            messages.append(
                {
                    "role": role,
                    "content": item.message
                }
            )



        messages.append(
            {
                "role": "user",
                "content": message
            }
        )



        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=messages,

            max_tokens=600

        )


        return response.choices[0].message.content



    except Exception as e:

        print("AI ERROR:", e)


        return (
            "Sorry, the AI Coach is temporarily unavailable. "
            "Please try again later."
        )