---
name: job-applier
description: Automated job application assistant. Fetches job descriptions from URLs, tailors CVs for each role, drafts personalized application emails, and prepares everything for submission. Use when user wants to apply to jobs quickly with tailored applications.
---

# Job Applier Skill

## Overview

This skill automates the job application process:
1. Accepts job URLs from user
2. Fetches job description from each URL
3. Tailors the relevant CV for that role
4. Drafts personalized application email
5. Prepares everything ready for submission

## What I Can Do

- ✅ Fetch job descriptions from URLs
- ✅ Analyze job requirements and tailor CV emphasis
- ✅ Draft personalized application emails
- ✅ Match CV to job role
- ✅ Prepare application package (email + CV)

## What I Cannot Do

- ❌ Submit directly to job portals (requires login)
- ❌ Create accounts on job sites
- ❌ Complete CAPTCHAs or interactive forms

## Quick Start

### 1. Get Job Links

Provide a list of job URLs you want to apply for:
```
Apply to these jobs:
- https://jobsite.co.uk/job/12345
- https://indeed.com/job/67890
- https://adzuna.co.uk/job/abcde
```

### 2. I Fetch & Tailor

For each job, I will:
- Fetch the job description
- Match to the best CV from `/home/sir-v/Documents/CV/2026/`
- Tailor the application to highlight relevant skills

### 3. Draft Applications

Applications are saved to:
```
/home/sir-v/MiRA/cv-engine/data/jobs/applications_draft/
```

## CV Files Location

All CVs are stored at:
```
/home/sir-v/Documents/CV/2026/
├── Randolph_Dube_AI_Consultant.pdf
├── Randolph_Dube_ML_AI_Engineer.pdf
├── Randolph_Dube_Data_Engineer_SC.pdf
├── Randolph_Dube_Data_Engineer.pdf
├── Randolph_Dube_Solutions_Architect.pdf
└── Randolph_Dube_Business_Analyst.pdf
```

## CV to Role Mapping

| Role Type | CV File |
|-----------|---------|
| AI / ML / Consultant | `Randolph_Dube_AI_Consultant.pdf` |
| ML Engineer / MLOps | `Randolph_Dube_ML_AI_Engineer.pdf` |
| Data Engineer (SC Cleared) | `Randolph_Dube_Data_Engineer_SC.pdf` |
| Data Engineer / AWS | `Randolph_Dube_Data_Engineer.pdf` |
| Solutions Architect | `Randolph_Dube_Solutions_Architect.pdf` |
| Business Analyst | `Randolph_Dube_Business_Analyst.pdf` |

## Example Usage

### Example 1: Apply to Specific Jobs

```
Apply to these jobs:
1. https://www.jobsite.co.uk/jobs/ai-consultant-london
2. https://www.indeed.com/jobs/data-engineer-leeds
```

### Example 2: Tailor Existing CV

```
Tailor my AI Consultant CV for this job:
https://jobsite.co.uk/job/12345
Focus on: Python, TensorFlow, AWS
```

### Example 3: Check Application Status

```
What applications have we drafted?
```

## Workflow

```
User provides job URLs
        ↓
Fetch job descriptions
        ↓
Analyze requirements
        ↓
Match to best CV
        ↓
Tailor application
        ↓
Draft email + prepare CV
        ↓
Save to applications_draft/
        ↓
User submits manually
```

## File Structure

```
job-applier/
├── SKILL.md                   # This file
├── src/
│   └── job_fetcher.py         # Fetches job descriptions
├── templates/
│   └── application_template.md # Email template
└── applications_draft/         # Created applications
    └── README.md              # Index of drafts
```

## Notes

- Most job sites require manual login to apply
- I prepare everything; you click submit
- Keep job URLs ready for quick application
