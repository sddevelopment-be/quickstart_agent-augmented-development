#!/usr/bin/env python3
"""
Distribution Config Editor - Web-based configuration tool for release packaging.

This script provides a simple web interface to select which directories and files
should be included in the framework release package. It displays the repository
structure as a collapsible tree with checkboxes, and updates distribution-config.yaml
when submitted.

Usage:
    python ops/release/config_editor.py [--port PORT]

Then open http://localhost:8765 in your browser.

Reference:
    - ops/release/distribution-config.yaml
    - ADR-013: Zip-Based Framework Distribution
"""

import argparse
import http.server
import json
import os
import socketserver
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Dict, List, Any

import yaml

# Repository root (relative to script location)
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CONFIG_FILE = SCRIPT_DIR / "distribution-config.yaml"

# Directories to always exclude from the tree view
EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
    "output",
    "dist",
    "build",
    ".mypy_cache",
    ".ruff_cache",
    ".coverage",
    "htmlcov",
    "*.egg-info",
}

# File patterns to exclude
EXCLUDED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".gitignore",
}


def should_exclude(name: str) -> bool:
    """Check if a file or directory should be excluded from the tree."""
    if name in EXCLUDED_DIRS or name in EXCLUDED_FILES:
        return True
    for pattern in EXCLUDED_DIRS | EXCLUDED_FILES:
        if pattern.startswith("*") and name.endswith(pattern[1:]):
            return True
    return False


def scan_directory(path: Path, relative_to: Path, max_depth: int = 4, current_depth: int = 0) -> Dict[str, Any]:
    """
    Recursively scan a directory and return its structure.

    Returns a dict with:
        - name: directory/file name
        - path: relative path from repo root
        - type: 'dir' or 'file'
        - children: list of child nodes (for directories)
    """
    name = path.name or str(path)
    rel_path = str(path.relative_to(relative_to))

    if path.is_file():
        return {
            "name": name,
            "path": rel_path,
            "type": "file",
        }

    # Directory
    result = {
        "name": name,
        "path": rel_path,
        "type": "dir",
        "children": [],
    }

    if current_depth >= max_depth:
        result["truncated"] = True
        return result

    try:
        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for entry in entries:
            if should_exclude(entry.name):
                continue
            child = scan_directory(entry, relative_to, max_depth, current_depth + 1)
            result["children"].append(child)
    except PermissionError:
        result["error"] = "Permission denied"

    return result


def load_current_config() -> Dict[str, Any]:
    """Load the current distribution configuration."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f)
    return {}


def get_currently_selected_paths(config: Dict[str, Any]) -> set:
    """Extract all selected paths from the current configuration."""
    selected = set()

    for item in config.get("core_directories", []):
        if isinstance(item, dict):
            selected.add(item.get("path", ""))
        else:
            selected.add(item)

    for item in config.get("export_directories", []):
        if isinstance(item, dict):
            selected.add(item.get("path", ""))
        else:
            selected.add(item)

    for item in config.get("root_files", []):
        if isinstance(item, dict):
            selected.add(item.get("path", ""))
        else:
            selected.add(item)

    return selected


def generate_html(tree: Dict[str, Any], selected_paths: set, config: Dict[str, Any]) -> str:
    """Generate the HTML page with the directory tree."""

    tree_json = json.dumps(tree, indent=2)
    selected_json = json.dumps(list(selected_paths))
    config_json = json.dumps(config, indent=2)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Distribution Config Editor</title>
    <style>
        :root {{
            --bg-color: #1a1a2e;
            --surface-color: #16213e;
            --primary-color: #0f3460;
            --accent-color: #e94560;
            --text-color: #eaeaea;
            --text-muted: #a0a0a0;
            --success-color: #4ade80;
            --border-color: #2a2a4a;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }}

        h1 {{
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .subtitle {{
            color: var(--text-muted);
            font-size: 0.95rem;
        }}

        .main-content {{
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 30px;
        }}

        @media (max-width: 900px) {{
            .main-content {{
                grid-template-columns: 1fr;
            }}
        }}

        .panel {{
            background: var(--surface-color);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-color);
        }}

        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-color);
        }}

        .panel-title {{
            font-size: 1.1rem;
            font-weight: 600;
        }}

        .tree-container {{
            max-height: 70vh;
            overflow-y: auto;
            padding-right: 10px;
        }}

        .tree-container::-webkit-scrollbar {{
            width: 8px;
        }}

        .tree-container::-webkit-scrollbar-track {{
            background: var(--bg-color);
            border-radius: 4px;
        }}

        .tree-container::-webkit-scrollbar-thumb {{
            background: var(--primary-color);
            border-radius: 4px;
        }}

        .tree-node {{
            user-select: none;
        }}

        .tree-item {{
            display: flex;
            align-items: center;
            padding: 6px 8px;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.15s;
        }}

        .tree-item:hover {{
            background: var(--primary-color);
        }}

        .tree-toggle {{
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 4px;
            color: var(--text-muted);
            font-size: 12px;
            transition: transform 0.2s;
        }}

        .tree-toggle.expanded {{
            transform: rotate(90deg);
        }}

        .tree-toggle.empty {{
            visibility: hidden;
        }}

        .tree-checkbox {{
            width: 18px;
            height: 18px;
            margin-right: 8px;
            accent-color: var(--accent-color);
            cursor: pointer;
        }}

        .tree-icon {{
            margin-right: 8px;
            font-size: 16px;
        }}

        .tree-name {{
            flex: 1;
            font-size: 0.9rem;
        }}

        .tree-name.file {{
            color: var(--text-muted);
        }}

        .tree-children {{
            margin-left: 24px;
            display: none;
        }}

        .tree-children.expanded {{
            display: block;
        }}

        .selection-summary {{
            margin-bottom: 20px;
        }}

        .summary-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.9rem;
        }}

        .summary-item:last-child {{
            border-bottom: none;
        }}

        .summary-label {{
            color: var(--text-muted);
        }}

        .summary-value {{
            font-weight: 600;
        }}

        .selected-list {{
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 20px;
        }}

        .selected-item {{
            display: flex;
            align-items: center;
            padding: 6px 10px;
            background: var(--bg-color);
            border-radius: 6px;
            margin-bottom: 6px;
            font-size: 0.85rem;
            font-family: 'SF Mono', Monaco, Consolas, monospace;
        }}

        .selected-item .icon {{
            margin-right: 8px;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            width: 100%;
        }}

        .btn-primary {{
            background: var(--accent-color);
            color: white;
        }}

        .btn-primary:hover {{
            background: #d13a54;
            transform: translateY(-1px);
        }}

        .btn-primary:disabled {{
            background: var(--border-color);
            cursor: not-allowed;
            transform: none;
        }}

        .btn-secondary {{
            background: var(--primary-color);
            color: var(--text-color);
            margin-top: 10px;
        }}

        .btn-secondary:hover {{
            background: #1a4a7a;
        }}

        .status-message {{
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 0.9rem;
            display: none;
        }}

        .status-message.success {{
            background: rgba(74, 222, 128, 0.15);
            color: var(--success-color);
            display: block;
        }}

        .status-message.error {{
            background: rgba(233, 69, 96, 0.15);
            color: var(--accent-color);
            display: block;
        }}

        .toolbar {{
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }}

        .toolbar-btn {{
            padding: 6px 12px;
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-muted);
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.15s;
        }}

        .toolbar-btn:hover {{
            background: var(--primary-color);
            color: var(--text-color);
        }}

        .category-header {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin: 15px 0 8px 0;
            padding-bottom: 5px;
            border-bottom: 1px solid var(--border-color);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Distribution Config Editor</h1>
            <p class="subtitle">Select directories and files to include in the framework release package</p>
        </header>

        <div class="main-content">
            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">Repository Structure</span>
                    <div class="toolbar">
                        <button class="toolbar-btn" onclick="expandAll()">Expand All</button>
                        <button class="toolbar-btn" onclick="collapseAll()">Collapse All</button>
                        <button class="toolbar-btn" onclick="selectNone()">Clear Selection</button>
                    </div>
                </div>
                <div class="tree-container" id="tree-container">
                    <!-- Tree will be rendered here -->
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <span class="panel-title">Selection Summary</span>
                </div>

                <div class="selection-summary">
                    <div class="summary-item">
                        <span class="summary-label">Directories</span>
                        <span class="summary-value" id="dir-count">0</span>
                    </div>
                    <div class="summary-item">
                        <span class="summary-label">Files</span>
                        <span class="summary-value" id="file-count">0</span>
                    </div>
                </div>

                <div class="category-header">Selected Paths</div>
                <div class="selected-list" id="selected-list">
                    <!-- Selected items will be listed here -->
                </div>

                <button class="btn btn-primary" id="save-btn" onclick="saveConfig()">
                    Save Configuration
                </button>
                <button class="btn btn-secondary" onclick="resetToOriginal()">
                    Reset to Current Config
                </button>

                <div class="status-message" id="status-message"></div>
            </div>
        </div>
    </div>

    <script>
        // Data from server
        const treeData = {tree_json};
        const initialSelected = new Set({selected_json});
        const currentConfig = {config_json};

        // State
        let selectedPaths = new Set(initialSelected);

        // Render the tree
        function renderTree(node, container, level = 0) {{
            const div = document.createElement('div');
            div.className = 'tree-node';
            div.dataset.path = node.path;
            div.dataset.type = node.type;

            const item = document.createElement('div');
            item.className = 'tree-item';

            // Toggle arrow for directories
            const toggle = document.createElement('span');
            toggle.className = 'tree-toggle';
            if (node.type === 'dir' && node.children && node.children.length > 0) {{
                toggle.textContent = '▶';
                toggle.onclick = (e) => {{
                    e.stopPropagation();
                    toggleNode(div);
                }};
            }} else {{
                toggle.className += ' empty';
            }}
            item.appendChild(toggle);

            // Checkbox
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'tree-checkbox';
            checkbox.checked = selectedPaths.has(node.path);
            checkbox.onclick = (e) => {{
                e.stopPropagation();
                toggleSelection(node.path, checkbox.checked, div);
            }};
            item.appendChild(checkbox);

            // Icon
            const icon = document.createElement('span');
            icon.className = 'tree-icon';
            icon.textContent = node.type === 'dir' ? '📁' : '📄';
            item.appendChild(icon);

            // Name
            const name = document.createElement('span');
            name.className = 'tree-name' + (node.type === 'file' ? ' file' : '');
            name.textContent = node.name;
            item.appendChild(name);

            div.appendChild(item);

            // Children container for directories
            if (node.type === 'dir' && node.children && node.children.length > 0) {{
                const children = document.createElement('div');
                children.className = 'tree-children';
                for (const child of node.children) {{
                    renderTree(child, children, level + 1);
                }}
                div.appendChild(children);

                // Expand first two levels by default
                if (level < 2) {{
                    children.classList.add('expanded');
                    toggle.classList.add('expanded');
                }}
            }}

            container.appendChild(div);
        }}

        function toggleNode(nodeDiv) {{
            const children = nodeDiv.querySelector('.tree-children');
            const toggle = nodeDiv.querySelector('.tree-toggle');
            if (children) {{
                children.classList.toggle('expanded');
                toggle.classList.toggle('expanded');
            }}
        }}

        function toggleSelection(path, checked, nodeDiv) {{
            if (checked) {{
                selectedPaths.add(path);
            }} else {{
                selectedPaths.delete(path);
            }}

            // If directory, also toggle all children
            if (nodeDiv.dataset.type === 'dir') {{
                const childCheckboxes = nodeDiv.querySelectorAll('.tree-children .tree-checkbox');
                childCheckboxes.forEach(cb => {{
                    const childNode = cb.closest('.tree-node');
                    if (checked) {{
                        selectedPaths.add(childNode.dataset.path);
                    }} else {{
                        selectedPaths.delete(childNode.dataset.path);
                    }}
                    cb.checked = checked;
                }});
            }}

            updateSummary();
        }}

        function updateSummary() {{
            let dirCount = 0;
            let fileCount = 0;

            const listContainer = document.getElementById('selected-list');
            listContainer.innerHTML = '';

            const sortedPaths = Array.from(selectedPaths).sort();

            for (const path of sortedPaths) {{
                const node = document.querySelector(`.tree-node[data-path="${{CSS.escape(path)}}"]`);
                if (node) {{
                    const isDir = node.dataset.type === 'dir';
                    if (isDir) {{
                        dirCount++;
                    }} else {{
                        fileCount++;
                    }}

                    const item = document.createElement('div');
                    item.className = 'selected-item';
                    item.innerHTML = `<span class="icon">${{isDir ? '📁' : '📄'}}</span>${{path}}`;
                    listContainer.appendChild(item);
                }}
            }}

            document.getElementById('dir-count').textContent = dirCount;
            document.getElementById('file-count').textContent = fileCount;
        }}

        function expandAll() {{
            document.querySelectorAll('.tree-children').forEach(el => el.classList.add('expanded'));
            document.querySelectorAll('.tree-toggle').forEach(el => {{
                if (!el.classList.contains('empty')) el.classList.add('expanded');
            }});
        }}

        function collapseAll() {{
            document.querySelectorAll('.tree-children').forEach(el => el.classList.remove('expanded'));
            document.querySelectorAll('.tree-toggle').forEach(el => el.classList.remove('expanded'));
        }}

        function selectNone() {{
            selectedPaths.clear();
            document.querySelectorAll('.tree-checkbox').forEach(cb => cb.checked = false);
            updateSummary();
        }}

        function resetToOriginal() {{
            selectedPaths = new Set(initialSelected);
            document.querySelectorAll('.tree-node').forEach(node => {{
                const cb = node.querySelector(':scope > .tree-item > .tree-checkbox');
                if (cb) {{
                    cb.checked = selectedPaths.has(node.dataset.path);
                }}
            }});
            updateSummary();
            showStatus('Reset to current configuration', 'success');
        }}

        async function saveConfig() {{
            const btn = document.getElementById('save-btn');
            btn.disabled = true;
            btn.textContent = 'Saving...';

            try {{
                const response = await fetch('/save', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        selected: Array.from(selectedPaths)
                    }})
                }});

                const result = await response.json();

                if (result.success) {{
                    showStatus('Configuration saved successfully!', 'success');
                }} else {{
                    showStatus('Error: ' + result.error, 'error');
                }}
            }} catch (err) {{
                showStatus('Error saving configuration: ' + err.message, 'error');
            }} finally {{
                btn.disabled = false;
                btn.textContent = 'Save Configuration';
            }}
        }}

        function showStatus(message, type) {{
            const el = document.getElementById('status-message');
            el.textContent = message;
            el.className = 'status-message ' + type;

            setTimeout(() => {{
                el.className = 'status-message';
            }}, 5000);
        }}

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            const container = document.getElementById('tree-container');
            for (const child of treeData.children || []) {{
                renderTree(child, container);
            }}
            updateSummary();
        }});
    </script>
</body>
</html>
'''


class ConfigEditorHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the config editor."""

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            # Scan repository and generate page
            tree = scan_directory(REPO_ROOT, REPO_ROOT)
            config = load_current_config()
            selected = get_currently_selected_paths(config)

            html = generate_html(tree, selected, config)
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/save":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode("utf-8"))
                selected_paths = set(data.get("selected", []))

                # Update configuration
                update_config(selected_paths)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")


def update_config(selected_paths: set):
    """Update the distribution-config.yaml with selected paths."""

    # Load existing config to preserve structure
    config = load_current_config()

    # Categorize selected paths
    core_directories = []
    export_directories = []
    root_files = []

    for path in sorted(selected_paths):
        full_path = REPO_ROOT / path

        # Skip if it's a child of an already-selected directory
        # (we only want top-level selections)
        parent_selected = False
        for other in selected_paths:
            if other != path and path.startswith(other + "/"):
                parent_selected = True
                break

        if parent_selected:
            continue

        # Categorize
        if full_path.is_file():
            # Root-level files
            if "/" not in path:
                root_files.append({
                    "path": path,
                    "description": f"Root file: {path}",
                    "required": False,
                })
        else:
            # Directories
            if path.startswith(".claude") or path.startswith(".opencode"):
                export_directories.append({
                    "path": path,
                    "description": f"Export directory: {path}",
                    "required": False,
                })
            else:
                core_directories.append({
                    "path": path,
                    "description": f"Core directory: {path}",
                    "required": False,
                })

    # Update config while preserving other sections
    config["core_directories"] = core_directories
    config["export_directories"] = export_directories
    config["root_files"] = root_files

    # Update metadata
    from datetime import datetime, timezone
    config["metadata"] = config.get("metadata", {})
    config["metadata"]["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    config["metadata"]["config_version"] = config.get("version", "1.0.0")

    # Write back
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  Updated {CONFIG_FILE}")
    print(f"  - Core directories: {len(core_directories)}")
    print(f"  - Export directories: {len(export_directories)}")
    print(f"  - Root files: {len(root_files)}")


def main():
    parser = argparse.ArgumentParser(
        description="Web-based editor for distribution-config.yaml"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8765,
        help="Port to run the server on (default: 8765)"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't automatically open browser"
    )

    args = parser.parse_args()

    # Start server
    with socketserver.TCPServer(("", args.port), ConfigEditorHandler) as httpd:
        url = f"http://localhost:{args.port}"
        print(f"\n{'='*60}")
        print("Distribution Config Editor")
        print(f"{'='*60}")
        print(f"\n  Server running at: {url}")
        print(f"  Config file: {CONFIG_FILE}")
        print(f"\n  Press Ctrl+C to stop the server")
        print(f"{'='*60}\n")

        # Open browser
        if not args.no_browser:
            webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")


if __name__ == "__main__":
    main()
