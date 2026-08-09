# CareerPath India Database Design

## Table 1 : Users

| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary Key |
| full_name | String(100) | Full Name |
| email | String(120) | Unique Email |
| password | String(255) | Hashed Password |
| role | String(20) | Student/Admin/Mentor |
| is_active | Boolean | Active Status |
| created_at | DateTime | Registration Time |