# 日记陪练 Agent

这是一个很小的本地练手 agent。它会：

- 接收你随手写的几句话
- 内容太少时追问一句
- 按自然、不正式的风格整理成日记
- 保存到 `diaries/日期.md`
- 用 `diary_memory.json` 保存偏好

## 运行

```bash
python3 diary_agent.py "今天使用了几个 skill，测试了 AI 代回复的 skill，还有狗狗你难过"
```

或者直接运行后输入：

```bash
python3 diary_agent.py
```

## 练习方向

1. 给它增加更多追问规则
2. 修改 `diary_memory.json` 里的写作偏好
3. 增加“本周总结”功能
4. 接入大模型 API，让它从规则版升级成真正的 LLM agent
