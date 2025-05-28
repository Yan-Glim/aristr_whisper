import stable_whisper
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = stable_whisper.load_model('base')
result = model.transcribe(f"vedio/output.wav")

output = result.segments

llm = ChatOpenAI(
    model="yangllm:latest",
    base_url="http://localhost:11434/v1",
    api_key="NA",  # 非空值即可
    temperature=0.7,
    streaming=True,
    verbose=True
    )

prompt="""
你是一个好用的翻译助手。请将给定的所有对话内容中的所有非中文的翻译成中文。我发给你所有的话都是需要翻译的内容，你只需要回答翻译结果。翻译结果请符合中文的语言习惯。
Chat history: {history}
input: {input}
"""

prompt=ChatPromptTemplate.from_template(prompt)

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    prompt=prompt,
    memory=ConversationBufferWindowMemory(k=5)  # 设置窗口大小为5防止上下文过长
)

srt_content = ""
for segment in output:
    start_ms = int(segment.start * 1000)  # 将秒转换为毫秒
    end_ms = int(segment.end * 1000)  # 将秒转换为毫秒
    idx = output.index(segment) + 1  # 获取当前段落的索引，从1开始计数
    
    # 将毫秒转换为SRT时间格式（HH:MM:SS,mmm）
    start_time = f"{start_ms//3600000:02d}:{(start_ms//60000)%60:02d}:{(start_ms//1000)%60:02d},{start_ms%1000:03d}"
    end_time = f"{end_ms//3600000:02d}:{(end_ms//60000)%60:02d}:{(end_ms//1000)%60:02d},{end_ms%1000:03d}"
    translate = conversation.predict(input=segment.text).replace("\n", "").replace("<think>", "").replace("</think>", "")
    srt_content += f"{idx}\n{start_time} --> {end_time}\n{translate}\n{segment.text}\n\n"

print(srt_content.strip())


with open("subtitle.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)