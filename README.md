# aristr_whisper
A simple project fast create str file with langchain memory for learning

个人学习写的简单的asr项目

## 环境
- 使用conda安装虚拟环境使用
- 安装stable_whisper,langchain
```shell
pip install stable-ts langchain langchain-openai
```

## LLM
- 使用openai服务，请勿使用思维链的llm服务，如果使用quwen3可以在prompt或者Modelfile中添加
```text
/no-think
```

## menmory
- 默认使用langchain的思维窗 窗口大小可根据llm自行调整
- 可以使用ConversationBufferMemory(),这样history会包含整个对话信息，可能效果会更好但是幻觉非常严重

## asr
- asr使用的是openai的[whisper](https://github.com/openai/whisper),whisper的时间戳输出在长视频下不准，所以使用的是[stable-ts](https://alibaba-damo-academy.github.io/FunASR/m2met2_cn/index.html)对准的时间戳输出,切换模型可以详见[stable-ts](https://alibaba-damo-academy.github.io/FunASR/m2met2_cn/index.html)
- 尝试过阿里的[funsar](https://github.com/modelscope/FunASR),加上vad模型后的时间戳是字时间戳,也不适用