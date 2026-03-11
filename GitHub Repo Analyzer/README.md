# GitHub Repo Analyzer

A simple Python tool that analyzes any GitHub repository using the GitHub API and displays useful information about the repository.

## 🚀 Features

* Fetch repository details using GitHub API
* Display repository name
* Show primary programming language
* Get repository size
* Check if the repo is a fork
* Display clone URL
* Show number of forks
* Show repository visibility (public/private)
* Display language statistics

## 🛠️ Tech Stack

* Python
* GitHub REST API
* Requests Library

## 📦 Installation

1. Clone the repository

```
git clone https://github.com/your-username/github-repo-analyzer.git
```

2. Install dependencies

```
pip install requests
```

## ▶️ Usage

Run the script:

```
python analyzer.py
```

Example:

```
Enter GitHub Repo URL:
https://github.com/user/repository
```

Output example:

```
Name: Bank-Statement-Analyzer
Language: Python
Fork: False
Size: 10680
Visibility: Public
Clone URL: https://github.com/user/repository.git
Forks: 2
```

## 📚 Future Improvements

* Show top contributors
* Show commit count
* Show open issues and pull requests
* Show repository topics
* Show stars and watchers
* Generate a full repository report