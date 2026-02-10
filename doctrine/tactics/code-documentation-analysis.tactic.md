# Tactic: Code and Documentation Analysis for Boundary Discovery

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Invoked By:** [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md)

---

## Purpose

Extract terminology from codebase and documentation to identify semantic clusters that reveal implicit context boundaries.

---

## Prerequisites

- [ ] Access to codebase (source control)
- [ ] Access to documentation (README, specs, ADRs)
- [ ] Command-line tools available (grep/rg, AST parsers)
- [ ] Optional: LLM access for semantic similarity analysis

---

## Procedure

### Step 1: Extract Terminology from Code

**Objective:** Collect domain terms from all code artifacts

**Sources:**
1. **Class/module/function names**
   ```bash
   rg "^class (\w+)" --only-matching | sort | uniq
   ```

2. **Code comments and docstrings**
   ```bash
   rg "^\s*#.*" --type python | grep -v "^#!" | sort | uniq
   ```

3. **Test descriptions**
   ```bash
   rg "def test_\w+" --only-matching | sort | uniq
   ```

4. **Documentation sections**
   ```bash
   find docs/ -name "*.md" -exec grep -h "^##" {} \; | sort | uniq
   ```

**Output:** Raw term list (100-500 terms typical)

**Time Estimate:** 1-2 hours

---

### Step 2: Cluster by Semantic Similarity

**Objective:** Group related terms together

**Analysis:**
1. **Co-occurrence analysis:**
   - Which terms appear in same files?
   - Which are never used together?
   
   ```bash
   # Find files containing "Order"
   rg -l "Order" > order_files.txt
   
   # Find files containing "Customer"
   rg -l "Customer" > customer_files.txt
   
   # Find intersection (co-occurrence)
   comm -12 <(sort order_files.txt) <(sort customer_files.txt)
   ```

2. **Definition conflict detection:**
   - Same term with different meanings?
   - Use grep to find definitions:
   
   ```bash
   rg "class Order" --with-filename
   # Check if multiple definitions exist with different fields
   ```

3. **Semantic similarity (LLM-assisted):**
   - Extract definitions
   - Compare meanings
   - Score similarity (0-1)

**Output:** Term clusters (groups of related concepts)

**Time Estimate:** 2-3 hours

---

### Step 3: Map Clusters to Code Ownership

**Objective:** Identify which teams own which vocabulary domains

**Analysis:**
1. **Git ownership:**
   ```bash
   # Who commits to files with "Order"?
   git log --all --format='%an' -- '*Order*' | sort | uniq -c | sort -rn
   ```

2. **Directory structure:**
   - Which directories contain which clusters?
   - Do directories align with teams?

3. **Cross-boundary detection:**
   - Where do clusters span team boundaries?
   - Potential coupling risk

**Output:** Ownership map (clusters → teams)

**Time Estimate:** 1-2 hours

---

### Step 4: Propose Context Boundaries

**Objective:** Suggest boundaries based on semantic clusters

**Process:**
1. **Align with clusters:**
   - If Cluster A (Customer, Order, Quote) owned by Team Sales
   - And Cluster B (Shipment, Warehouse) owned by Team Fulfillment
   - Propose boundary between clusters

2. **Validate with ownership:**
   - Do proposed boundaries match team structure?
   - Where is there mismatch?

3. **Check for violations:**
   - Same term in multiple clusters with different meanings?
   - Cross-cluster dependencies?

**Output:** Proposed context boundaries with evidence

**Time Estimate:** 1-2 hours

---

## Tools Reference

### Command-Line Tools

**ripgrep (rg):**
```bash
# Find term usage
rg "Customer" --count

# Find class definitions
rg "^class (\w+)" --only-matching

# Find in specific file types
rg "Order" --type python --type java
```

**AST Parsers:**
```python
# Python example using ast module
import ast, glob

terms = set()
for file in glob.glob("src/**/*.py", recursive=True):
    with open(file) as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                terms.add(node.name)
```

**Git Analysis:**
```bash
# Commit authors for pattern
git log --all --format='%an' -- '*pattern*' | sort | uniq -c

# Recent changes
git log --since="6 months ago" --name-only --pretty=format: | grep "Order" | sort | uniq -c
```

---

## Success Criteria

**Analysis is successful when:**
- ✅ 100-500 terms extracted from codebase
- ✅ Terms clustered by semantic similarity
- ✅ Clusters mapped to team ownership
- ✅ Proposed boundaries validated with teams
- ✅ Cross-boundary risks identified

---

## Common Issues and Solutions

**Issue 1: Too many terms (noise)**
**Solution:** Filter generic terms (data, info, manager, handler), focus on domain-specific

**Issue 2: Cluster boundaries unclear**
**Solution:** Use co-occurrence matrix, visualize with network graph

**Issue 3: Ownership ambiguous**
**Solution:** Survey teams directly about term ownership

**Issue 4: LLM similarity scores unreliable**
**Solution:** Use co-occurrence as primary signal, LLM as validation

---

## Related Documentation

**Approaches:**
- [Bounded Context Linguistic Discovery](../approaches/bounded-context-linguistic-discovery.md) - Strategic framework

**Tactics:**
- [Terminology Extraction and Mapping](terminology-extraction-mapping.tactic.md) - Glossary creation
- [Team Interaction Mapping](team-interaction-mapping.tactic.md) - Organizational analysis

---

## Version History

- **1.0.0** (2026-02-10): Initial extraction from bounded-context-linguistic-discovery approach

---

**Curation Status:** ✅ Extracted per feedback (comment 2785994932)
