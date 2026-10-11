# Listing omission diagnosis

The main category index from owner-merged PR #17 is a static bullet and paragraph (SHA-256 7da24230dca20c0a475caef2d616b15a7f56f47443f97eb7e0f8de6963c1f174). It has no NewPost, filter injection or count; the actual built browser showed zero .post-block elements and no date. This is an index template omission, not a missing CSS dependency or article metadata issue.

Staging commit 4005ee45f2f3267a8b53ce24fa97af7b49cfb144 already contains the intended shared listing (SHA-256 5c578e76cdbd84e0d316008e341d56daaa34a0f150237a53a9111bcd58c73d3a), following the existing cybersec category template. The release preparation boundary rejects newly executable Markdown/imports; PR #17 used a static list to stay within that conservative preparation boundary. The publication review verified the link/content but did not require parity with the existing shared category listing. This explains why the article was published but its category row presentation was omitted.

Restore only that exact category index, with the introduction and category-scoped NewPost. The shared component, data loader, article frontmatter/body, assets and category config already exist on main and need no change. The repaired browser shows one electricity row with its original metadata and creation date.

The T-0010 public verifier additionally needs this exact current index successor: validate the original merged release/scope first, then compare this one current path with its fixed new identity. The original scope and historical records remain unchanged. The index is not an unrestricted repair CODE source. A public CLI red control accepted the stale list before the repair; the green control now rejects stale/modified/mode-changed/deleted/linked index inputs. The old historical rejection checks remain active.

No publication CLI restriction is relaxed. The executable Markdown uses the established template and was reviewed, built in a disposable OS sandbox, and exercised in the real local browser. No installation or remote action occurred.
