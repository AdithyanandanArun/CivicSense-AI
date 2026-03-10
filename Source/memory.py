from db import SessionLocal, Conversation

MAX_HISTORY = 6

def save_message(session_id, role, message):
    db = SessionLocal()
    msg=Conversation(session_id=session_id,role=role,message=message)
    db.add(msg)
    db.commit()
    db.close()


def get_recent_messages(session_id):

    db = SessionLocal()

    messages = (
        db.query(Conversation)
        .filter(Conversation.session_id == session_id)
        .order_by(Conversation.timestamp.desc())
        .limit(MAX_HISTORY)
        .all()
    )

    db.close()

    return list(reversed([
        {"role": m.role, "content": m.message}
        for m in messages
    ]))