# Lesson 7: Planning Design Pattern

**Source:** Microsoft AI Agents for Beginners  
**URL:** https://microsoft.github.io/ai-agents-for-beginners/07-planning-design/

## Learning Goals
- Define clear overall goals for agents
- Decompose complex tasks into subtasks
- Use structured output for reliable responses
- Apply event-driven approaches

## The Planning Challenge

Real-world tasks are too complex for single steps. Agents need:
1. Clear objectives
2. Task decomposition
3. Subtask coordination

## Task Decomposition

Split large tasks into smaller, goal-oriented subtasks:

```
"Generate travel itinerary" 
  → Flight Booking
  → Hotel Booking  
  → Car Rental
  → Activities
```

## Structured Output

LLMs can generate JSON for downstream processing:

```python
class TravelPlan(BaseModel):
    main_task: str
    subtasks: List[SubTask]
    is_greeting: bool
```

### Example Output
```json
{
  "main_task": "Plan family trip to Melbourne",
  "subtasks": [
    {"assigned_agent": "flight_booking", "task_details": "Book flights"},
    {"assigned_agent": "hotel_booking", "task_details": "Find hotels"},
    {"assigned_agent": "activities", "task_details": "List activities"}
  ]
}
```

## Multi-Agent Planning Pattern

```
User Request → Planner Agent → Decompose Task 
                            ↓
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
         FlightBot    HotelBot    ActivitiesBot
              ↓             ↓             ↓
              └─────────────┼─────────────┘
                            ↓
                      Compile Results
                            ↓
                      User Response
```

## Iterative Planning

Agents may need to:
- Re-plan based on subtask outcomes
- Adapt to unexpected situations
- Incorporate user feedback

## MIRA Planning Implementation

### 1. Goal Definition
Every MIRA interaction should have clear objectives:
- What does the user want?
- What constraints exist?
- What's the success criteria?

### 2. Task Decomposition
Break complex requests:
```
"Build me a website" 
  → Requirements gathering
  → Design planning
  → Code generation
  → Testing
  → Deployment
```

### 3. Planner Agent (Persona Council Role)
```python
class PlannerAgent:
    def decompose(self, goal: str) -> List[Task]:
        # Use LLM to break down goal
        # Assign to specialized sub-agents
        # Track dependencies
```

### 4. Structured Output for MIRA
```python
@dataclass
class MiraTask:
    id: str
    description: str
    assigned_persona: str
    status: TaskStatus
    dependencies: List[str]
```

### 5. Coordination
- Sequential tasks (must complete in order)
- Parallel tasks (can run simultaneously)
- Conditional tasks (run based on outcomes)

## MIRA-Specific Applications

1. **Shadow Ops Pipeline**
   - Scout → Research → Ground → Pitch → Build → Monetise → Close
   - Each stage is a subtask

2. **Self-Training**
   - Data collection → Processing → Training → Evaluation → Deployment

3. **Client Delivery**
   - Intake → Analysis → Creation → Review → Delivery → Follow-up

---
*Video: https://youtu.be/kPfJ2BrBCMY*
