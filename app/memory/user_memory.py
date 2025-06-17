from langchain.memory import ConversationBufferMemory

# 사용자별 메모리를 저장할 딕셔너리
user_memories = {}

def get_user_memory(user_id: int) -> ConversationBufferMemory:
    """
    사용자 ID 기준으로 단기 기억 인스턴스 가져오거나 새로 생성
    """
    if user_id not in user_memories:
        # 메모리 인스턴스 생성 후 저장 (return_messages=True로 메시지 리스트 반환)
        user_memories[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return user_memories[user_id]