# Shared preview notice retrospective record

Homepage behavior already exists in commit f981af27b4992a938ac9f0065b57b857083e8737, ancestor of selected baseline 32cd6a9d4ead636ddc4e5020fceb35ad9645cc7f. It introduced root envDir, public example/ignore rules, plain title/text props, exact true override and absent/exact staging fallback, global registration, homepage usage and 22 component tests. This record was created after that implementation; it does not claim the original work had these specs, review or TDD beforehand.

The selected article at baseline used a manual info block. T-0004 replaces that block with the same component; the homepage API/flag logic is retained. Pure text, empty suppression and accessible names retain their established contract. New article integration has its own actual red/green record. Production checks use false/main; true/main remains a valid diagnostic override, not an API violation.

Notion #16 is the parent-managed external index, status review according to parent read-only inspection. It is not T-0016. No Notion state or public issue was changed. Actual production deployment is outside this task, and no deployment success or ticket done is inferred from local tests.
