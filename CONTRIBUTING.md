# Contributing to VideoSummarizerAI

This document outlines the simplified Git workflow for contributing to the VideoSummarizerAI project.

## Branching Strategy

We use a straightforward branching model:

- `main` - The primary branch containing stable code
- Feature branches - Named after the feature or fix they implement

## Contribution Workflow

### Getting Started

1. Clone the repository:
git clone <repository-url>
cd VideoSummarizerAI

2. Create a new branch for your feature or fix:
git checkout -b <feature-name>

Name your branch descriptively, e.g., `audio-extraction-improvement` or `fix-keyframe-bug`

### Development Process

1. Make your changes locally
2. Commit your changes with clear, descriptive messages:
git add .
git commit -m "Add audio format detection"

3. Push your branch to the remote repository:
git push -u origin <feature-name>

4. Create a Pull Request (PR) from your branch to `main`
5. Wait for code review and address any feedback
6. Once approved, your changes will be merged into `main`

### Commit Message Guidelines

Write clear commit messages that explain what changes were made and why:

- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issue numbers if applicable: "Fix #42: Resolve memory leak in video processing"

### Keeping Your Branch Updated

If your feature branch gets behind the main branch:
git checkout main
git pull
git checkout <feature-name>
git merge main

Resolve any conflicts
## Pull Request Process

1. Ensure your code adheres to the project's style and quality standards
2. Update documentation if necessary
3. Include appropriate tests for your changes
4. Fill out the PR template completely

## Git Best Practices

To maintain a clean and useful Git history:
1. **Stay Focused**: Each branch should implement a single feature or fix
2. **Commit Granularly**: Make small, focused commits that do one thing
3. **Write Good Commit Messages**: 
   - First line should be a concise summary (50 chars or less)
   - Optionally followed by a blank line and more detailed explanation
4. **Reference Issues**: Mention issue numbers in commit messages when applicable
5. **Keep Branches Short-lived**: Complete and merge feature branches promptly
6. **Avoid Direct Commits to Main**: Always work in a feature branch, even for small changes
7. **Pull Before You Push**: Always pull the latest changes before pushing to avoid conflicts
8. **Use Pull Requests**: Even as a solo developer, PRs create a review checkpoint