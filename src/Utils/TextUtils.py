"""
Shared text helpers for wrapping long strings into multiple lines that
fit a maximum pixel width, using a given pygame font.
"""

from typing import List

import pygame

def wrap_text(font: pygame.font.Font, text: str, maxWidth: float) -> List[str]:
   
    if not text:
        return []

    words = text.split(" ")
    lines: List[str] = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()

        if current and font.size(candidate)[0] > maxWidth:
            lines.append(current)
            current = word
        else:
            current = candidate

    if current:
        lines.append(current)

    return lines

def format_modifier(key: str, value: int) -> str:
    sign = "+" if value >= 0 else "" 
    return f"{key}{sign}{value}"