---
title: BrowserOS + Hermes Agent Integration Guide
icon: lucide/globe
description: Complete guide to integrating BrowserOS (agentic browser) with Hermes Agent for autonomous web automation, research, data extraction, and monitoring.
keywords:
  - browseros
  - hermes
  - AI agent
  - agentic browser
  - MCP
  - web automation
  - browser automation
  - Nous Research
---

![BrowserOS + Hermes Agent](/assets/images/browseros/hermes-browseros-banner.png){ width=900 }

BrowserOS is an agentic browser — a Chrome-based browser with a built-in MCP (Model Context Protocol) server that exposes 66+ browser automation tools to AI agents. When paired with Hermes Agent, you get autonomous web control through natural language.

## Introduction

### What is BrowserOS?

BrowserOS is an AI-native browser built on Chromium (version 146) that provides:

| Feature             | Description                                                              |
| :------------------ | :----------------------------------------------------------------------- |
| **MCP Server**      | Built-in server on `localhost:9201` exposing all tools via JSON-RPC      |
| **Tab Management**  | Group, organize, move tabs with full metadata                            |
| **Hidden Tabs**     | Run background automation without disturbing user's view                 |
| **Bookmarks API**   | Full CRUD on browser bookmarks                                           |
| **History API**     | Search and manage browsing history                                       |
| **Tab Groups**      | Organize tabs into colored groups                                        |
| **Built-in Skills** | 12 pre-built workflows (deep-research, extract-data, monitor-page, etc.) |
| **Screenshots**     | Full-page and element-level screenshots                                  |
| **PDF Export**      | Save any page as PDF                                                     |
| **Connect Apps**    | Integration with 40+ services (Gmail, GitHub, Slack, etc.)               |

!!! tip "Why Use BrowserOS with Hermes?"

<!-- markdownlint-disable-next-line MD046 -->

    - **Natural language control** — Tell Hermes what to do in the browser, and it executes autonomously
    - **Persistent browser state** — Browser tabs, history, bookmarks, and sessions persist across conversations
    - **MCP-first design** — Tools are exposed standards-compliant for any MCP client
    - **Local privacy** — All browsing stays on your machine; no external proxies

### When to Use BrowserOS vs Hermes Browser Tools

| Use Case                             | Tool                                                |
| :----------------------------------- | :-------------------------------------------------- |
| **Complex multi-step workflows**     | BrowserOS MCP tools — full control, persistent tabs |
| **Quick URL checks**                 | Hermes built-in browser — simpler, ephemeral        |
| **Research, extraction, monitoring** | BrowserOS — stateful, resumable                     |
| **Simple navigation + screenshot**   | Either works                                        |

---

## Integration Setup

### Prerequisites

1. **BrowserOS installed** — AppImage in `~/Downloads/browseros` or extracted to `~/.local/bin/browseros`
2. **Hermes Agent** with MCP support — Python venv with `mcp` package
3. **Config updated** — MCP server added to `~/.hermes/config.yaml`

### Quick Start

1. Browse to the BrowserOS AppImage and run it:

   ```bash
   ~/Downloads/BrowserOS
   ```

2. Wait for the browser window to open and the server to start.

3. Verify the MCP server is running:

   ```bash
   curl http://127.0.0.1:9201/health
   # Returns: {"status": "ok", "cdpConnected": true}
   ```

4. Ensure Hermes config has the MCP server:

   ```yaml
   # ~/.hermes/config.yaml
   mcp_servers:
     browseros:
       url: "http://127.0.0.1:9201/mcp"
       timeout: 120
       connect_timeout: 30
   ```

5. Restart Hermes to pick up the config:

   ```bash
   hermes
   ```

!!! warning "Common Setup Issues"

<!-- markdownlint-disable-next-line MD046 -->

| Issue                  | Solution                                   |
| :--------------------- | :----------------------------------------- |
| MCP connection refused | Start BrowserOS: `~/Downloads/BrowserOS`   |
| Tools not appearing    | Restart Hermes Agent in a new session      |
| Timeout errors         | Increase timeout in config: `timeout: 180` |

### Verification

After restart, you should see:

```
MCP servers have been reloaded. Added servers: browseros.
70 MCP tool(s) now available.
```

Tools are now available as `mcp_browseros_<tool_name>` (e.g., `mcp_browseros_navigate_page`).

---

## Tool Categories

BrowserOS exposes 66 tools across 7 categories:

### 1. Page/Tab Management

| Tool              | Description                               |
| :---------------- | :---------------------------------------- |
| `get_active_page` | Get the currently active (focused) page   |
| `list_pages`      | List all open tabs                        |
| `navigate_page`   | Navigate to URL, or back/forward/reload   |
| `new_page`        | Open a new tab (background by default)    |
| `new_hidden_page` | Open a hidden tab for background work     |
| `show_page`       | Restore a hidden tab to visibility        |
| `move_page`       | Move a tab to a different window/position |
| `close_page`      | Close a tab                               |

### 2. Content Extraction

| Tool                     | Description                                |
| :----------------------- | :----------------------------------------- |
| `take_snapshot`          | Get interactive element IDs for automation |
| `take_enhanced_snapshot` | Detailed accessibility tree with context   |
| `get_page_content`       | Extract clean markdown content             |
| `get_page_links`         | Extract all links as `[text](url)`         |
| `get_dom`                | Get raw HTML DOM structure                 |
| `search_dom`             | Search DOM with text/CSS/XPath             |
| `get_console_logs`       | Get browser console output                 |

### 3. Interaction

| Tool            | Description                         |
| :-------------- | :---------------------------------- |
| `click`         | Click an element by snapshot ID     |
| `click_at`      | Click at coordinates                |
| `hover`         | Hover over an element               |
| `hover_at`      | Hover at coordinates                |
| `type_at`       | Type at coordinates                 |
| `drag_at`       | Drag from one coordinate to another |
| `focus`         | Focus an element                    |
| `clear`         | Clear input text                    |
| `fill`          | Type into an input                  |
| `check`         | Check a checkbox/radio              |
| `uncheck`       | Uncheck a checkbox                  |
| `upload_file`   | Upload file to input                |
| `press_key`     | Press a key/key combo               |
| `drag`          | Drag from element to element/coords |
| `scroll`        | Scroll page or element              |
| `handle_dialog` | Accept/dismiss JS dialog            |
| `select_option` | Select dropdown option              |

### 4. Media & Export

| Tool              | Description                |
| :---------------- | :------------------------- |
| `take_screenshot` | Screenshot of current page |
| `save_pdf`        | Save page as PDF           |
| `save_screenshot` | Screenshot to file         |
| `download_file`   | Click to download file     |

### 5. Window Management

| Tool                   | Description          |
| :--------------------- | :------------------- |
| `list_windows`         | List all windows     |
| `create_window`        | Create new window    |
| `create_hidden_window` | Create hidden window |
| `close_window`         | Close window         |
| `activate_window`      | Focus window         |

### 6. Bookmarks

| Tool               | Description               |
| :----------------- | :------------------------ |
| `get_bookmarks`    | List all bookmarks        |
| `create_bookmark`  | Create bookmark or folder |
| `remove_bookmark`  | Remove bookmark/folder    |
| `update_bookmark`  | Update title/URL          |
| `move_bookmark`    | Move to folder            |
| `search_bookmarks` | Search by title/URL       |

### 7. History

| Tool                   | Description          |
| :--------------------- | :------------------- |
| `search_history`       | Search history       |
| `get_recent_history`   | Recent items         |
| `delete_history_url`   | Delete specific URL  |
| `delete_history_range` | Delete by date range |

### 8. Tab Groups

| Tool               | Description                  |
| :----------------- | :--------------------------- |
| `list_tab_groups`  | List all groups              |
| `group_tabs`       | Group tabs                   |
| `update_tab_group` | Update title/color/collapsed |
| `ungroup_tabs`     | Remove from group            |
| `close_tab_group`  | Close group and tabs         |

### 9. Script Execution

| Tool              | Description                        |
| :---------------- | :--------------------------------- |
| `evaluate_script` | Execute JavaScript in page context |

### 10. Connect Apps (40+ integrations)

| Tool                                    | Description                  |
| :-------------------------------------- | :--------------------------- |
| `discover_server_categories_or_actions` | Discover available services  |
| `get_category_actions`                  | Get actions for a category   |
| `get_action_details`                    | Get action parameters        |
| `execute_action`                        | Execute a Connect App action |
| `handle_auth_failure`                   | Handle auth errors           |

---

## Practical Examples

### Example 1: Quick Page Summary

**Request:**

> "Summarize the current state of quantum computing from Wikipedia"

**Tools used:**

1. `navigate_page` → go to Wikipedia quantum computing page
2. `get_page_content` → extract clean markdown
3. Summarize the content

### Example 2: Multi-Source Research

**Request:**

> "Research the best noise-canceling headphones from 5 sources and create a comparison table"

**Workflow:**

1. Create workspace: `create_hidden_window`
2. Open 5 hidden tabs: `new_hidden_page` × 5
3. Navigate each: `navigate_page`
4. Extract: `get_page_content` or `evaluate_script`
5. Save each: write to `raw/`
6. Close: `close_page`
7. Merge: Read all raw files, create `merged.csv`
8. Report: Generate `report.html`

### Example 3: Product Price Tracking

**Request:**

> "Track the price of 'NVIDIA RTX 5090' on Amazon, Newegg, and Best Buy. Alert me if any drop below $1000."

**Workflow:**

1. Create 3 hidden tabs for each retailer
2. Navigate to product pages
3. Use `evaluate_script` to extract price text
4. Save price history to a local file
5. Compare against threshold
6. Alert user if condition met

### Example 4: Form Submission

**Request:**

> "Fill out the signup form at example.com/signup with test credentials"

**Tools used:**

1. `navigate_page` → go to form
2. `take_snapshot` → get element IDs
3. `fill` → fill name/email fields
4. `select_option` → select dropdown
5. `click` → submit button
6. `handle_dialog` → accept confirmation

### Example 5: Bookmarks Management

**Request:**

> "Create a bookmark folder for 'AI Research' and save these 5 URLs as bookmarks inside it"

**Workflow:**

1. `create_bookmark` → create folder
2. `create_bookmark` × 5 → add each URL with the folder ID

### Example 6: Screenshot Walkthrough

**Request:**

> "Create a step-by-step screenshot walkthrough of logging into Gmail"

**Workflow:**

1. `new_page` → navigate to Gmail
2. `take_snapshot` → get login elements
3. `save_screenshot` → capture each step
4. Continue until logged in
5. Compile into markdown with image paths

---

## Built-in Skills

BrowserOS comes with 12 built-in skills at `~/.browseros/skills/builtin/`:

| Skill                    | Description                                         |
| :----------------------- | :-------------------------------------------------- |
| `deep-research`          | Multi-source research with HTML report + PDF        |
| `extract-data`           | Extract structured data (tables, products, pricing) |
| `monitor-page`           | Track changes on a web page over time               |
| `compare-prices`         | Compare prices across multiple retailers            |
| `find-alternatives`      | Find alternative products/services                  |
| `fill-form`              | Automate form filling and submission                |
| `save-page`              | Save pages for offline reading                      |
| `read-later`             | Queue pages to read later                           |
| `manage-bookmarks`       | CRUD on bookmarks                                   |
| `organize-tabs`          | Organize tabs into groups                           |
| `screenshot-walkthrough` | Document workflows with screenshots                 |
| `summarize-page`         | Extract and summarize page content                  |

---

## Advanced Workflows

### A. Deep Research (Multi-Day)

BrowserOS has a built-in `deep-research` skill:

> "Research the current state of AI coding assistants. Compare at least 5 sources including GitHub, papers with code, and industry blogs. Create both an HTML report and a PDF."

Hermes will:

1. Plan 5 search queries
2. Open parallel hidden tabs (10 max)
3. Navigate, extract, save each source
4. Merge findings into `findings.md`
5. Generate `report.html`
6. Save as PDF with `save_pdf`

### B. Price Comparison

Build a price comparison workflow:

1. **Define products** — Create a CSV with product names and URLs
2. **Hidden window** — Use `create_hidden_window` for automation
3. **Parallel extraction** — Open up to 10 tabs
4. **Price regex** — Use `evaluate_script` with regex to extract prices
5. **Merge** — Combine into comparison CSV
6. **Report** — Generate HTML with price columns and links

### C. Web Monitoring

Set up monitoring with cron:

1. Use BrowserOS to navigate to target pages
2. Extract current state with `get_page_content`
3. Compare against previous saved state
4. If changes detected, alert via Hermes
5. Save new state

Example cron job:

```
# Check Hacker News top post every hour
0 * * * * hermes exec "check HN and save top story"
```

### D. Connect Apps Actions

BrowserOS can connect to 40+ services:

1. `discover_server_categories_or_actions` — List available services
2. `get_category_actions` — Get actions for a service (e.g., GitHub)
3. `get_action_details` — Get required parameters
4. `execute_action` — Execute with parameters
5. `handle_auth_failure` — If auth fails, get auth URL

---

## Best Practices

### 1. Always Take a Snapshot First

Before any automation, always:

```
# Get interactive elements
snapshot = take_snapshot()
# Then use the element IDs for clicks, fills, etc.
```

### 2. Save Data Incrementally

Never accumulate data in memory:

```
# GOOD: Save each page immediately
for page in pages:
    data = extract(page)
    save(f"raw/{page.slug}.json")
merge_from_files("raw/")
```

### 3. Limit Concurrent Tabs

Max 10 open tabs at a time:

```
# Process in batches of 10
for batch in chunks(urls, 10):
    tabs = [new_hidden_page(url) for url in batch]
    extract_all(tabs)
    close_all(tabs)
```

### 4. Handle Dynamic Content

For pages with infinite scroll or lazy loading:

```
# Scroll to load more content
await scroll(direction="down")

# Or use JavaScript
evaluate_script(script="window.scrollTo(0, document.body.scrollHeight)")
```

### 5. Use JavaScript for Complex Extraction

For nested structures (product cards, etc.):

```javascript
// extract.js
const items = document.querySelectorAll(".product-card");
return JSON.stringify(
  Array.from(items).map((item) => ({
    name: item.querySelector(".title").innerText,
    price: item.querySelector(".price").innerText,
    url: item.querySelector("a").href,
  })),
);
```

### 6. Clean Up After Automation

Always close hidden windows and tabs:

```
await close_window(window_id=hidden_window_id)
```

### 7. Handle Dialogs Proactively

Before triggering potential dialogs:

```
# First, set the dialog handler
await handle_dialog(accept=True)
# Then click the element that might trigger a dialog
```

### 8. Record Source URLs

Every extracted data point should include its source:

```csv
product,price,source_url
NVIDIA RTX 5090,$999,https://newegg.com/product/...
```

---

## Troubleshooting

### MCP Connection Refused

**Problem:** `Failed to connect to MCP server 'browseros'`

**Fix:**

1. Verify BrowserOS is running: `curl http://127.0.0.1:9201/health`
2. If not, start BrowserOS: `~/Downloads/BrowserOS`
3. Restart Hermes

### Tools Not Appearing

**Problem:** Tools listed but not available

**Fix:**

1. Restart Hermes: `hermes` (new session)
2. Check config: `cat ~/.hermes/config.yaml | grep -A5 mcp_servers`

### Page Load Timeout

**Problem:** `navigate_page` times out

**Fix:**

- Increase timeout in config:

  ```yaml
  mcp_servers:
    browseros:
      url: "http://127.0.0.1:9201/mcp"
      timeout: 180 # increased from 120
  ```

### Screenshot Not Supported on Hidden Tab

**Problem:** `take_screenshot` fails on hidden tab

**Fix:**

- Use `show_page` first to make the tab visible:

  ```
  await show_page(page_id=page_id)
  ```

### Element Not Found

**Problem:** `click` or `fill` fails — element not in snapshot

**Fix:**

1. Wait for page to settle: `evaluate_script` with a small delay
2. Re-take snapshot: `take_snapshot`
3. Use `search_dom` to find element by text/CSS
4. Use `scroll` to bring element into view

---

## Summary

BrowserOS transforms web automation from brittle scripts into reliable AI-driven workflows. Combined with Hermes Agent's memory, skills, and MCP integration, you get:

- **Natural language control** over any web task
- **Persistent state** across sessions
- **66+ tools** for every browser interaction
- **40+ integrations** via Connect Apps
- **Built-in skills** for research, extraction, monitoring

Pair BrowserOS with Hermes for the most powerful local AI browser experience available.

---

## Additional Resources

- **MCP Protocol:** https://modelcontextprotocol.io
- **Hermes MCP:** See `hermes-agent` skill for MCP configuration
- **BrowserOS Skills:** Built-in workflows at `~/.browseros/skills/builtin/`
