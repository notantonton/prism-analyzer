# Run notes — prism-analyzer, incident-alerting-cycle1 (with_skill)

## Isolation mode: B (single-context emulation)

- I looked for a subagent-launch tool (Agent / Task), including a ToolSearch for "agent task subagent launch". None was available. The deferred tools that exist (SendMessage, TaskStop, worktree tools) message or stop agents that already exist; none of them starts a fresh subagent.
- The environment also has `mcp__claude-code-remote__create_session`, which creates a new Claude Code Remote cloud session. I did not use it as a stand-in for Mode A:
  - it is not a subagent: it creates a persistent session in the user's account, which is a visible side effect;
  - the new session starts in a fresh container that would not have `/home/user/prism-analyzer`;
  - the skill says Mode A means "Agent / Task" and a fresh general-purpose subagent.
- So I ran Mode B:
  - the Mode B warning goes at the top of the reply and again in the `[ИЗОЛЯЦИЯ]` header line;
  - one line offers Mode C;
  - vectors ran one at a time, in descending P, each built only from its own brief plus `vectors/protocol.md` and its own vector file.
- Order of vectors: 1.2, then 3.1, then 4.2. All three scored P=27 with identical S, L and E. The skill gives no tie rule for the Mode B *execution* order, so I used the survey's tie-break chain, which ends at the lower vector number.
- Files read:
  - `SKILL.md`;
  - `references/survey.md`;
  - `vectors/protocol.md`;
  - the three active vector files (1.2, 3.1, 4.2).
- Files not read:
  - the five inactive vector files;
  - the skill's `evals/` folder, to avoid contaminating the run.

## Gate and survey decisions

- **Gate passed.** All four Causa Finalis elements could be read directly from the description.
  - Result and criterion: MTTR sev1 < 30 min, and holding SLA 99.9%.
  - Beneficiary: corporate clients.
  - Horizon: "к концу года", which I read as 31.12.2026, about 2 months from 02.11.2026.
- **No questions asked.** The skill says to restate an inferable goal and ask for confirmation. The user said not to ask, so I recorded the restatement and the missing details as [ДОПУЩЕНИЕ] instead:
  - sev1 definition;
  - how MTTR is computed;
  - SLA window, assumed monthly (≈43 min).
- **Survey result:** 1.2, 3.1 and 4.2 activated (P=27 each).
  - 2.1, 2.2 and 4.1 scored P=18; 3.2 scored P=16; 1.1 scored P=12.
  - There was no tie at the 3rd/4th boundary, so three vectors ran.
- **Judgment calls:**
  - E for 2.2 and 4.2 was raised from 2 (calibration profile) to 3.
  - L for 3.2 was set to 2 using the 2-month horizon correction. With L=3, 3.2 would have reached P=24, still below the cutoff.
  - Both are explained in the "Основания оценок" note under the relief map.

## Where the skill was unclear or hard to follow

1. **Step 7 (saving state) in Mode B.** The text says "Есть файловая система (режим А) — запиши…" and "В режимах Б и В попроси Арбитра сохранить матрицу". It is unclear whether saving depends on having a filesystem or on being in Mode A. Here I was in Mode B *with* a filesystem, so I did both: I wrote `prism-runs/oncall-alerting/cycle-1-{input,matrix}.md` and asked the Arbiter to keep the matrix.
2. **"До начала анализа предупреди Арбитра" in Mode B.** In a single, non-interactive reply with no live user, the only way to do this is to put the warning first in the reply. There is no separate pre-analysis turn.
3. **Gate "попроси подтвердить" vs. the user's "переспрашивать не надо".** The skill does not say what to do when the Arbiter has refused confirmation rounds in advance. I treated this like the Beneficiary/Horizon rule (assumption with a mark) and continued.
4. **Mode B ordering with tied P.** The skill does not specify the order; see above.
5. **"Брешь считается ФАКТОМ, если её суть опирается на цитату".** Support for the 4.2 breach is mixed. The goal-as-metric and the shared cluster are quotes, but the fatal condition rests on assumptions (who sets severity and timestamps, no external SLA measurement, MTTR used to judge the team). I classified it as an ASSUMPTION breach and started its Опора with ДОПУЩЕНИЕ. As a result it sits after the 1.2 FACT breach, even though its index is higher (12 vs 8). The rule is clear, but it is hard to apply when support is mixed.
6. **"Другие фатальные кандидаты".** It is unclear whether the amplifier law counts as a candidate. I did not count it.
7. **Index rationale.** The block format has no place for the reason behind each I/T/D score. I kept the format strict; the reasons appear only indirectly in the mechanics text. An Arbiter who wants to dispute a score has less to work with.
8. **Inherent Mode B tension.** "Сам систему ты не анализируешь" cannot hold in Mode B, because the Dispatcher also writes the vector blocks. The skill acknowledges this only through the leakage warning.
9. **Possible leakage point.**
   - In its "Сигналы для других зон", vector 1.2 (written first) sent 4.2 a signal: if MTTR is counted from the alert, an outage the monitoring misses drops out of the metric.
   - Vector 4.2's mechanism includes a related path ("an incident the monitoring did not see gets a late or no start mark").
   - 4.2's brief independently listed this node as a target («Prometheus и Alertmanager крутятся в том же k8s-кластере, что и прод» — marker "контролёр зависит от контролируемого"), and the main law is 4.2.1 (Goodhart) on the severity and timestamp boundaries.
   - Even so, this sub-path may be context leakage. I did not mark it as a ДУБЛЬ, because the core mechanisms differ: detection stops (1.2) versus the metric replacing the goal (4.2).
10. **Quote discipline.** During the Step 5 check, my own labels in « » (e.g. «MTTR → SLA») looked like citations. I removed the « » from all non-citation labels, so every remaining « » string in the matrix is a verbatim substring of the description; a script confirmed this.
