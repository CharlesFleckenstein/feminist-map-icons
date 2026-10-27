# User stories

Product intent for Gallery of Possibilities (Icon Library). Stories follow `docs/permissions.md`. Moderators approve or reject submissions; only admins publish.

---

## Visitor (no account required for browse)

1. As a visitor, I want to open the site and see published icons so that I can explore the library without signing in.
2. As a visitor, I want to search and filter icons (e.g. by tag, designer, or keyword) so that I can find icons that fit my map.
3. As a visitor, I want to open an icon detail page so that I can read description, tags, designer, and related metadata.
4. As a visitor, I want to download PNG and SVG of a published icon so that I can use it in QGIS or other tools.
5. As a visitor, I want to sign up and request contributor access so that I can upload icons after approval.

---

## Contributor (approved account)

6. As a contributor, I want to sign in so that I can access upload and my submissions.
7. As a contributor, I want to create or draw an icon and upload PNG/SVG with metadata so that I can submit it to the library.
8. As a contributor, I want new uploads to start as pending so that they are not public until reviewed and published.
9. As a contributor, I want to see my own submissions (including unpublished) so that I can track review status.
10. As a contributor, I want to edit my own draft or pending icons so that I can fix mistakes before approval.
11. As a contributor, I want to delete my own unapproved icons so that I can remove submissions that should not go forward.
12. As a contributor, I want to request an edit to my own published icon so that maintainers can update it without me changing live content directly. *(later)*
13. As a contributor, I want to request deletion of my own published icon so that maintainers can remove it through review. *(later)*
14. As a contributor, I want clear feedback when upload validation fails (wrong type, too large, etc.) so that I know how to fix the file. *(later — validation issue)*

---

## Moderator

15. As a moderator, I want to view the queue of pending (and in-review) submissions so that I can work through reviews.
16. As a moderator, I want to approve an icon submission so that it is marked ready for an admin to publish. *(approve ≠ publish)*
17. As a moderator, I want to reject an icon submission so that unsuitable uploads do not proceed.
18. As a moderator, I want to request changes on a submission so that the contributor can revise and resubmit.
19. As a moderator, I want to request an edit of someone else’s icon so that corrections can be tracked. *(later)*
20. As a moderator, I want to delete a published icon directly when needed so that harmful or wrong content can be removed.
21. As a moderator, I want to approve contributor account requests so that applicants can upload after review. *(later on website; Django admin grant/revoke is Admin-only for now)*
22. As a moderator, I must not be able to publish icons so that only library admins control what goes live.

---

## Admin

23. As an admin, I want to publish an approved icon so that it becomes visible and downloadable to visitors.
24. As an admin, I want to unpublish or change status when needed so that the live library stays correct.
25. As an admin, I want to grant and revoke contributor access. *(done — admin actions)*
26. As an admin, I want to manage and assign contributor approvals in bulk so that onboarding stays efficient.
27. As an admin, I want to create and manage moderator accounts so that review work can be shared.
28. As an admin, I want full CRUD on icons, tags, and related data so that I can fix anything that roles above cannot.
29. As an admin, I want the same browse/search/download experience as visitors so that I can verify the public library.

---

## Cross-cutting

30. As any signed-in user, I want my role (Contributor / Moderator / Admin) to control what I can do regardless of how I logged in (password or Google later).
31. As a QGIS or API client, I want to read published icons from the same API the website uses so that desktop and web stay in sync.
32. As a site operator, I want imported Zenodo icons to remain published with clear provenance so that the existing collection is usable from day one.

---

## Suggested build order (for planning, not priority votes)

1. Visitor browse, search, detail, download  
2. Contributor sign-in, upload, own submissions, edit/delete pending  
3. Moderator review queue (approve / reject / request changes)  
4. Admin publish + contributor grant/revoke (API/admin already partly done)  
5. Request-edit / request-delete flows and website contributor-approval UI  
