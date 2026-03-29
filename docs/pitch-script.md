# 3-Minute Demo Pitch Script

## 0:00 - 0:30 (The Hook & The Problem)
"We all hate the feeling of leaving a 45-minute meeting, asking 'Who's doing what?', and watching critical action items fall through the cracks because no one was assigned.
Enter **Meeting-to-Execution Autopilot**. It’s not just a meeting summarizer. It’s an autonomous multi-agent system that ingests transcripts, assigns owners, tracks progress, and crucially—recovers when things fail."

## 0:30 - 1:15 (Scenario 1: Ingestion & Orchestration)
*(Action: Open the "Meetings" tab. Show the transcript. Click Send to Pipeline. Go to Tasks.)*
"Here is a raw transcript payload from Zoom. Our Extractor Agent analyzes it, but it doesn't just produce text. It triggers the Orchestrator Agent to create structured JSON tasks. Notice here: the tasks appear instantly. But what happens if an action item doesn't have an owner? Look at this Security Audit task—the Owner Assignment agent flagged it, recognizing it needs an owner, but left it 'Unassigned' due to low confidence."

## 1:15 - 2:00 (Scenario 2: The Health Monitor & Recovery)
*(Action: Go to the "Demo Runner" tab. Click 'Run Scenario 2 - Monitor'.)*
"In a real enterprise, that unassigned task becomes a stalled blocker. Let’s trigger our Health Monitor agent. 
*(Navigate back to Dashboard/Tasks)*
"Instantly, the Health Monitor detected the SLA risk, and passed it to the Recovery Agent! The Recovery Agent automatically escalated the task status to 'Escalated' and updated the priority to high because it contains the keyword 'security'."

## 2:00 - 2:30 (Scenario 3: The Audit Trail)
*(Action: Go to the "Audit Trail" tab.)*
"But AI autonomy is scary for enterprises without visibility. That’s why we built the Audit Trail Agent. Every single decision—the extraction, the stall detection, the escalation—is logged immutably. Look at this line: 'Escalation Agent - High risk task automatically escalated'. You see the Confidence Score and whether Human Approval was required."

## 2:30 - 3:00 (Impact & The Close)
*(Action: Show the Dashboard Metrics)*
"Our impact model shows a 100-person tech company saves $225,000 a year by reclaiming 2.5 hours per manager per week, and rescuing 80% of stalled tasks before they breach SLAs.
This is Agentic AI for true enterprise workflows. Thank you."
