from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 사용자별 메모리를 저장할 딕셔너리
user_memories = {}

def get_user_memory(user_id: int) -> ConversationBufferMemory:
    """
    사용자 ID 기준으로 단기 기억 인스턴스 가져오거나 새로 생성
    """
    if user_id not in user_memories:
        # InMemoryChatMessageHistory를 명시적으로 설정
        user_memories[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            input_key="input",
            return_messages=True,
            chat_memory=InMemoryChatMessageHistory()
        )
    return user_memories[user_id]