# Backend Implementation Guide - UI-Friendly Features

**For:** Renuka (Backend Lead)  
**To Unblock:** UI Kickoff (Feb 18, 2026)  
**Priority:** All items below must be completed today

---

## Quick Implementation Checklist

### ✅ ITEM 1: Add Pagination to Settings

**File:** `core/settings.py`  
**Time Est:** 2 min

```python
# Add to settings.py (after MIDDLEWARE section):
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 100,
}
```

---

### ✅ ITEM 2: Create Evidence List View with Filtering

**File:** `apps/evidence/views.py`  
**Time Est:** 10 min

**Add this view:**

```python
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import EvidenceFile
from .serializers import EvidenceFileSerializer  # create this

class EvidenceListView(ListAPIView):
    serializer_class = EvidenceFileSerializer
    queryset = EvidenceFile.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['assessment_id', 'question_id', 'uploaded_by']
    ordering_fields = ['created_at', 'expiry_date']
    ordering = ['-created_at']
```

**Add to URLs** `apps/evidence/urls.py`:

```python
path("list/", EvidenceListView.as_view(), name="evidence-list"),
```

---

### ✅ ITEM 3: Create EvidenceFileSerializer

**File:** `apps/evidence/serializers.py` (create if missing)  
**Time Est:** 5 min

```python
from rest_framework import serializers
from .models import EvidenceFile
from datetime import date

class EvidenceFileSerializer(serializers.ModelSerializer):
    expires_in_days = serializers.SerializerMethodField()
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = EvidenceFile
        fields = ['id', 'assessment_id', 'question_id', 'file_url', 'expiry_date',
                  'expires_in_days', 'uploaded_by', 'uploaded_by_name', 'file_type',
                  'org_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_expires_in_days(self, obj):
        if obj.expiry_date:
            return (obj.expiry_date - date.today()).days
        return None

    def get_uploaded_by_name(self, obj):
        # Link to user name if you have user model
        # For now, return ID
        return obj.uploaded_by
```

---

### ✅ ITEM 4: Create User Profile Endpoint

**File:** `apps/common/views.py` (create if missing)  
**Time Est:** 8 min

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileView(APIView):
    """Get current logged-in user profile"""

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = request.user
        org_id = request.headers.get('org-id')

        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'org_id': org_id,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
        })
```

**Add to URLs** `core/urls.py`:

```python
from apps.common.views import UserProfileView

urlpatterns = [
    # ... existing paths ...
    path("api/users/me/", UserProfileView.as_view(), name="user-profile"),
]
```

---

### ✅ ITEM 5: Add Unread Count Endpoint

**File:** `apps/notifications/views.py`  
**Time Est:** 5 min

**Add this view:**

```python
from rest_framework.views import APIView

class UnreadCountView(APIView):
    """Get count of unread notifications"""

    def get(self, request):
        org_id = request.headers.get("org-id")
        unread = Notification.objects.filter(
            org_id=org_id,
            status="unread"
        ).count()
        total = Notification.objects.filter(org_id=org_id).count()

        return Response({
            "unread_count": unread,
            "total_count": total
        })
```

**Add to URLs** `apps/notifications/urls.py`:

```python
path("unread-count/", UnreadCountView.as_view(), name="unread-count"),
```

---

### ✅ ITEM 6: Create Notification Serializer

**File:** `apps/notifications/serializers.py`  
**Time Est:** 5 min

```python
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'org_id', 'user_id', 'type', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'org_id', 'created_at']
```

---

### ✅ ITEM 7: Install Required Packages

**File:** `requirements.txt`  
**Time Est:** 1 min

```
# Ensure these exist in requirements.txt:
djangorestframework
django-filter
```

**Run:**

```bash
pip install -r requirements.txt
```

---

### ✅ ITEM 8: Add EvidenceFile created_at Field

**File:** `apps/evidence/models.py`  
**Time Est:** 5 min

**Current model** is missing `created_at`. Update:

```python
class EvidenceFile(models.Model):
    org_id = models.IntegerField(null=True, blank=True)
    assessment_id = models.IntegerField(null=True, blank=True)
    question_id = models.IntegerField(null=True, blank=True)
    file_url = models.URLField()
    uploaded_by = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # ADD THIS LINE

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Evidence {self.id}"
```

**Run Migration:**

```bash
python manage.py makemigrations evidence
python manage.py migrate
```

---

## Implementation Order (Do in this order)

1. **Settings** (2 min) → Item 1
2. **Models** (5 min) → Item 8 + migration
3. **Serializers** (10 min) → Items 3 + 6
4. **Views** (25 min) → Items 2, 4, 5
5. **URLs** (5 min) → Add all routes
6. **Test in Postman** (10 min) → Verify responses
7. **Total Time:** ~60 min

---

## Testing Checklist

After implementation, test these in Postman:

### Notifications

- [ ] `GET /api/notifications/` → Returns paginated list
- [ ] `PATCH /api/notifications/1/mark-read/` → Status changes to "read"
- [ ] `POST /api/notifications/read-all/` → All become "read"
- [ ] `GET /api/notifications/unread-count/` → Returns correct counts

### Evidence

- [ ] `GET /api/evidence/list/` → Returns paginated evidence
- [ ] `GET /api/evidence/list/?assessment_id=10` → Filters correctly
- [ ] `POST /api/evidence/upload/` → Creates evidence with created_at
- [ ] `GET /api/evidence/list/?ordering=created_at` → Orders correctly

### User

- [ ] `GET /api/users/me/` → Returns current user profile
- [ ] `GET /api/users/me/` (no auth) → Returns 401

---

## Sample Response Formats (For Testing)

### GET /api/notifications/

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/notifications/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "org_id": 101,
      "user_id": 5,
      "type": "evidence_upload",
      "message": "New evidence uploaded",
      "status": "unread",
      "created_at": "2026-02-18T10:30:45.123456Z"
    }
  ]
}
```

### GET /api/evidence/list/

```json
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
      "uploaded_by": 5,
      "uploaded_by_name": 5,
      "file_type": "pdf",
      "org_id": 101,
      "created_at": "2026-02-18T11:45:30Z"
    }
  ]
}
```

### GET /api/users/me/

```json
{
  "id": 5,
  "email": "vendor@company.com",
  "first_name": "John",
  "last_name": "Doe",
  "username": "vendor_user",
  "org_id": "101",
  "is_staff": false,
  "is_active": true
}
```

---

## Sync with Pranjali (QA)

Once done, share:

1. ✅ Postman collection link (with new endpoints)
2. ✅ Sample data with pagination
3. ✅ Evidence list with filters
4. ✅ Confirm /me/ endpoint returns correct role

Pranjali should test:

- [ ] Pagination works (page=1, page=2)
- [ ] Evidence filters by assessment
- [ ] Timestamps in ISO format
- [ ] All response codes (200, 400, 401)

---

## TODO for TODAY (EOD Feb 18)

- [ ] All 8 items implemented
- [ ] Migrations run
- [ ] Postman collection updated
- [ ] Share collection link with UI + Anuja + Pranjali
- [ ] Confirm 409 behavior documented (for Anuja's tracker)
