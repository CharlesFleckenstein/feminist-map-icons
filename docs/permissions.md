# Role permissions

Access rules for Icon Library.  


| Action | Visitor | Contributor | Moderator | Admin |
|--------|---------|-------------|-----------|-------|
| View published icons | Yes | Yes | Yes | Yes |
| Search/filter icons | Yes | Yes | Yes | Yes |
| Download icons | Yes | Yes | Yes | Yes |
| Sign up for contributor access | Yes | No | No | No |
| Approve contributor accounts | No | No | Yes | Yes |
| Create/draw icon | No | Yes | Yes | Yes |
| Upload icon | No | Yes | Yes | Yes |
| View own submissions | No | Yes | Yes | Yes |
| Edit own draft/pending icon | No | Yes | Yes | Yes |
| Request edit of someone else's icon | No | No | Yes | Yes |
| Delete own unapproved icon | No | Yes | Yes | Yes |
| Delete published icon directly | No | No | Yes | Yes |
| Request edit of own published icon | No | Yes | Yes | Yes |
| Request deletion of own published icon | No | Yes | Yes | Yes |
| Approve icon submissions | No | No | Yes | Yes |
| Reject icon submissions | No | No | Yes | Yes |
| Request changes to submissions | No | No | Yes | Yes |
| Publish icons | No | No | No | Yes |
| Manage/assign contributor approvals | No | No | No | Yes |
| Full CRUD | No | No | No | Yes |

**Notes**

- **Approve ≠ publish:** moderators approve/reject/request changes; only admins publish.
- Admins should be able to create moderators.
- Visitors do not need an account to view/search/download published icons.
- Login method (username/password vs Google) does not replace these roles; roles still apply after sign-in.
