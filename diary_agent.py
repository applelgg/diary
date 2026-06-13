#!/usr/bin/env python3
"""A tiny diary coaching agent for local practice."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MEMORY_PATH = BASE_DIR / "diary_memory.json"
DIARY_DIR = BASE_DIR / "diaries"


@dataclass
class DiaryMemory:
    tone: str = "自然、简短、不鸡汤"
    name: str = "我"
    preferences: list[str] | None = None

    @classmethod
    def load(cls) -> "DiaryMemory":
        if not MEMORY_PATH.exists():
            return cls(preferences=["保留真实口吻", "不要写得太正式"])

        data = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
        return cls(
            tone=data.get("tone", cls.tone),
            name=data.get("name", cls.name),
            preferences=data.get("preferences") or ["保留真实口吻"],
        )

    def save(self) -> None:
        MEMORY_PATH.write_text(
            json.dumps(
                {
                    "tone": self.tone,
                    "name": self.name,
                    "preferences": self.preferences or [],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


class DiaryCoachAgent:
    def __init__(self, memory: DiaryMemory) -> None:
        self.memory = memory

    def needs_follow_up(self, raw: str) -> bool:
        short_text = len(raw.strip()) < 18
        vague_words = ["还行", "没啥", "一般", "不知道", "随便"]
        return short_text or any(word in raw for word in vague_words)

    def follow_up_question(self, raw: str) -> str:
        if "难过" in raw or "烦" in raw or "累" in raw:
            return "今天让你情绪波动最大的那一刻是什么？"
        if "skill" in raw.lower() or "agent" in raw.lower():
            return "今天测试这些能力时，哪个地方最让你有感觉？"
        return "今天最值得记下来的一件小事是什么？"

    def polish(self, raw: str, extra: str = "") -> str:
        details = raw.strip()
        if extra.strip():
            details = f"{details}。补充一下：{extra.strip()}"

        reflection = self._make_reflection(details)

        return (
            f"{date.today().isoformat()}\n\n"
            f"今天主要记一下：{details}\n\n"
            f"{reflection}\n"
        )

    def save_diary(self, content: str) -> Path:
        DIARY_DIR.mkdir(exist_ok=True)
        path = DIARY_DIR / f"{date.today().isoformat()}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def _make_reflection(self, details: str) -> str:
        if "skill" in details.lower() or "agent" in details.lower():
            return "感觉自己是在一点点摸清这些工具的边界：哪些只是新鲜，哪些真的能放进日常里。今天不一定做了很多，但算是往前试了一步。"
        if "难过" in details or "烦" in details or "累" in details:
            return "有些情绪不一定要马上解决，能把它写下来，本身就已经是在照顾自己了。"
        return "日子不一定每天都有大事，但这些零碎的记录，会慢慢帮我看见自己是怎么过来的。"


def run_once(raw: str) -> None:
    memory = DiaryMemory.load()
    memory.save()

    agent = DiaryCoachAgent(memory)
    extra = ""

    if agent.needs_follow_up(raw):
        print(agent.follow_up_question(raw))
        extra = input("> ").strip()

    diary = agent.polish(raw, extra)
    path = agent.save_diary(diary)

    print("\n整理好的日记：\n")
    print(diary)
    print(f"已保存到：{path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="日记陪练 Agent")
    parser.add_argument("text", nargs="*", help="今天的流水账")
    args = parser.parse_args()

    raw = " ".join(args.text).strip()
    if not raw:
        raw = input("今天发生了什么？\n> ").strip()

    run_once(raw)


if __name__ == "__main__":
    main()
