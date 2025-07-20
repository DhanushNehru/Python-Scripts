

# 📁 Save File and Folder to Drive

A simple utility to interact with Google Drive. This project uses the Google Drive API and requires authentication via  `client_secret.json` file.

## 🚀 Features

* Upload files and folders to Google Drive.
* Doesn't change folder structure
* Easy setup for Google Drive API.

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

Make sure you have Python 3 installed.

```bash
pip install -r requirements.txt
```

### 2. Generate `client_secret.json` (Google OAuth Credentials)

To access Google Drive, you’ll need OAuth 2.0 credentials:

1. Go to the **Google Cloud Console**:
   👉 [Create OAuth Credentials](https://console.cloud.google.com/apis/credentials)

2. Steps:
   * Don't forget to check project name, create new project.
   * Search **Google Drive API**, don't get confused with Google Drive Analytics API
   * Click Enable
   * Go to **Credentials** on left sidebar, click **Create Credential** on top and select **OAuth client ID**
   * You might be asked to **configure consent screen**
   * Click on it and click Get Started
   * Add necessary details like app name and emails, Name example: test123
   * Click **Create**
   * Now select **Create OAuth Client**
   * Choose application type as **Desktop app** and leave name as it is
   * Download the JSON file and **rename it to `client_secret.json`**
   * Place the file in the project directory
   * Now you would have to create test user for using this API.
   * Select **Audience** from left Sidebar
   * Add all necessary emails under test email and save it

📝 Official Guide:
[Using OAuth 2.0 for Installed Applications](https://developers.google.com/identity/protocols/oauth2)

---

## ▶️ Running the Script

Once everything is set up:

```bash
python main.py
```

---

## 📎 Notes

* Make sure to enable the **Google Drive API** in your Google Cloud Console.

---

