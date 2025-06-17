# CI/CD Pipeline Configuration

This project uses **GitHub Actions** to implement Continuous Integration (CI) and Continuous Deployment (CD) practices.

# Fix issue 
https://github.com/orgs/IIS-ZPI/projects/26/views/1?pane=issue&itemId=115731745&issue=IIS-ZPI%7CZPI2024_IO_CodeBlack%7C77



##  Triggering Events

The pipeline runs automatically on:

- Pushes to: `main`, `release`, `develop`, `feature/**`
- Pull requests targeting: `main`, `release`, `develop`

##  Workflow Overview

The CI/CD process is defined in `.github/workflows/ci.yml`. It consists of two main jobs:

###  Build Job

**Runs on:** `ubuntu-latest`

**Steps:**

1. **Checkout the code**
   Uses `actions/checkout@v4` to retrieve the repository contents.

2. **Set up Python 3.10**
   Uses `actions/setup-python@v3`.

3. **Install dependencies**
   - Upgrade `pip`
   - Install `flake8` `pytest` and `requests` dependencies
   - Install packages listed in `requirements.txt` if it exists

4. **Linting with flake8**
   - Check for critical syntax issues: `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
   - Run style guide checks (non-blocking): `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`

5. **Run unit tests using pytest**
   Executes `pytest` to validate the functionality of the codebase.

###  Release Job

**Conditions:**  
Triggered only when a pull request is merged into the `release` branch **and** the build is successful.

**Steps:**

1. **Checkout the repository**

2. **Set up Python 3.10**

3. **Install build tools**
   Installs `build` for packaging the Python project.

4. **Build the Python package**
   Uses `python -m build` to generate distribution files (`.tar.gz` and `.whl`) in the `dist/` folder.

5. **Tag the release**
   Automatically creates and pushes a tag in the format `v2.<run_number>`.

6. **Upload artifacts**
   Uploads the contents of the `dist/` folder using `actions/upload-artifact@v4`.

##  Artifacts

After each successful release job, distribution files are uploaded as downloadable artifacts via GitHub Actions.

##  Test Automation

- Unit tests run automatically for each push and pull request to `main`, `release`, and `develop`.
- Results are available in the **Actions** tab on GitHub.

##  Instructor Notes

- The pipeline runs only on the `main`, `release`, and `develop` branches.
- Each successful PR to `release` creates a new version tag starting at `v2.0.0` and uploads the build.

##  Project Management

Project managing is handled using GitHub Projects: https://github.com/orgs/IIS-ZPI/projects/26

##  Language

- All documentation, commit messages, and reports are written in **English**, per course guidelines.
