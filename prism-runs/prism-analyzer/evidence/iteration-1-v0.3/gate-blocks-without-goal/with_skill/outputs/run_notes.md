# Run notes: prism-analyzer, case "gate-blocks-without-goal"

## What happened
- Read `/home/user/prism-analyzer/SKILL.md` and followed it in order: Step 0 (isolation mode), then Step 1 (gate).
- **Stopped at Step 1 (gate).** The user's message describes the system's parts (aiogram bot, SQLite, an hourly cron for reminders, YooKassa, a Google Sheets admin panel the bot re-reads every 5 min, 4 masters with schedules in that sheet). It gives **no Causa Finalis**: there is no Result (what changes in the world) and no Criterion (an observable sign of success or failure). The skill marks both as "Стоп — спросить". Beneficiary and Horizon are also missing; the skill says to ask about them and, without an answer, use an assumption with a mark (`ДОПУЩЕНИЕ`, or "бессрочно").
- Following "Цель, которую можно однозначно вывести… переформулируй и попроси подтвердить", I wrote a draft Result based on what the bot does. I said explicitly that this describes what the bot does, not why it exists, and asked the user to confirm or correct it. The Criterion cannot be inferred from the description at all, so I asked for it directly.
- Checked whether the description covers the minimum per axis and put every gap into the **same single message**, as "Собери всё недостающее в одно сообщение" requires:
  - Formalis: the parts are named, but how they connect is unclear.
  - Materialis: absent (hosting, who maintains the code, payment model, labour spent on the sheet).
  - Efficiens: absent (who edits schedules, cancellation/refund flow, how failures get noticed).
  - Finalis: absent (goal, metrics, incentives).
- Did **not** run Steps 2–8: no survey, no briefs, no vectors, no matrix. I wrote no `prism-runs/` files, because Step 7 only applies once a matrix exists.
- Did not read `references/survey.md` or `vectors/*`, since they are only needed from Step 2 on. Did not read `evals/*`, which is not part of the skill's instructions, to avoid contaminating the run.

## Isolation mode
- **Mode Б (single context)** is the mode I would have used. My toolset had **no Agent/Task subagent tool**. Available tools: Bash, Read, Write, Edit, Glob, Grep, Skill, Artifact, ToolSearch, MCP connectors, SubagentHandback. The deferred-tool list had nothing like Agent or Task either.
- `mcp__claude-code-remote__create_session` was available and can start a fresh cloud session with no inherited context. That could arguably stand in for Mode А. I did not treat it as one, for three reasons: the skill names "Agent / Task" specifically; it creates real sessions in the user's account, a heavyweight side effect; and results would come back asynchronously through send_message/list_events, a loop the skill doesn't describe.
- Per Step 0, the gate message starts with the verbatim Mode Б warning ("Изоляция векторов эмулируется директивами в одном контексте; возможны контекстные протечки между векторами") and a one-line offer of Mode В.

## Places where the skill was unclear or hard to follow
1. **Step 0 vs a gate stop.** Mode Б says to warn the Arbiter "до начала анализа", and Step 1 says to put all questions into one message. The skill doesn't say whether the isolation warning and the Mode В offer belong in a message that stops at the gate. I included them, so the Arbiter can pick Mode В in the same single round and the gate doesn't become two rounds.
2. **"Однозначно вывести" has no threshold.** Here what the bot does is inferable, but why it exists is not: load, no-shows, admin workload or prepayment would each give different fatal points. I offered a draft Result for confirmation rather than demanding a goal from scratch. It is a judgement call whether that counts as "reformulate and confirm" or as "stop and ask".
3. **May the Dispatcher give example criteria?** Examples make the question easier to answer, but they risk anchoring the Arbiter on the Dispatcher's idea of success. The skill is silent on this. I gave neutral templates ("N% of slots", "N% no-shows"…) and asked for the user's own numbers.
4. **Gate questions can leak Dispatcher hypotheses.** The skill bans breach hypotheses in briefs (Step 3) but says nothing about how to word gate questions. Even a neutral question about connections (for example, which of SQLite and Sheets is the source of truth) points the Arbiter, and later the vectors through the Arbiter's answer, at a particular zone. I kept the questions descriptive and avoided failure-scenario examples, but some leakage is unavoidable and the skill gives no guidance on it.
5. **A partly described axis.** The "НЕ АКТИВИРОВАНЫ: нет данных" rule covers an Arbiter who refuses to fill an axis. It doesn't cover an axis that is partly described, like Formalis here (parts listed, connections unclear). The "minimum per axis" isn't operationalised, so it was unclear whether Formalis already passes. I asked anyway.
6. **What counts as a "subagent tool".** Whether a remote-session tool such as `create_session` qualifies as Mode А isn't defined.
7. **Saving state on a gate stop.** Step 7 talks only about input and matrix files after a run. It's unspecified whether `cycle-1-input.md` should be written when the pipeline stops at the gate. I wrote nothing.
