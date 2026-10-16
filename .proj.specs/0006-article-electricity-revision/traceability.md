| Type × field × boundary | Expected behavior | AC |
|---|---|---|
| revision × exact source/type/hash × public CLI | accepts only approved 3 paths | A1 |
| source × byte/mode/missing/link/unknown ignored path × CLI | rejects drift | A2 |
| provenance × record/before/base/history/ancestry × CLI | rejects tampering; preserves epochs | A3 |
| runtime × full checks/review × integrated checkout | all required gates pass | A4 |
| publication × staging SHA/deployment/browser × real remote | verifies actual revision; main/source unchanged | A5 |
