from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from . import ai
from .services import ask_ai_coach

from app.extensions import db
from app.models.chat import ChatMessage
from app.models.conversation import Conversation


from .ai_memory import (
    extract_memories,
    get_user_memories
)


@ai.route("/ai-coach")
@login_required
def ai_coach():

    conversations = (
        Conversation.query
        .filter_by(user_id=current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    conversation = None

    if conversations:
        conversation = conversations[0]

    if conversation:
        messages = (
            ChatMessage.query
            .filter_by(conversation_id=conversation.id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )
    else:
        messages = []

    return render_template(
        "ai/coach.html",
        conversations=conversations,
        conversation=conversation,
        messages=messages
    )


@ai.route("/ai-coach/new")
@login_required
def new_chat():

    conversation = Conversation(
        user_id=current_user.id,
        title="New Chat",
        mode="career"
    )

    db.session.add(conversation)
    db.session.commit()

    return redirect(
        url_for(
            "ai.open_chat",
            conversation_id=conversation.id
        )
    )


@ai.route("/ai-coach/<int:conversation_id>")
@login_required
def open_chat(conversation_id):

    conversations = (
        Conversation.query
        .filter_by(user_id=current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=current_user.id
    ).first_or_404()

    messages = (
        ChatMessage.query
        .filter_by(conversation_id=conversation.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    return render_template(
        "ai/coach.html",
        conversations=conversations,
        conversation=conversation,
        messages=messages
    )


@ai.route("/ai-coach/chat", methods=["POST"])
@login_required
def ai_chat():

    message = request.form.get("message", "").strip()

    conversation_id = request.form.get("conversation_id")

    if not message:
        return redirect(url_for("ai.ai_coach"))

    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=current_user.id
    ).first()

    if not conversation:

        conversation = Conversation(
            user_id=current_user.id,
            title="New Chat",
            mode="career"
        )

        db.session.add(conversation)
        db.session.commit()


    user_message = ChatMessage(
        conversation_id=conversation.id,
        user_id=current_user.id,
        role="user",
        message=message
    )

    db.session.add(user_message)

    db.session.commit()


    # Extract important information from user message

    extract_memories(
        current_user.id,
        message
    )


    # Retrieve all saved user memories

    memories = get_user_memories(
        current_user.id
    )

    history = (
        ChatMessage.query
        .filter_by(conversation_id=conversation.id)
        .order_by(ChatMessage.created_at.asc())
        .limit(50)
        .all()
    )

    # Generate personalized AI response

    response = ask_ai_coach(
        current_user,
        message,
        history,
        memories
    )
    

    ai_message = ChatMessage(
        conversation_id=conversation.id,
        user_id=current_user.id,
        role="assistant",
        message=response
    )

    db.session.add(ai_message)

    conversation.updated_at = db.func.now()

    db.session.commit()

    return redirect(
        url_for(
            "ai.open_chat",
            conversation_id=conversation.id
        )
    )


