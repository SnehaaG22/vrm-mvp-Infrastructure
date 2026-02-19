# UI Team - Quick API Reference Card

**Date:** Feb 18, 2026  
**Status:** Ready for UI Kickoff  
**Backend Docs:** See `UI_API_DOCUMENTATION.md` for full details

---

## API Base URL

```
http://localhost:8000/api/
```

## Default Headers (ALL Requests)

```
Authorization: Bearer <TOKEN>
org-id: <ORG_ID>
Content-Type: application/json
```

---

## Authentication Endpoints

### Login

```
POST /auth/login/
Body: { "email": "...", "password": "..." }
Response: { "token": "eyJ0eXAi...", "user": {...} }
```

### Get Current User Profile

```
GET /users/me/
Response:
{
  "id": 5,
  "email": "john@vendor.com",
  "first_name": "John",
  "last_name": "Doe",
  "org_id": "101",
  "is_staff": false
}
```

---

## Notifications API

### Get All Notifications (Paginated)

```
GET /notifications/?page=1

Response:
{
  "count": 127,
  "next": "/notifications/?page=2",
  "results": [
    {
      "id": 1,
      "type": "evidence_upload",
      "message": "New evidence uploaded",
      "status": "unread",
      "created_at": "2026-02-18T10:30:45Z"
    }
  ]
}
```

### Mark Single Notification as Read

```
PATCH /notifications/{id}/mark-read/
Response: { "status": "ok" }
```

### Mark ALL as Read

```
POST /notifications/read-all/
Response: { "status": "ok" }
```

### Get Unread Count

```
GET /notifications/unread-count/
Response: { "unread_count": 12, "total_count": 127 }
```

**UI Tip:** Use count endpoint for badge in top nav

---

## Evidence Upload API

### Upload Evidence

```
POST /evidence/upload/

Required body:
{
  "question_id": 42,
  "expiry_date": "2026-12-31",
  "assessment_id": 10,
  "org_id": 101,
  "uploaded_by": 5,
  "file_url": "https://minio.../file.pdf",
  "file_type": "pdf"
}

Response (201):
{
  "detail": "Evidence uploaded",
  "id": 156,
  "created_at": "2026-02-18T11:45:30Z"
}
```

**Validation Rules:**

- ✅ expiry_date & question_id = REQUIRED
- ✅ expiry_date must be in future (YYYY-MM-DD)
- ✅ file_url must be valid URL
- ✅ file_type = pdf, xlsx, jpg, png, docx (suggested)

**Error Examples:**

```
400: { "error": "expiry_date and question_id required" }
400: { "error": "expiry_date cannot be in the past" }
```

### List Evidence (with Filters)

```
GET /evidence/list/
GET /evidence/list/?assessment_id=10
GET /evidence/list/?uploaded_by=5
GET /evidence/list/?ordering=-created_at

Response:
{
  "count": 45,
  "results": [
    {
      "id": 156,
      "assessment_id": 10,
      "question_id": 42,
      "file_url": "https://...",
      "expiry_date": "2026-12-31",
      "expires_in_days": 318,
      "created_at": "2026-02-18T11:45:30Z"
    }
  ]
}
```

**UI Tip:** Use `expires_in_days` field to show warnings (< 30 days = orange, < 7 = red)

---

## 📋 Common Patterns

### Pagination

```
GET /notifications/?page=1&page_size=20
Response includes: count, next, previous, results
```

### Error Handling

```
4xx/5xx Response:
{
  "error": "Human message",
  "detail": "Optional details"
}

Show to user: error.error
Log for debugging: error.detail
```

### Date/Time Handling

```javascript
// Backend sends ISO 8601: "2026-02-18T10:30:45Z"
// Frontend display:
const date = new Date("2026-02-18T10:30:45Z");
date.toLocaleDateString(); // "2/18/2026"
date.toLocaleTimeString(); // "4:00:45 PM" (IST)

// Relative time: "2 hours ago" - use library:
// npm install date-fns react-time-ago
import TimeAgo from "react-time-ago";
<TimeAgo date={date} />; // "2 hours ago"
```

---

## 🎯 Daily Testing Checklist

**Before each sprint:**

- [ ] Login → Get token
- [ ] Call `/users/me/` → Verify role
- [ ] Get Notifications → Verify pagination
- [ ] Mark notification as read → Verify status changes
- [ ] Upload Evidence → Verify response includes id + created_at
- [ ] List Evidence → Filter by assessment_id
- [ ] Check timestamps → Verify ISO format

---

## 🆘 Common Issues & Fixes

| Issue                                    | Fix                                               |
| ---------------------------------------- | ------------------------------------------------- |
| **401 Unauthorized**                     | Check token in Authorization header               |
| **Missing org-id header**                | Add `org-id: <value>` to headers                  |
| **Empty results**                        | Check filter params, try without filters first    |
| **Pagination returns 0 results**         | Make sure data exists, try page=1                 |
| **"creation_failed" on evidence upload** | Verify question_id exists + expiry_date is future |

---

## 📞 Support

- **API Questions?** → Check `UI_API_DOCUMENTATION.md`
- **Backend Issues?** → Reach out to Renuka
- **Missing Endpoint?** → Check `BACKEND_IMPLEMENTATION_GUIDE.md` for TODOs
- **UI Feature Questions?** → Sync in standup

---

## Sample cURL Commands (Testing)

### Get Notifications

```bash
curl -X GET "http://localhost:8000/api/notifications/?page=1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "org-id: 101"
```

### Upload Evidence

```bash
curl -X POST "http://localhost:8000/api/evidence/upload/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "org-id: 101" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 42,
    "expiry_date": "2026-12-31",
    "assessment_id": 10,
    "org_id": 101,
    "uploaded_by": 5,
    "file_url": "https://minio.../file.pdf",
    "file_type": "pdf"
  }'
```

### Mark Notification as Read

```bash
curl -X PATCH "http://localhost:8000/api/notifications/1/mark-read/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "org-id: 101"
```

---

**Last Updated:** Feb 18, 2026  
**Next Sync:** Daily at 10 AM IST
