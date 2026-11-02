# Машиночитаемая Матрица отказов

`cycle-<N>-matrix.json` — та же матрица, что и `cycle-<N>-matrix.md`, для исправителя-ИИ и для инструментов. Содержание обоих файлов должно совпадать: JSON не добавляет ни оценок, ни выводов. Поле, которого нет в матрице, — `null`, а не выдуманное значение. Простое изложение `cycle-<N>-summary-human.md` (`references/summary-human.md`) — та же матрица для человека: с ней не расходится и ничего к ней не добавляет.

```json
{
  "prism_version": "0.6.0",
  "previous_prism_version": null,
  "system": "oncall-alerting",
  "cycle": 1,
  "causa_finalis": {
    "result": "…", "beneficiary": "…", "criterion": "…", "horizon": "…",
    "assumptions": ["горизонт принят как календарный год"],
    "source": "declared | arbiter | inferred",
    "declared_goal_mismatch": null
  },
  "snapshot": {"kind": "git | archive | copy | none", "ref": "adbca5d | sha256:… | path"},
  "scout": {"mode": "full | light", "files_read": 12, "discrepancies": 3},
  "isolation": "subagents | single-context | manual",
  "roles": "dispatcher-not-fixer | dispatcher-is-fixer",
  "completeness": {
    "status": "measured | not-measured",
    "reason": null,
    "found": 2, "known": 3,
    "probe": [{"vector": "3.1", "case": "3.1-a", "result": "found | missed | other-breach | not-received", "blind": true}],
    "known_breaches": [{"source": "reality | review | fixer | arbiter", "text": "…", "zone": "1.2",
                        "found_as": "B1-1.2-01", "sealed": true}]
  },
  "goal_control": null,
  "center_of_gravity": "…",
  "relief_map": [
    {"vector": "3.1", "E": 3, "S": 3, "L": 3, "modifiers": [], "P": 27,
     "decision": "activated | not-activated | recheck | manual", "signals": ["«цитата»"]}
  ],
  "breaches": [
    {
      "id": "B1-3.1-01",
      "vector": "3.1",
      "mode": "full | recheck | micro",
      "recheck_verdict": null,
      "law": "3.1.6", "amplifier": "3.1.7",
      "essence": "…",
      "localization": "path:line | элемент",
      "basis": "система предполагает, что … | null",
      "evidence": [{"kind": "fact | fact-absence | fact-scout | assumption", "text": "…", "source": "path:line | description | Р2"}],
      "type": "fact | assumption",
      "mechanics": "…",
      "closure_condition": {"state": "…", "check": "…"},
      "probability_pct": [30, 60], "probability_basis": "…",
      "harm_pct": [60, 100], "harm_basis": "…",
      "index": {"I": 2, "T": 2, "D": 2, "value": 8, "I_why": "…", "D_why": "…"},
      "other_candidates": ["3.1.1", "3.1.9"],
      "signals": [{"to": "2.1", "text": "…"}],
      "border_control": []
    }
  ],
  "protected": [{"vector": "2.1", "checked": [{"law": "2.1.3", "why_not_fatal": "…"}],
                 "confirmation": "probe-found | unconfirmed | refuted", "confirmation_basis": "…"}],
  "micro": [{"vector": "1.1", "checked": [{"law": "1.1.4", "why_not_fatal": "…"}],
             "law": "1.1.3", "where": "…", "losses_pct": [5, 10], "losses_basis": "…",
             "confirmation": "probe-found | unconfirmed | refuted", "confirmation_basis": "…"}],
  "open_from_previous": [{"id": "B1-2.2-01", "status": "not-fixed | carried"}],
  "not_activated": [{"vector": "1.1", "P": 12, "reason": "below-cutoff | no-data | open-breach | excluded"}],
  "contradictions": [],
  "duplicates": [],
  "signals_next_cycle": [{"to": "3.2", "from": "1.2 | completeness", "text": "…"}],
  "persistence_warning": true
}
```

Правила:
- `breaches` — в порядке блоков матрицы (шаг 7 SKILL.md); номер `id` постоянный между циклами. Брешь, найденная в режиме МИКРО, — здесь, с `"mode": "micro"`.
- `probability_pct` / `harm_pct` — `null`, если в матрице «не оценивается»; тогда в `*_basis` — чего не хватает.
- `basis` — `null`, если «не выявлено».
- `completeness` — в каждом цикле (`references/completeness.md`). Известных брешей нет — `"status": "not-measured"`, `found` и `known` — `null`, в `reason` — почему. Проба с результатом `not-received` в `found` и `known` не входит. `blind: false` — режим Б; `sealed: false` — сведения Арбитра переданы открыто до съёмки.
- `confirmation` — у каждого элемента `protected` и `micro`; в `confirmation_basis` — результат пробы зоны или пропущенная известная брешь.
- `micro` — только с цикла 2; в примере показан формат элемента.
- `goal_control` (цикл N>1): `{"precision": [a, b], "confirmed_closures": [c, d], "misses": {"independent": e, "found_later": f}}`; `null` на месте показателя — «не определена» / «не измерены», а не лучшее значение.
- `signals_next_cycle` — `"from": "completeness"` для известной бреши, которую прогон пропустил.
- Советов и исправлений в JSON нет — как и в матрице.
