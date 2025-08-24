# Code Review Action

This GitHub Action automatically analyzes pull requests using AI to provide meaningful reviews, suggestions and also gives us a clear signal if the PR is ready to be merged or not.  
This helps developers maintain high code quality, consistency, and prevents tedious cycles of going through poorly documented new code so they can focus on innovating.

## Features
- Automated AI-powered code review on pull requests.
- Analyzes differences and then provide insights and suggestions for improvements.
- Easy to integrate into any repository.

## Setup Guide

1. Clone this repository or download it as a ZIP and extract it into your project ( you only need the .yml file and the main python script) .
2. Copy the `.github/workflows/ai-review-fin.yml` workflow file into your repository of choice under `.github/workflows/`.
3. Create a GitHub secret for your Gemini API key:
   - Go to your repository **Settings > Secrets and variables > Actions**.
   - Add a new secret with the name: `GEMINI_API_KEY`.
   - Add your Gemini key in the provided section.
4. Now whenever you open a pull request in this repository, the action will run and post a review in the comments of that pull request.



## Example

When a pull request is created or updated, the AI Review Fin Action automatically runs and leaves a comment on the PR with AI-generated feedback.

## Contributing
Feel free to open issues or pull requests to improve this project.
