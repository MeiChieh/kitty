from typing import Dict, Any, List
from openai import OpenAI  # Assuming OpenAI client is being used


def set_initial_st_state(
    state: Dict[str, Any], initial_vals_dict: Dict[str, Any]
) -> None:
    """
    Sets initial values in the state dictionary if they do not already exist.

    Args:
        state (Dict[str, Any]): The state dictionary to update.
        initial_vals_dict (Dict[str, Any]): Dictionary containing initial key-value pairs to set in state.
    """
    for key, val in initial_vals_dict.items():
        if key not in state:
            state[key] = val


def restart_chat(state: Dict[str, Any]) -> None:
    """
    Resets the chat state by clearing messages and resetting parameters.

    Args:
        state (Dict[str, Any]): The state dictionary containing chat configurations.
    """
    state["messages"] = []
    state["is_first_msg"] = True
    state["temperature"] = 1.5
    state["top_p"] = 0.8
    state["presence_penalty"] = 0.5


def validate_api_key(client: OpenAI) -> bool:
    """
    Validates the API key by attempting to list models.

    Args:
        client (OpenAI): The OpenAI client instance.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    api_key_is_valid = False

    try:
        _ = client.models.list()
        api_key_is_valid = True
    except Exception as e:
        api_key_is_valid = False
        print(f"Error validating API key: {e}")

    return api_key_is_valid


def send_first_message(message_state: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sends the first assistant message to initialize the conversation.

    Args:
        message_state (List[Dict[str, Any]]): List representing the message history.

    Returns:
        List[Dict[str, Any]]: Updated message state including the first message.
    """
    first_msg_1 = """
    Hey, let's practice interview!
    \nDo you already have an interested job description you'd like to prepare for?
    \n- If yes, please paste it below,
    \n- If not, you can say skip.
    """

    message_state.append({"role": "assistant", "content": first_msg_1, "avatar": "😺"})

    return message_state
