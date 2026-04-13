# Junior Backend Developer Take-Home Assignment

## Scenario

At dibz, we regularly collect queue data from housing platforms and store the latest status in our database.

This small assignment simulates a simplified version of that workflow:

- log in to a housing platform
- fetch a user's account page
- parse queue spot information from HTML
- update our SQLite database with the latest values

The codebase is intentionally **not** production-grade. The goal is to evaluate how you approach a realistic junior backend task using Python.

## What is included

- a local mock housing platform (`mock_platform/`)
- a realistic account HTML page for **Maxim Eyd**
- a seeded SQLite database with a few users
- starter Python modules with a few `TODO`s

## Your task

Implement the missing pieces so that running the sync script will:

1. log into the mock housing platform
2. fetch the account page for the logged-in user
3. parse the queue spot data for **Maxim Eyd**
4. update the SQLite database only for **Maxim Eyd**
5. update `users.last_login` for Maxim when the sync runs

## Queue spot fields to update

For Maxim's queue spots, update the following fields from the HTML page:

- `registration_date`
- `last_updated`
- `update_before`
- `status`
- `inactive_reason` (only when relevant)

## Notes and expectations

- Keep the solution simple and readable.
- Reasonable helper functions and structure are encouraged.
- You do **not** need to build a web API.
- You do **not** need to write perfect tests, but adding a small test or two is welcome.
- You may use `BeautifulSoup`, Selenium, plain string parsing, or a combination.
- The assignment mentions Selenium because we use it in real workflows, but for this exercise you only need enough to show you understand where it fits.

## Small gotchas to notice

A few details are intentionally slightly inconsistent, similar to a real scraped page:

- one queue uses `Reg. date` instead of `Registration date`
- one queue uses `Updated` instead of `Last updated`
- one queue uses `Please refresh before` instead of `Update before`
- status values may differ slightly in casing/spacing
- only inactive queue spots contain an inactive reason

You do not need to over-engineer this. A pragmatic approach is enough.

## Constraints

- only update the records for **Maxim Eyd**
- leave other users and their queue spots unchanged
- keep the schema as-is unless you have a very good reason not to
- assume date values can stay as strings in `YYYY-MM-DD` format

## Suggested time scope

Aim for a solution that would reasonably take a junior developer a couple of hours.

## How to run the assignment

### 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Reset the database

```bash
python scripts/reset_db.py
```

### 3) Start the mock platform

In a separate terminal:

```bash
python mock_platform/server.py
```

The mock platform will run on `http://127.0.0.1:8000`.

### 4) Run the sync script

```bash
cd src
python main.py
```

**Note:** When you first run `main.py`, it will fail with errors. This is expected fixing these errors is part of the assignment.


## Credentials

Use these credentials for the mock platform:

- username: `maxim@example.com`
- password: `test123`

## What we will look for

We will mainly evaluate:

- Python fundamentals
- ability to parse HTML reliably
- basic SQL / SQLite usage
- clean code structure
- sensible handling of edge cases
- overall problem-solving

## Files you will likely touch

- `src/platform_client.py`
- `src/parser.py`
- `src/database.py`

## Bonus ideas (optional)
- normalize status values consistently (`active` / `inactive`)
- show the updated Maxim records after the script finishes
