"""Append learning milestones to ``Activity_Ledger.md`` (F1.3).

Only meaningful milestones are logged (promotions, solved challenges) — never raw
chat. The format matches SRD 6.2 so the ledger stays human-readable and its
``[[WikiLinks]]`` feed back into the knowledge graph.
"""

from __future__ import annotations

import datetime
import os
from dataclasses import dataclass, field

LEDGER_HEADER = "## 📅 Milestone Activity Ledger\n"


@dataclass
class Milestone:
    topic: str
    status: str
    challenge: str = ""
    passed_constraints: str = ""
    detected_weakness: str = ""
    date: str = ""
    tags: list[str] = field(default_factory=list)

    def render(self) -> str:
        day = self.date or datetime.date.today().isoformat()
        lines = [f"### 🟢 {day} | Topic: [[{self.topic}]]",
                 f"- **Status:** {self.status}"]
        if self.challenge:
            lines.append(f"- **Challenge:** {self.challenge}")
        if self.passed_constraints:
            lines.append(f"- **Passed Constraints:** {self.passed_constraints}")
        if self.detected_weakness:
            lines.append(f"- **Detected Weakness:** [[{self.detected_weakness}]]")
        return "\n".join(lines) + "\n"


def append_milestone(ledger_path: str, milestone: Milestone) -> str:
    """Append a milestone block, creating the ledger with its header if absent."""
    exists = os.path.isfile(ledger_path)
    with open(ledger_path, "a", encoding="utf-8", newline="\n") as f:
        if not exists:
            f.write(LEDGER_HEADER)
        f.write("\n" + milestone.render())
    return milestone.render()
