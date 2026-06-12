# Event Store CLI Testing Guide

This guide provides a comprehensive list of CLI commands to fully test the CLI utility implemented in [cli.py](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py).

---

## 🛠️ Setup & Environment Activation

Before running the commands, ensure you activate the virtual environment and verify that Python can resolve the packages correctly:

```powershell
# 1. Activate the virtual environment (Windows Powershell)
.\myenv\Scripts\activate

# 2. Run CLI commands as a module to correctly resolve the src package imports
python -m src.cli.cli --help
```

---

## 📖 Available CLI Commands

All CLI commands are defined under [cli.py](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py).

### 1. View Help Context

Displays usage instructions and list of available subcommands.

```powershell
python -m src.cli.cli --help
```

---

### 2. Add an Event

Tests the [store_event](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py#L51) command.

#### Interactive Mode (Prompts for Inputs)

If run without options, it prompts you for the event date and message:

```powershell
python -m src.cli.cli add-event
```

#### Directly Passing Arguments

Pass the date (YYYY-MM-DD) and message directly using `--date`/`-d` and `--message`/`-m` options:

```powershell
# Using full options
python -m src.cli.cli add-event --date "2026-06-12" --message "Successfully created a test event via CLI"

# Using short options
python -m src.cli.cli add-event -d "2026-06-13" -m "Another test event"
```

---

### 3. Add Multiple Events

Tests the [add_multiple_events](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py#L65) command. It automatically inserts events with the current timestamp.

#### Interactive Mode (Prompts for Count)

```powershell
python -m src.cli.cli add-multiple-events
```

#### Directly Passing Count

Use the `--count`/`-c` option:

```powershell
# Add 5 events sequentially
python -m src.cli.cli add-multiple-events --count 5

# Using short option
python -m src.cli.cli add-multiple-events -c 3
```

---

### 4. Get Events (Within Date Range)

Tests the [get_events](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py#L79) command.

#### Interactive Mode (Prompts for Dates)

```powershell
python -m src.cli.cli get-events
```

#### Directly Passing Date Range

Use `--start-date`/`-s` and `--end-date`/`-e`:

```powershell
# Query events between June 1st and June 30th, 2026
python -m src.cli.cli get-events --start-date "2026-06-01" --end-date "2026-06-30"

# Using short options
python -m src.cli.cli get-events -s "2026-06-10" -e "2026-06-15"
```

---

### 5. Get All Events

Tests the [get_all_events](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py#L94) command to fetch every event in storage.

```powershell
python -m src.cli.cli get-all-events
```

---

### 6. Export Events as JSONL

Tests the [export_as_jsonl](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py#L104) command.

#### Interactive Mode (Prompts for output path)

If run without options, it asks you to specify the path (defaults to `exported_events.jsonl` if you press enter):

```powershell
python -m src.cli.cli export-as-jsonl
```

#### Directly Passing Output File

Use `--output`/`-o` to specify a custom output path:

```powershell
# Export to a custom jsonl file
python -m src.cli.cli export-as-jsonl --output "my_exported_events.jsonl"

# Using short option
python -m src.cli.cli export-as-jsonl -o "test_export.jsonl"
```

---

### 7. Interactive Menu Session

Tests the [interactive](file:///c:/Users/salah/Documents/fastapi-test/src/cli/cli.py#L123) command, presenting a numeric text menu to invoke all features continuously without restarting the script.

```powershell
python -m src.cli.cli interactive
```

_Menu Options:_

1. Add event
2. Add multiple events
3. View events in date range
4. View all events
5. Export events as JSONL
6. Exit

---

## ⚙️ Configuration Reference

The CLI behaviour adapts based on variables specified in the [.env](file:///c:/Users/salah/Documents/fastapi-test/.env) file:

- **`STORAGE_TYPE`**: Can be set to `mongodb` or `in_memory`.
- **`MONGO_DB_URI`**: Required if `STORAGE_TYPE=mongodb`.
- **`EVENT_HANDLERS`**: Comma-separated handlers (e.g. `console`, `rabbitmq`).
