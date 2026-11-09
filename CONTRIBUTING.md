# Contributing to sub-filter

Thanks for wanting to help improve **sub-filter**!  
Whether you’ve found a bug, fixed an issue, or have a cool idea—your help matters.  
Just follow these simple guidelines so everything stays organized and easy for everyone.

---

## 🐞 Found a Bug?

1. **Check if it’s already reported**  
   Look through the existing [Issues](https://github.com/viktor45/sub-filter/issues) to see if someone else has already reported the same problem.

2. **Report it if it’s new**  
   If you don’t see it listed, please [open a new bug report](https://github.com/viktor45/sub-filter/issues/new?template=🐞-bug-report.md).  
   To help us fix it fast, include:
   - A clear **title**
   - A simple **explanation** of what’s wrong
   - Steps to **reproduce the problem**
   - A small **code example** or **test case** showing what should happen vs. what actually happens

---

## 🛠️ Fixed a Bug?

Awesome! We really appreciate it.

- Create a **new Pull Request (PR)** with your fix.
- In your PR description:
  - Explain **what was broken** and **how you fixed it**
  - Mention the issue number if there’s one (like `Closes #42`)
- Keep your code clean and consistent with the rest of the project.

---

## 💡 Have a New Feature Idea or Want to Change Something?

Great ideas are welcome—but let’s talk first!

1. **Share your idea**  
   Open a [feature request](https://github.com/viktor45/sub-filter/issues/new?template=💡-feature-request.md) to describe what you’d like to add or improve.

2. **Wait for feedback**  
   Don’t start coding right away. Give the team and other users a chance to review your idea and give input.  
   We use GitHub Issues mostly for bugs and confirmed improvements, so **please get a thumbs-up before spending time on a big change**.

3. **Once approved—build it!**  
   Fork the repo, write your code, and send a clean, well-documented PR.

---

## 🙏 Thank You!

Every bit of help—whether it’s a typo fix or a big new feature—makes **sub-filter** better for everyone.  
We’re truly grateful for your time and effort!

## Стандарт небольших и проверяемых изменений

Для всех проектов `saymer-alt` действует [общий инженерный стандарт ревью](https://github.com/saymer-alt/saymer-infrastructure/blob/main/docs/engineering-change-review-standard.md). Это правило для **людей и ИИ**, а не файл инструкций агенту.

**Одна проблема → минимальное смысловое исправление → необходимые тесты → один обозримый PR → подтверждение результата.** Не смешивайте hotfix с рефакторингом, переименованиями и посторонними функциями. Если найден другой независимый дефект — отдельное Issue/PR. Размер изменений определяется не количеством строк, а возможностью доказать и проверить их; не отрывайте обязательные тесты и миграции от исправления. Большой неделимый diff требует отдельного обоснования и review. В описании PR указывайте границы, проверки и `NOT_TESTED`; CI PASS не означает field/runtime PASS. Проектные правила безопасности, веток и выпуска сохраняются.
