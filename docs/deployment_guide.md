# 🚀 Deployment Guide: Interactive Gradio Stakeholder Dashboard
**Module**: Introduction to Data Science (IDA117V) | Second Semester 2026  
**Project Title**: Municipal Basic Service-Delivery Outage & Infrastructure Vulnerability Triage System  
**Authors**: MM Masemola, B Mdluli, M Mammburu, ME Maleke, PA Mavhungu (Group 14)  

---

## 📌 Executive Overview
The deployment component satisfies **Rubric Question 7 (7 Marks)** by hosting the finalized, locked champion model (`models/champion_pipeline.joblib`) through an accessible, interactive web interface.

The application allows municipal technical directors and dispatch clerks to:
1. Input demographic, operational, and telemetry indicators for any ward in South Africa.
2. Receive immediate, calibrated risk probabilities across all three tiers:
   * **🟢 Low Risk (Routine Service)**
   * **🟡 Moderate Vulnerability (14-Day Inspection)**
   * **🔴 Critical Outage Risk (Immediate Emergency Intervention)**
3. Review plain-language operational guidance and dispatch recommendations.
4. Experience safe boundary error handling with explicit POPIA and ethical compliance notices.

---

## 🖥️ OPTION 1: Running Locally on Your Computer (Current Active State)

The application is **already running in the background** on your computer.

### How to Access Right Now:
Open your preferred web browser (Google Chrome, Microsoft Edge, Firefox) and navigate to:
👉 **[http://127.0.0.1:7860](http://127.0.0.1:7860)**

### How to Launch Manually via Terminal:
```powershell
# Navigate to the project root directory
cd c:\Users\mavhu\.gemini\antigravity\scratch\autograder\ida117v_project

# Run the Gradio app
python src/app.py
```

### One-Click Windows Shortcut:
Simply double-click the included batch script:
👉 `launch_dashboard.bat` (located in the `ida117v_project/` folder). It will start the server and automatically open your default browser.

---

## 🌐 OPTION 2: Generating a Public Shareable Link (For Markers & External Devices)

If you are presenting to lecturers remotely, or want the examiners to test the application from their own laptops or mobile phones without being connected to your local Wi-Fi network:

### How to Launch:
Run the script with the `--share` flag:
```powershell
python src/app.py --share
```
*Or simply double-click*: `launch_public_dashboard.bat`.

### What Happens:
Gradio creates a secure, encrypted tunnel via **Gradio Live** and outputs a publicly accessible HTTPS link:
```text
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://xxxxxxxx.gradio.live  <-- Share this link with your lecturers!
```
* This link is active for **72 hours** as long as your computer remains online and the terminal window remains open.
* Anyone in the world can test the live model directly from their phone or browser.

---

## ☁️ OPTION 3: Permanent 24/7 Cloud Deployment (Hugging Face Spaces)

To deploy the dashboard permanently to the cloud for free with a permanent `.hf.space` URL that stays online 24/7 forever (even when your computer is shut down):

### Step 1: Create a Free Hugging Face Account
1. Visit [https://huggingface.co/join](https://huggingface.co/join) and create a free account.
2. Click on your profile icon in the top right and select **New Space** (or go to [https://huggingface.co/new-space](https://huggingface.co/new-space)).

### Step 2: Configure the Space
* **Space Name:** `sa-municipal-outage-triage` (or your preferred name)
* **License:** `mit` or `cc-by-4.0`
* **Select the Space SDK:** Choose **Gradio**
* **Space Hardware:** Choose **CPU basic (Free - 2 vCPU, 16 GB RAM)**
* **Visibility:** Public
* Click **Create Space**.

### Step 3: Upload the Repository Files
Upload the following files directly into your new Space repository (via web upload or `git push`):
```text
├── app.py                      # (Copy from ida117v_project/src/app.py)
├── models/
│   └── champion_pipeline.joblib # (The saved locked champion pipeline)
├── requirements.txt            # (Specifying gradio, scikit-learn, xgboost, pandas, numpy)
└── README.md                   # (Project documentation and metadata)
```

### Step 4: Live URL
Within 60 seconds, Hugging Face will automatically install the environment, load `champion_pipeline.joblib`, and display the live dashboard at:
`https://huggingface.co/spaces/[your-username]/sa-municipal-outage-triage`

---

## 🧪 Demonstration Verification Scenarios (For Live Presentation)

When presenting to the panel, demonstrate the following four scenarios:

### Scenario 1: Critical Outage Risk (Informal Settlement Grid Overload)
* **Province:** Gauteng
* **Municipality:** City of Johannesburg
* **Settlement Type:** Informal
* **Informal Dwelling (%):** `78`
* **Substation Load Factor:** `1.35` (35% Overload)
* **Unplanned Power Trips (90d):** `16`
* **Service Protest History:** `Checked (Yes)`
* **Output:** 🔴 **[CRITICAL OUTAGE RISK]** (>96% confidence).
* **Action Plan:** Immediate emergency intervention; pre-position water tankers and auxiliary transformers.

### Scenario 2: Routine Suburban Ward (Stable Infrastructure)
* **Province:** Western Cape
* **Municipality:** City of Cape Town
* **Settlement Type:** Formal Urban
* **Piped Water Inside (%):** `98`
* **Substation Load Factor:** `0.62`
* **Water Pipe Bursts:** `1`
* **Power Trips:** `0`
* **Output:** 🟢 **[LOW RISK]** (>98% confidence).
* **Action Plan:** Maintain routine preventative maintenance cycle.

### Scenario 3: Moderate Vulnerability (Aging Pipe Reticulation)
* **Province:** Free State
* **Municipality:** Mangaung
* **Settlement Type:** Formal Town
* **Infrastructure Age (Years):** `38`
* **Substation Load Factor:** `0.95`
* **Water Pipe Bursts (90d):** `5`
* **Power Trips (90d):** `4`
* **Output:** 🟡 **[MODERATE VULNERABILITY]** (~87% confidence).
* **Action Plan:** Schedule on-site technical inspection within 14 days; prioritize thermal scanning.

### Scenario 4: Boundary Validation Error Handling
* Enter a negative population density (e.g. `-500`) or an informal percentage greater than 100% (e.g. `145%`).
* **Output:** ⚠️ **[INPUT VALIDATION FAILED]** with clear, red human-readable feedback. Confirms the application handles errors gracefully without crashing.
