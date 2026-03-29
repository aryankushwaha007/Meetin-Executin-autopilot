# 3-Minute Live Demo Runbook

**Goal**: Show a fully working app proving end-to-end autonomy, recovery, and auditability in under 3 minutes.

## Preparations
1. Start the app: `docker-compose up` or run the dev servers.
2. Ensure you have the `http://localhost:3000` tab open.
3. Make sure the database is clean (Click the Demo Runner -> Wipe Database).

## Step 1: The Dashboard (0:00 - 0:30)
- **Action**: Open the Homepage Dashboard.
- **Talking Point**: Point to the "Stalled Interventions" and "Autonomous Impact" cards. Explain the $225k ROI from time saved.

## Step 2: Ingestion & Orchestration (0:30 - 1:15)
- **Action**: Go to the "Meetings" tab.
- **Action**: Click the **Send to Pipeline** button located under the text area. Wait 2 seconds for the success message.
- **Action**: Go to the "Tasks" tab.
- **Talking Point**: Show that two tasks have been created. Explain that the Extractor Agent mapped the transcript to structural JSON, and the Orchestrator populated the database.
- **Highlight**: Point out that "Conduct Q3 Security Audit" has NO owner assigned, but the Agent flagged it as High Risk.

## Step 3: Health Monitor & Recovery (1:15 - 2:00)
- **Action**: Go to the "Demo Runner" tab.
- **Action**: Click "Run Scenario 2 & 3 (Health Monitor) 🛡️". This simulates the cron job that runs overnight.
- **Action**: The app will automatically redirect you back to the "Tasks" tab.
- **Talking Point**: Point out that the previously Unassigned "Security Audit" task has now been automatically **Escalated**. The Recovery agent detected it was stalled and high-risk, assigned it to "VP of Engineering," and bumped the status.

## Step 4: The Audit Trail (2:00 - 2:45)
- **Action**: Go to the "Audit Trail" tab.
- **Talking Point**: Scroll through the timeline. Let the judges read the immutable log. Point out the "Escalation Agent" log and explain the Confidence Score metric. Explain that this builds Enterprise Trust, essential for SOC2 environments.

## Step 5: Close (2:45 - 3:00)
- Remind judges: "We've shown autonomous orchestration, self-recovery from failure, and 100% auditability without a single human click."
