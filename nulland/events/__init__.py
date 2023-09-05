
def emit(topic, key, body):
    print(f"emit: {topic} {key} {body}")


def emit_user_action(action, body):
    emit("user_actions", action, body)
