# Traceability

| Type | Field | Boundary | Expected behavior | AC | Test rows |
|---|---|---|---|---|---|
| Published record | exact path/bytes/mode | native CLI, current main/staging | one exact record accepted after pinned publication | AC1 | D01 |
| Published record | deletion, bytes/newline, executable, symlink/parent | native CLI with disposable Git | altered identity rejected | AC2 | D02 |
| Unapproved source | sibling/public/management path, candidate policy | native CLI with candidate mutations | unknown path cannot be self-authorized | AC3 | D03 |
| Historical target | pre-publication ancestry, unavailable pin, query errors and original expected tree | baseline prepare/native verify | old trees require no record; extra record and ancestry errors rejected | AC4 | D04 |
| Historical contract | frozen module/runner bytes, fixed contexts and live fixture materialization | existing current test runner and Git identity | original contracts/assertions execute unchanged; current setup supplies pinned record | AC5 | D05 |
| Preservation | content, aliases, receipts, M0, policy | independent Git identity audit plus native targets | no unrelated or historical changes | AC6 | D06 |
