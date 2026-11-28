# SQE Project Implementation Plan

Build a maintainable test automation suite for the existing Flask-Ecommerce application using pytest, Selenium WebDriver, and Git. This is the working plan for the two-person team. Track ownership and discussion in the existing GitHub issues. Update this plan as milestones are verified and link to the corresponding PRs and Actions runs.

| Project reference | Location |
| --- | --- |
| Assignment brief | *SQE Project.pdf*, 3 pages. Page 1 covers setup, scope, and the start of the requirements. Page 2 completes the requirements and lists the deliverables. Page 3 contains the weighted rubric and tool list. |
| Original application | [Frost-Codes/Flask-Ecommerce](https://github.com/Frost-Codes/Flask-Ecommerce) |
| Team repository | [SQE-Project-Flask-Ecommerce-Automation](https://github.com/msaimnaveed2005/SQE-Project-Flask-Ecommerce-Automation) |
| Application review | [Feature analysis](FEATURE_ANALYSIS.md) |

**Repository visibility.** The *Project Scope* paragraph on page 1 says public. The setup checklist, Git repository requirement, deliverables, and tools section specify private. This plan follows the repeated private-repository instruction. Confirm the instructor's grading access before submission.

## Current status as of 21 November 2026

| Area | Status | Evidence or next check |
| --- | --- | --- |
| Application selection | Complete | The existing Flask app is cloned locally. |
| Assignment remote | Configured locally | `origin` points to the team repository for fetch and push. Verify repository visibility and the teammate's accepted access on GitHub. |
| Team and work allocation | Reported | Two teammates and ten existing issues, five each. Verify the issue assignees in GitHub and use the existing issue numbers for this plan. |
| Feature analysis | Drafted | `FEATURE_ANALYSIS.md` exists locally and was untracked when reviewed. Include it in a project PR. |
| Application baseline | Partially verified | In the current virtual environment, Flask served home, login, signup, and search. A search submission returned successfully, and a guest cart request redirected. Browser behavior and clean-clone setup remain to be verified. |
| Tests and continuous integration | Pending | No tracked pytest suite, Selenium framework, or Actions workflow was found. pytest and Selenium were absent from the current environment. The installed Flask stack differs from `requirements.txt`. |

**Start here.** Finish the access and issue checks in Step 1 and begin the clean setup in Step 2. The first automation milestone is one unit test and one real browser test passing locally and in Actions. Then expand coverage in parallel.

## 1. Confirm access and agree on test scope

- [ ] Confirm the repository is private and both teammates can clone it, push a branch, and review a pull request.
- [ ] Review the ten existing issues with both teammates. Confirm each has an assignee and an observable acceptance criterion. Record dependencies such as the cart tests requiring a working browser fixture and seeded products.
- [ ] Bring the feature analysis and this plan into the repository through a PR. Add focused ignore rules for virtual environments, generated Python caches, and test outputs.
- [ ] Agree on login, registration, search, and cart as the core browser workflows. Record the inherited limitations in the feature analysis. Product information appears on cards, category links are placeholders, and checkout uses placeholder IntaSend credentials. Treat those limitations as scope notes. Build the suite around supported behavior from the existing application.

**Done when** both teammates have verified access, the existing issues cover the work, and the agreed scope is documented in a reviewed PR.

## 2. Reproduce the application from a clean checkout

- [ ] Pick a Python version and verify a compatible dependency set in a fresh virtual environment. Use the same environment in CI. Document how to install the application dependencies and the separate pytest and Selenium dependencies, such as through `requirements-dev.txt`.
- [ ] Add a minimal configuration override to [`create_app()`](website/__init__.py) so tests can set a temporary SQLite URI before `db.init_app(app)`. Preserve the existing application entry point and default configuration.
- [ ] Create the schema and seed synthetic users and products through fixtures. Give the products predictable names, prices, stock, and flash-sale values. Use independent data for tests that write to the database so reruns and test order do not affect the results.
- [ ] Start Flask on a free loopback port for Selenium and wait for it to serve requests. Make fixture cleanup stop the server and release database resources after failures as well as passes.

**Done when** a clean environment can install the dependencies and start the app against a newly created and seeded test database. [Flask-SQLAlchemy configuration](https://flask-sqlalchemy.palletsprojects.com/en/stable/config/)

## 3. Build the pytest and Selenium framework

Use a small layout with `tests/unit/` for unit tests, `tests/ui/` for Selenium tests, `tests/pages/` for Page Objects, and `tests/conftest.py` for shared fixtures. Keep WebDriver and live-server fixtures scoped to UI tests. Use a root pytest configuration file if needed to make discovery and project options explicit.

- [ ] Implement and reuse fixtures for application configuration, the test database, seeded data, the server URL, and WebDriver. Give each UI test a fresh browser session and quit it during teardown.
- [ ] Start with headless Chrome in CI and a visible mode for local debugging. Keep browser options, base URL, and wait timeout in one place so new workflows can reuse them.
- [ ] Put locators, interaction methods, and methods that read visible values in Page Objects. Keep expected outcomes in test assertions. Prefer stable IDs, field names, or selectors scoped to the page component. Use `WebDriverWait` for a specific condition, such as results becoming visible or a quantity changing after an AJAX request.
- [ ] Prove the framework with one password-verification unit test and one Selenium search test that submits a query from the home page and asserts the seeded product appears.

**Done when** `python -m pytest` runs both tests successfully, the unit suite can run by itself without launching a browser, and a teammate can extend the suite using the existing fixtures and Page Objects. [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) · [Selenium Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/) · [Selenium explicit waits](https://www.selenium.dev/documentation/webdriver/waits/)

## 4. Run both suites in GitHub Actions

- [ ] Add `.github/workflows/tests.yml` once the local smoke tests pass. Trigger it on pushes and pull requests targeting `main`. Include pushes to `main` so merges trigger a run on the resulting `main` commit.
- [ ] Install the same Python and dependencies used locally. Ensure the runner can launch the headless browser and run both suites through pytest. Make the unit and UI results identifiable in the logs. Add failure screenshots if they help diagnose UI failures.
- [ ] Check and link a successful branch-push run, a successful PR check, and a successful run on `main` after merging. Apply the same checks to subsequent implementation PRs.

**Done when** GitHub Actions shows both suites executing on all three occasions. [GitHub Actions workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

## 5. Expand the unit suite

Steps 5 and 6 can run in parallel once the shared framework works. Test existing application logic and use parametrization where cases differ mainly by input or expected result.

| Target | Cases to cover |
| --- | --- |
| Password logic in [`Customer`](website/models.py) | The correct password verifies, an incorrect password fails, and the stored hash differs from the original password. |
| Registration rules in [`SignUpForm`](website/forms.py) | Valid input passes. Missing required fields fail. Test username lengths one and two and password lengths five and six to cover both sides of the minimum. Keep any form-only CSRF override scoped to these tests. |
| Cart calculations, if extracted into a helper used by the app | If a small helper is needed for maintainability, test empty input, a single item, and multiple quantities. Assert the delivery fee where applicable. |

- [ ] Run `python -m pytest tests/unit` and verify that the core test cases exercise the application model or form logic directly.
- [ ] Keep any route-and-database checks identified as integration tests in the documentation and test layout.

**Done when** the unit suite gives passing evidence for positive, negative, and relevant boundary or error cases.

## 6. Expand the Selenium suite

Use seeded data and real browser interactions. For the cart, calculate expected amounts from the fixture's known price and delivery fee and wait for the visible value to change before asserting. Keep the scenarios independent so a failure in signup does not prevent the login or cart tests from running.

| Priority | Workflow | Visible outcomes |
| --- | --- | --- |
| Core | Login | Valid credentials reveal signed-in navigation. A wrong password displays the error and leaves the visitor signed out. |
| Core | Registration | A valid submission displays success and takes the user to login. Reusing a seeded email displays the duplicate-account message. |
| Core | Search | A partial, case-insensitive query displays the expected seeded products and excludes an unrelated product. An unmatched query displays the empty-results message. |
| Core | Cart | Adding a product produces the correct row. Increasing and decreasing quantity updates the quantity and total. Removing the product clears the row. Load the cart again to verify the empty-state message after removing the last item. |
| Useful extension | Home and guest navigation | The home page shows seeded flash-sale products. A guest opening the cart lands on login. |

- [ ] Implement reusable Page Objects or components for the tested pages and shared navigation.
- [ ] Run `python -m pytest tests/ui`, then `python -m pytest`. Run the UI suite again with fresh fixtures to catch state leaks or timing problems. Record reproducible inherited defects in the relevant issue with the expected and observed behavior.

**Done when** the selected workflows pass locally and in CI with meaningful visible assertions for each core scenario.

## 7. Demonstrate collaboration through the existing issues

Use this proposed split to check that the ten existing issues cover the plan. Keep the actual issue titles and numbers as the source for assignment.

| Saim | Teammate |
| --- | --- |
| Feature analysis and test scope | Selenium driver and Page Object foundation |
| Clean application setup and temporary test database | Registration and login UI tests |
| Password and form unit tests | Search UI tests |
| GitHub Actions and post-merge verification | Cart UI tests |
| README and submission evidence | Clean-clone validation and browser test reliability |

- [ ] For each issue, push a branch, open a linked PR to `main`, describe the change and test results, and have the other teammate review it.
- [ ] Verify that each teammate authored and reviewed PRs. Check the `main` workflow after merging and link the run to the milestone here or in the issue.

**Done when** the private repo shows a traceable path from assigned issue to reviewed contribution and passing CI.

## 8. Prepare and verify the final submission

- [ ] Update [`READMe.md`](READMe.md) with application attribution, prerequisites, install and run commands, separate and full test commands, coverage scope, how the fixtures and Page Objects fit together, and how to add a workflow.
- [ ] Have a teammate follow that README from a fresh clone. Verify `python -m pytest tests/unit`, `python -m pytest tests/ui`, and `python -m pytest` all pass.
- [ ] Confirm the private repository on `main` contains the pytest automation project, unit tests, Selenium UI tests, reusable Page Objects and fixtures, project documentation, and the GitHub Actions workflow.
- [ ] Record the final `main` commit and successful Actions run, along with representative reviewed PRs. Confirm grading access with the instructor.

### Final rubric check

| Criterion | Weight | Evidence to verify |
| --- | ---: | --- |
| Functionality | 25% | Passing pytest unit cases and Selenium tests with visible assertions for the selected workflows. |
| Scalability and Flexibility | 25% | Reusable fixtures and Page Objects, predictable seed data, configurable browser setup, and documented instructions for adding a workflow. |
| Code Quality | 25% | Readable modular tests, reusable locators, explicit waits, and fixture-managed setup and cleanup. |
| Test Execution and Integration | 15% | Passing runs from a clean clone and GitHub Actions evidence for branch pushes, PRs, and post-merge `main`. |
| GitHub Usage | 10% | Private repository with both teammates, assigned issues, contributions from branches, reviewed PRs, and visible CI history. |
