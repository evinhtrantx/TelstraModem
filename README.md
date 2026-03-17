# myapp — Minimal Console Python Application Template

Quick start

- Run the CLI directly:

```bash
python main.py greet --name Alice
python main.py run
python main.py version
```

- Or run as a module:

```bash
python -m myapp greet -n Bob
```

Run tests (requires `pytest`):

```bash
python -m pip install -r requirements.txt
pytest -q
```

Structure

- `main.py` — convenience entry point
- `myapp/` — package containing `cli.py`, `app.py`, and `__main__.py`
- `tests/` — example tests

Selenium example

- The project includes a small Selenium helper at `myapp/selenium_example.py` which uses `webdriver-manager` to download a matching ChromeDriver and launch Chrome/Chromium in headless mode.
- Install deps:

```bash
python -m pip install -r requirements.txt
```

- Quick manual test (requires Chrome/Chromium or Edge installed on the machine):

```bash
python -c "from myapp.selenium_example import fetch_title; print(fetch_title('https://example.com'))"
```

- The Selenium test (`tests/test_selenium.py`) is skipped automatically when no browser binary is found in `PATH` to avoid CI failures.
