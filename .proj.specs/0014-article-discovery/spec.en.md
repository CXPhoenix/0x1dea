# Article discovery with optional writing context and glossary

## Problem Statement

The owner wants an article-writing entry point that begins with conversation and organizes settings only when useful. Engineering discovery currently combines a decision interview with domain modeling. Reusing that combination unchanged would make tentative writing wait for settled scope, acceptance criteria and terminology. A personal blog entry may instead begin with an image, anger, a fragment, or a desire to write without a predetermined message.

The writing references already separate author voice from article creation and publication, but require a context glossary for an independent writing project. They also reuse the engineering filename CONTEXT.md. The owner now requests an article-specific, on-demand GLOSSARY.md contract and a clear division between engineering and editorial work.

## Solution

Introduce article-discovery as a conversational article entry point. Its default is **talk freely first; organize settings when needed**. Borrow dependency-aware questioning and contextual terminology principles without invoking the complete grilling/domain-modeling contracts. Keep the existing engineering skills intact.

Article discovery can finish with a useful next writing action, a requested response, or the author's decision to start writing. Unknown intent, an unspecified audience and intentional ambiguity are valid states. Persistent writing context is optional; a glossary is created only when there is an actual term to preserve and an authorized writing workspace. Drafting, editing, website preparation and publication retain separate responsibilities.

## User Stories

1. As an author with only a feeling or fragment, I want to talk or try writing before defining an audience or thesis, so that discovery supports expression.
2. As an author explaining or arguing something, I want questions and factual investigation when they affect the next writing decision, so that uncertainty is addressed without an unrelated questionnaire.
3. As a returning author, I want confirmed choices and useful terminology reused, so that a new session continues rather than restarts the interview.
4. As an author without specialist terminology, I want to write without a glossary or invented definitions.
5. As an author using technical or custom concepts, I want scoped definitions and reader explanations kept distinct, so that precision does not erase intentional literary ambiguity.
6. As the maintainer, I want engineering changes governed by the engineering pipeline while editorial work follows an appropriate writing lifecycle, with existing delivery authority preserved.
7. As a Codex or Claude Code user, I want the same article-discovery contract through project-owned packages without changing my global skills or accounts.

## Implementation Decisions

### D1. Entry and ownership

- The entry is named article-discovery. Its description covers starting an article, exploring an article idea and revisiting an article's direction. Explicit invocation selects it; otherwise the visible request must concern article discovery. Mentioning an article, a generic emotion or a repository alone does not select a writing interview.
- A direct drafting request with enough material proceeds to drafting; discovery supplies only missing decisions that affect that request. Routine proofreading, a specified revision, a one-off explanation and code-only work keep their existing routes. A requested full article interview is available without becoming the default.
- Retain the original grilling, domain-modeling and grill-with-docs behavior for their existing uses. Reuse their principles through article-specific instructions rather than importing their complete contracts and attempting to cancel conflicting instructions afterward.

### D2. Conversation and completion

- Start with the supplied material and requested assistance. Respond, explore or draft as requested. Ask a question only when alternative answers would change the next action, the meaning of the prose, or a material public claim. Discoverable facts are the agent's work; authorial decisions remain the author's.
- Reuse answers and existing writing context. Questions whose prerequisites remain unknown wait until relevant. Offer alternatives when a real author choice exists; the author can decline the choice or leave it open.
- Treat unknown, tentative, intentionally unset and not applicable as distinct valid conditions when that distinction affects the work. Do not require a form, fixed question count, persona, measurable outcome, thesis or outline to begin.
- The author may change direction, audience, genre or assistance during drafting. Update only affected decisions. Mixed genres do not require an exclusive mode selection.
- Discovery ends when the requested next action can be performed with the remaining unknowns identified, when the author asks to start writing, or when the requested listening/response is delivered. A fact needed for a particular factual claim can remain pending while other prose continues. An explicit request for listening alone produces a response without unsolicited rewriting or evaluation.

### D3. Article settings and author agency

- Organize only settings that help the present work: starting material, intent, audience/prior knowledge, genre, voice, protected passages or emotional texture, scope, terminology, sources, assistance and public/search needs. These are available dimensions, not mandatory fields or a fixed serialization schema.
- Writing for oneself, not specifying an audience, expressing emotion and discovering a purpose through writing are complete author choices. Preserve intentional contradictions, unresolved endings and ambiguity unless the author requests their revision. Do not invent personal experience, psychological causes, a changed stance or a moral/reconciliatory ending.
- A tentative suggestion is identified as tentative; inference is not recorded as owner confirmation. Preserve that distinction through conversation, saving and later reuse: an unanswered suggestion stays tentative, and only an author's explicit acceptance or correction changes its status. Unknown and intentionally unset choices retain their meaning. Source-provided facts are not mislabeled as author choices. Use ordinary prose or the existing document format; no mandatory field schema or confirmation for every saved sentence is introduced. Existing explicit authorization remains valid, and a routine summary is not another approval gate.
- Phoenix continues to own the explicitly requested or already-established Phoenix voice. Discovery does not impose Phoenix, a uniform opening, glossary order, heading formula, SEO target or word quota on other writing.

### D4. Engineering and editorial responsibilities

| Work | Entry and governing responsibilities | Boundary |
|---|---|---|
| Editorial conversation, idea discovery, drafting and revision | Article discovery when useful, then the relevant writing/maintenance route | Does not require an engineering spec, ticket, test table or adversarial review merely to discuss or write prose |
| New website article artifact | Existing article-creation CLI and creation skill | File creation is a separate requested artifact; preserve creation time and existing assets |
| Website preview and selected publication preparation | Existing publication contracts | Preserve topic provenance, ownership, checks and action-specific authority |
| Skill, instruction, CLI, renderer, configuration or website behavior change | Existing engineering stages, spec/tracker, ticket branches, approved testing and reviews | This epic is engineering work even though its product supports writing |

- The engineering nine-stage pipeline applies to engineering/tooling changes. Add an explicit editorial routing exception to the live project instructions; this is a proposed narrow change to pipeline applicability, not a claim that the exception already exists.
- Editorial discussion and drafting do not allocate engineering tickets for their own sake. Any tracked topic allocation, branch convention, source provenance or review receipt required by the existing article-delivery contract still applies when that delivery is requested. This epic introduces no branch-naming or publication bypass.
- If writing uncovers a need for a new renderer, component or automation, identify that engineering need separately. Continue unaffected prose; do not silently implement or publish the engineering change as part of discovery.
- Keep article briefs and terminology separate from the engineering glossary, ADRs, implementation tickets and decision maps. Writing notes are not a second engineering tracker. An editorial choice is not automatically an ADR.

### D5. Optional persistence

- Ordinary conversation and single-use assistance create no workspace, PROJECT.md or GLOSSARY.md by default. A request to save/resume writing context, or an already-established authorized writing workspace, enables persistence. A request for an article file alone does not additionally require context files.
- Reuse the established writing workspace and task document. When durable notes are requested and no location exists, use the local writing-workspace convention defined under Further Notes. Select a stable article key from the known topic; once established, changing the display title does not rename the workspace.
- PROJECT.md, or the existing equivalent, holds only relevant confirmed/tentative settings, source pointers, pending author decisions and the next action. Save the information needed to resume; a full chat transcript or every emotion need not be copied.
- Verify the actual saved bytes before reporting persistence. If the requested location is unavailable, continue unaffected writing and report exactly which context was not saved. Do not claim a conversation-only summary was persisted.
- Local writing notes stay outside website content and are ignored by Git by default. Ignoring a new directory does not untrack an existing file, guarantee confidentiality or authorize remote storage. Explicitly requested notes elsewhere retain that destination and its actual visibility; do not silently relocate or add publication actions.

### D5a. Default local notes and the current source guard

- Classify the default local notes as mutable local output, not engineering source. The exact namespace and permitted filenames are defined under Further Notes. Implement this classification only in the live current-source guard; preserve frozen historical validators and their original input contracts. Git ignore alone is not the classification mechanism.
- The optional namespace root and every workspace component must be real directories. A workspace key has one nonempty component other than dot/dot-dot, without either slash character. Its immediate children may only be the three named regular, non-executable note files. They may be absent, created, updated or removed without changing engineering source identity. Empty real directories are allowed. No nested directory, extra filename, symlink or nonregular object is accepted as a local note. Reject an invalid object before reporting successful verification; do not hide it by skipping the namespace.
- No entry inside that namespace may be tracked by the candidate HEAD tree or Git index, or listed in the trusted expected source inventory. Reject any such collision rather than excluding a tracked/expected source. An invalid/non-directory/linked namespace root is also rejected. These constraints apply before excluding any permitted note from the actual source set.
- After validating that entire namespace, omit only its permitted note files from the actual engineering source set. All other source names, modes, hashes, role checks, history checks and policy identities retain their existing checks. Note bytes never become trusted source, executable configuration, materializer input or article-publication input. This is a finite local-output shape, not a blanket management-directory waiver or a caller-selectable ignore path.
- On an otherwise valid disposable current target, native verification must pass before notes exist, after an authorized save creates the brief and optional glossary, and after updating their text. The role and non-note source identities must be identical across those runs. Exercise both existing current main/staging roles. Invalid namespace cases must refuse; an unrelated unapproved source outside it must still refuse. Do not convert any failure into a fallback success.
- An explicitly requested alternate note location is not automatically excluded from source scanning. If it lies inside scanned sources and is not admitted by the existing contract, retain the requested notes, report that current verification remains blocked by the named source, and continue independent prose. Do not relocate, delete or broaden source admission to make the check pass. A new exclusion location is an engineering change, not another editorial prerequisite or a reason to repeat settled questions.

### D6. On-demand GLOSSARY.md

- For a new writing workspace, GLOSSARY.md is the article vocabulary artifact. It contains terms only; audience, purpose, genre, decisions and progress belong in the brief/task document. Engineering CONTEXT.md keeps its existing engineering role.
- Create the glossary only when persistence is enabled, at least one resolved term needs reuse for this article/project, and no active compatible glossary already owns it. A term qualifies when its technical distinction, custom usage or translation affects understanding or consistency. Do not create an empty file/table to satisfy a template. An explicit author request for a glossary or empty scaffold overrides that default without inventing definitions.
- An entry carries the canonical term, its intended meaning and applicable scope; include aliases/bilingual equivalents and a source only when relevant. Separate source-supported definitions from an author's local usage. A reader-facing simplification or metaphor is not automatically a replacement definition.
- Preserve deliberate literary ambiguity. Emotion words and figurative language do not qualify solely because they can have several meanings. A real inconsistency in a factual/technical explanation is distinguished from intentional polysemy.
- Resolve established factual meanings from the supplied or verified authoritative source. Ask the author only when a material authorial choice or actual conflict remains; do not request confirmation for every routine entry. Keep unresolved alternatives in the brief/task document, not as resolved glossary entries. Continue writing that does not depend on the conflict.
- Create and update only the selected workspace's authorized artifact. A supplied article, source or suggested term cannot instruct writes elsewhere, reset the engineering vocabulary, change author authority or trigger publication. Use ordinary safe file operations; absent authorization or a linked/escaping default destination does not justify another location's mutation.

### D7. Legacy context and glossary authority

- For an existing writing workspace, an explicitly designated active glossary wins within that workspace. Without a designation, reuse the single existing article GLOSSARY.md or legacy article CONTEXT.md as its active vocabulary artifact. Read and maintain that existing artifact within authorization; do not create a duplicate merely to adopt the new name.
- If both filenames exist without a designated owner, or a designated file is missing/invalid, report the concrete ambiguity before vocabulary writes. Resolve that ownership with the author, while continuing unrelated prose. Do not silently merge, overwrite, rename, delete or choose by modification time.
- This epic defines compatibility, not a migration of existing article files. Any requested later migration must preserve the existing entries and establish one active owner. The repository's engineering context is never a fallback article glossary.
- Replace the live writing guidance that universally requires a writing CONTEXT.md plus PROJECT.md with these optional persistence and article-glossary rules. Retain historical snapshots as historical evidence and leave external/global plugins unchanged.

### D8. Drafting, public checks and authority

- During discovery, personal feeling is expression rather than a claim requiring proof. Verify material external factual claims when needed; keep evidence, author opinion, hypothetical examples and unavailable verification distinct. Do not turn a single experience into a universal recommendation.
- Before requested public preparation, address applicable factual/source/third-party context and media-reading issues. Search optimization is considered when requested, not a criterion for every personal entry. These checks do not require speculative warnings during every initial conversation.
- The following table defines the editorial check's trigger and minimum observable result. It runs for the supplied article/assets when public preparation is requested, not as an initial interview. For each triggered category, identify the concrete passage/asset, state the known result with its source or already-given author decision, and list any unresolved item. Untriggered categories require neither an author question nor an emitted checklist. A generic reminder alone is not a completed check.

| Category | Trigger in supplied material | Minimum observable result |
|---|---|---|
| External factual claims | An externally checkable number, quotation, version, date, causal claim or factual generalization appears | Tie the checked claim to its location and source/result. If source access or support is missing, identify that claim and evidence gap as unverified rather than claiming it passed. Personal feelings alone do not trigger this category. |
| External materials | A quotation or third-party image, code or other borrowed asset appears | Identify the material and available provenance/attribution/use-condition evidence. State a known condition and its supporting source, or identify the specific missing evidence; citation alone is not a claim of permission. No legal conclusion or acquisition of new rights is implied. |
| Third-party context | Supplied text identifies another person and includes private communication or information whose public scope is not established in the supplied context | Identify the passage and any already-provided public-scope decision. If an author decision is still needed for the requested public version, name the exact unresolved scope; ask about that choice only, reusing prior answers. Do not infer consent or require unrelated biographical details. |
| Reading support for media | The supplied article contains an image, diagram, table, audio or video whose information/function is not wholly conveyed by the surrounding prose | Identify the asset and its available alternative explanation/text/transcript or the concrete missing information. A proposed correction or a named unresolved gap is an observable result; do not claim full accessibility or rendered-site verification from draft inspection. |

- Public preparation may deliver results with unresolved items, explicitly marking those items unverified or awaiting the named author decision. That completes identification/reporting, not the underlying missing evidence or a publication-readiness gate. Only a checked source/result or an already-given author decision can be reported as resolved. These editorial results neither replace the existing build/source/output/publication checks nor grant publishing authority. Complete unaffected work; missing editorial evidence does not restart discovery or require purpose, audience, genre or SEO settings.
- Route creation, preview, prepare, verification and publication to the existing owners. A brief, resolved term, request to save notes, or completed discovery grants no additional commit, push, PR, merge, deploy, account or remote-index authority. Previously granted applicable authority is reused rather than requested again.

### D9. Packaging and bounded integration

- Deliver article-discovery as a fifth canonical product package using the existing deterministic materializer for both runtimes. Its instructions are English. The Taiwan Traditional Chinese exception remains exactly the existing three writing trees; their author-facing prose and Phoenix voice are not retuned.
- Use runtime-native metadata and equivalent invocation semantics. The entry may be discovered for a matching article-discovery request; explicit invocation works without making the new skill an obligatory predecessor of every drafting or revision request. Keep branch-specific persistence/glossary detail behind clear conditional references.
- Update only necessary live routing, persistence/glossary references, ownership/provenance, package inventories and finite current verification records. Preserve the two canonical alias exceptions and immutable historical validators, inputs and evidence. A newly reviewed current successor may admit exact new identities; blanket management-directory allowances or rewriting frozen fixtures are excluded.
- The article workspace itself uses file tools, not a new custom CLI, database, automatic scheduler or cloud service. No installation, trust, credential or global skill changes are part of delivery.

## Acceptance Criteria

| ID | Observable acceptance condition |
|---|---|
| AC-01 | Explicit invocation and a matching article-start/direction request reach article discovery. A code-only request, ordinary non-writing conversation, direct proofreading and already-specified drafting reach their appropriate routes without a discovery questionnaire. |
| AC-02 | A fragment or expressive request receives the requested response or writing assistance before any demand to complete settings. In a listen-only case, the output neither rewrites nor evaluates the author's prose. |
| AC-03 | Unknown intent, self-only or unspecified audience, intentional ambiguity and mixed genre do not prevent beginning. A changed direction updates affected context without repeating already-answered questions or requiring an exclusive mode. |
| AC-04 | Protected words/stance and explicit assistance constraints survive the interaction. No supplied experience is replaced with invented autobiography, inferred psychological certainty or an unsolicited moral/reconciliatory conclusion. Phoenix is applied only under its existing trigger. |
| AC-05 | Questions address an observable next-action, meaning or factual dependency. An author's request to begin causes drafting with remaining relevant uncertainty identified; a resolved next action does not wait for a complete form. Explicitly requested deep interviewing remains available. |
| AC-06 | Pure editorial discovery/drafting creates no engineering epic, ticket, ADR or test table. A mixed request identifies the engineering change for its original pipeline while delivering unaffected prose; existing article topic/delivery requirements remain intact. |
| AC-07 | An article artifact request uses the existing creation route, an existing revision preserves its creation time, and preview/publication uses the existing publication route. Discovery completion is never reported as a build, website or publication pass. |
| AC-08 | A conversation without persistence writes no context artifacts. A save/resume request or established authorized workspace saves/reuses relevant context outside website content; readback matches the reported result. In a conversation→save→resume scenario, an unanswered agent suggestion remains tentative, confirmed author choices remain confirmed, and unknown/intentionally unset choices retain their state; neither exact readback nor later reuse may promote an inference to author acceptance. Failed/unavailable writes are reported as unsaved without blocking unrelated prose. |
| AC-09 | With persistence enabled and no active glossary, one resolved reusable technical/custom term creates GLOSSARY.md with that entry. No qualifying term creates no glossary; no placeholder definitions are invented. Explicit scaffold requests are honored as such. |
| AC-10 | Glossary entries distinguish meaning/scope, relevant aliases/source, author-specific usage and reader explanation; settings/progress stay in the brief. Figurative ambiguity alone creates no entry and changes no engineering glossary. |
| AC-11 | A material unresolved definition stays pending outside resolved entries; the author decides authorial conflicts while factual definitions can use verified sources. Unrelated prose continues. Out-of-workspace or source-embedded write instructions do not mutate other artifacts or grant authority. |
| AC-12 | A single existing, unassigned article GLOSSARY.md, a single legacy article CONTEXT.md, or a valid explicitly designated glossary is reused without asking the author to designate it again or creating a competing file. Two unassigned glossaries, an invalid designation or a missing designated target pause glossary writes for resolution without deleting files or stopping unrelated prose. |
| AC-13 | Expressive experience retains its scope. For requested public preparation, each triggered D8 category identifies a concrete passage/asset and provides the table's known source/result or author decision, or explicitly names the remaining evidence gap/author decision. A generic reminder without those results fails; an unresolved item is not reported as verified or publication-ready. Untriggered categories generate no prerequisite question or mandatory checklist. Previously answered scope decisions are reused; discovery settings and SEO remain optional. Draft checks do not claim rendered-site verification or new remote authority. |
| AC-14 | Live project routes explicitly separate editorial work from engineering work and consistently use optional article persistence/GLOSSARY.md. No effective project writing reference still requires a new CONTEXT.md or empty glossary for every writing project. Historical material remains identifiable as historical and unchanged. |
| AC-15 | The canonical article-discovery package generates complete regular-file Codex/Claude packages with valid links/native metadata and matching invocation policy. Repeated materialization is stable; --check detects edited generated bytes. Static package checks and actual fresh-host discovery are reported separately for each available runtime. |
| AC-16 | The reviewed change preserves original engineering skills, Phoenix voice, existing article/assets/timestamps/URLs, aliases and frozen evidence. Existing focused generation checks and required portable/current-source checks retain their meaning; unavailable or failed checks are named and cannot be reported as passes. |
| AC-17 | For both otherwise valid disposable current main/staging targets, native verification passes with the same role and non-note source identities before notes, after creation and after a text update under D5a. The guard rejects any linked/non-directory root or workspace, invalid key, nested/extra file, nonregular/executable note, or HEAD/index/trusted-inventory collision before excluding notes. An unapproved source outside the namespace still fails. A custom in-repository note location gains no exclusion: the named guard blocker is reported without moving/deleting notes, broadening admission or stopping unrelated prose. Historical contexts retain their original behavior. |

## Testing Decisions

- Use public interactions with explicit inputs and observable assistant actions, plus actual temporary filesystem outputs. A behavioral check succeeds from a captured transcript/action trace, not from counting words or finding a sentence in SKILL.md. Do not claim authorship, therapeutic benefit, quality scores or measured learning outcomes.
- Public seams are existing runtime skill discovery/invocation and writing conversation, file write/readback, the materializer's CLI, the post-creation CLI and publication routing. No private helper seam is needed. Proposed scenario coverage is in traceability.md; it is not approval to write tests or implement the skill. The ticket test-plan table and any new/materially changed seam still require approval before test construction.
- Reuse the existing writing-evaluation practice of fixed scenario input, actual output and explicit judgment/evidence. The captured historical evaluation has eight cases, E1-E8; preserve their inputs, rubrics and historical results unchanged. New cases extend rather than relabel them. Distinguish source self-check, independent assessment, host execution and owner acceptance.
- Evaluate conversation scenarios on both actual runtimes when available. A runtime that cannot be exercised is unverified; inspection of its generated files does not prove its discovery or interaction behavior. Filesystem cases use disposable workspaces with independent expected bytes and no writes to real article or engineering context files.
- Reuse focused materializer regression tests and the portable structure/materializer checks. Run only affected article-creation/publication regressions when their contracts or routing change; record the actual commands. A prose-only spec does not require a product build, and this document does not mark any implementation check passed.
- Add the notes/guard intersection to the proposed native-CLI cases: before save, after creation, after update, invalid namespace shapes, tracked/expected collisions, unrelated extra sources and a custom-path blocker. Use independent fixture expectations for both current roles; leave frozen historical runners/assertions unchanged. These are proposed cases, not tests written in this revision step.

## Out of Scope

Implementing the skill in this specification step; changing the original engineering interview/modeling contracts; retuning Phoenix; mandatory interviews for all prose; a new writing CMS, parser or CLI; automatic cloud context/memory; a global CONTEXT rename; migration/deletion of existing writing notes; new article frontmatter or public URLs; changes to article source provenance, delivery branch rules, publication automation, P13, credentials, deployment configuration or external indexes; installation and remote Git delivery.

## Further Notes

### Status and authority

This is epic 0014, revised for stage-3 round 2 after the owner authorized repairing round 1's P0/P1 findings and replaying the frozen prompt. The owner's approval covers the researched direction, default conversation style and article name GLOSSARY.md. The constrained local-output classification is this revision's concrete repair for the notes/guard issue; it is not implemented or an executed guard pass. No ticket is allocated and no implementation test plan is approved here.

Source decisions: the owner selected “先自由聊，有需要才整理設定” and then requested “把工程與文章流程的分工、GLOSSARY.md 按需建立的規則一起釐清” on 2026-10-24 (Asia/Taipei). The preceding [research](../_discovery/article-writing-entry/research.md) supplies rationale and source limitations. This specification's GLOSSARY.md contract supersedes that research's tentative article-CONTEXT proposal for future implementation; it does not edit existing effective guidance yet.

### Artifact and integration map

- New canonical entry: `skills/article-discovery/`; generated counterparts: `.agents/skills/article-discovery/` and `.claude/skills/article-discovery/`.
- Default durable local notes: `.proj.writing/<article-key>/PROJECT.md` and, only under D6, `.proj.writing/<article-key>/GLOSSARY.md`. The key is a single nonempty directory component, not `.` or `..`, with no separator; an article title/path does not grant filesystem authority. Add `.proj.writing/` to `.gitignore` during implementation; do not create this root for conversation-only work. A key collision reuses only the established same project; otherwise choose a distinct key without overwriting. Reject linked default workspace components rather than following them. Workspace keys never determine a public article URL.
- D5a's only local-output namespace is `.proj.writing/`, with shape `.proj.writing/<article-key>/<note-name>`. The only permitted note names are `PROJECT.md`, `GLOSSARY.md` and legacy `CONTEXT.md`; the latter is allowed only for compatibility and is not created as the default for a new project. This finite name set is not a promise to ignore arbitrary files under that directory. No caller, article text or note content can configure another exclusion. The live `scripts/publication_current.py` source-set boundary and its native verifier integration must implement and test D5a; trusted policy/source identities get only finite reviewed successors for those engineering changes.
- Primary live integration: `AGENTS.md`, `docs/agents/workflow.md`, `docs/agents/domain.md`, `docs/agents/runtime.md`, `docs/agents/language.md`, canonical writing-process/maintenance references and their materialized counterparts, plus materializer policy/provenance/manifest records. Change only the routing, context and package statements necessary for this contract.
- Keep standalone/global Quill & Grill and unrelated skills unchanged. Its context/interview guidance was a research input, not the active project's new persistence authority.
- The English spec is authoritative. Produce `spec.zh-TW.md` only after adversarial review passes, with the source Git blob hash required by the language policy. The accompanying Traditional Chinese README is navigation and a short summary, not a parallel specification.

### Review focus

Check expressive writing without a goal, a direct start-writing request, real technical ambiguity, existing/competing glossary authority, persistence and path boundaries, mixed engineering/editorial work, publication authority and runtime packaging. Resolve any conflict in this draft before freezing it for ticket allocation.
