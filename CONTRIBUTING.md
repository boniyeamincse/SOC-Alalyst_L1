# Contributing Guidelines

Thank you for your interest in contributing to the SOC Level 1 Analyst Course!

## Overview

This is a comprehensive SOC L1 training course with 28 modules covering fundamentals through advanced incident response. Contributions are welcome to improve content quality, add real-world examples, or enhance learning materials.

## How to Contribute

### 1. Reporting Issues

Found a mistake or unclear content?
- Open an issue on the repository
- Include module number and specific section
- Explain the problem clearly
- Suggest a fix if possible

### 2. Submitting Content Improvements

**For Module Content:**
1. Identify the module (1-28)
2. Locate the `/modules/module-XX-name/index.md` file
3. Make improvements:
   - Fix typos/grammar
   - Clarify explanations
   - Add real-world examples
   - Improve code blocks or diagrams
4. Submit a pull request with clear description

**For Documentation:**
- Update files in `/docs/` folder
- Keep consistent with existing style
- Update CHANGELOG.md with changes

### 3. Adding Resources

**Playbooks & Runbooks:**
- Add to `/playbooks/` or `/runbooks/`
- Follow module-based organization
- Include clear instructions

**Lab Datasets:**
- Add to `/datasets/`
- Provide documentation
- Ensure lab-related files

**Diagrams:**
- Add to `/diagrams/`
- Use standard formats (PNG, SVG)
- Include descriptions

**Templates:**
- Add to `/templates/`
- Document usage
- Provide examples

### 4. Adding Real-World Examples

- Module sections welcome real SOC examples
- Anonymize sensitive information
- Reference module number
- Explain relevance to learning objective

### 5. Improving Labs

**Beginner Lab (Module 24):**
- Clear scenario setup
- Step-by-step guidance
- Solution walkthrough

**Intermediate Lab (Module 25):**
- Mixed signals/red flags
- Requires investigation
- Multiple verification steps

**Advanced Lab (Module 26):**
- Real incident scenario
- Escalation decisions
- Multiple systems involved

**Capstone (Module 27):**
- Full shift simulation
- Multiple alert types
- Time management practice

## Content Standards

### Writing Style

- **Language:** Bangla-English mixed (প্রয়োজন অনুযায়ী)
- **Tone:** Professional, beginner-friendly
- **Length:** Concise, not rambling
- **Clarity:** Avoid jargon without explanation
- **Examples:** Real-world, practical

### Module Structure

Each module should have:
1. Learning objectives
2. Introduction/story
3. Main content sections
4. Real-world examples
5. Common mistakes
6. Practical checklist
7. Mini-quiz (5-10 questions)
8. Summary

### Code and Diagrams

- Use clear formatting
- Include explanations
- Show expected output
- Provide context

### Assessment Questions

- Clear, unambiguous wording
- 4 multiple-choice options
- One clear correct answer
- Distractors are plausible

## Style Guide

### Headers
```markdown
# Title (Module title only)
## Section (Main topics)
### Subsection (Details)
```

### Formatting
- **Bold:** Important terms
- `Code`: Commands, file names
- > Quote: Important notes
- Lists: Bullet or numbered

### Lists and Boxes
- Use consistent formatting
- Clear hierarchy
- Break up long sections

### Links
- Internal: Relative paths
- External: Full URLs
- Descriptive link text

## Review Process

1. **Submit PR** with clear description
2. **Review** for:
   - Content accuracy
   - Style consistency
   - Grammar/spelling
   - Formatting compliance
3. **Feedback** - respond to comments
4. **Approval** - merge when approved
5. **Release** - update CHANGELOG.md

## Code of Conduct

- Respectful communication
- Focus on content quality
- Support beginner questions
- Share knowledge generously
- Give credit to contributors

## Recognition

Contributors who make substantial improvements will be:
- Listed in course credits
- Mentioned in CHANGELOG.md
- Recognized as course co-authors

## Questions?

- Review existing modules for style examples
- Check CHANGELOG.md for recent changes
- Refer to docs/glossary.md for terminology
- Ask in issue discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as this project.

---

Thank you for helping make this course better for SOC L1 learners worldwide!

Happy contributing! 🛡️
