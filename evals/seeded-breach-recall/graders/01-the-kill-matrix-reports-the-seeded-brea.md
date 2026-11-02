---
type: llm
focus: trace
weight: 1
---

The Kill Matrix reports, in a block with status ФАТАЛЬНАЯ БРЕШЬ ОБНАРУЖЕНА (in any vector), that production data and all backups can be lost together: the backups live in the same cloud account as production and the production environment holds a key that can delete them, so one incident named in the goal (a production compromise, ransomware, an operator error with that key, or suspension of the account) destroys or locks both
