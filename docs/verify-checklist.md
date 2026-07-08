# Verification checklist (from Accio verify-accio-checklist)

- [ ] `config/local.json` exists, `listings_dir` resolves
- [ ] `./scripts/migrate_from_accio.sh` if re-syncing from BuiltByKern
- [ ] `logs/replies.json` valid JSON (`repair_replies_log.py` if Accio duplicate root)
- [ ] `python3 scripts/build_week.py` exits 0
- [ ] `state/week-current.json` `today_key` matches weekday
- [ ] `python3 scripts/trim_logs.py --check` exits 0
- [ ] KERN-Post context = `runtime/post.RUN.md` only
- [ ] KERN-Reply context = `runtime/reply-cycle.RUN.md` only
- [ ] Cron messages = `prompts/cron-*.txt` (no strategy doc)
- [ ] Browser logged in as @builtbykern before first live run
- [ ] `record_post.py` / `record_reply.py` tested once with dummy flags (optional dry run)
