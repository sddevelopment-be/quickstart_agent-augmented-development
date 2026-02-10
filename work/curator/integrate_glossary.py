#!/usr/bin/env python3
"""
Glossary Integration Script
Integrates 360 candidate terms from batches 1-4 into existing glossary
Handles deduplication, merging, and alphabetical ordering
"""

import yaml
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Paths
WORKSPACE_ROOT = Path("/home/runner/work/quickstart_agent-augmented-development/quickstart_agent-augmented-development")
CANDIDATES_DIR = WORKSPACE_ROOT / "work" / "glossary-candidates"
CURATOR_DIR = WORKSPACE_ROOT / "work" / "curator"
EXISTING_GLOSSARY = WORKSPACE_ROOT / "doctrine" / "GLOSSARY.md"

# Batch YAML files
BATCH_FILES = [
    "batch1-directives-candidates.yaml",
    "batch2-approaches-candidates.yaml",
    "batch3-tactics-candidates.yaml",
    "batch4-agents-candidates.yaml"
]


def normalize_term_name(name: str) -> str:
    """Normalize term name for comparison (lowercase, no extra spaces)"""
    # Remove parenthetical context for comparison
    name = re.sub(r'\s*\([^)]+\)\s*', '', name)
    # Normalize whitespace
    name = re.sub(r'\s+', ' ', name)
    return name.strip().lower()


def parse_existing_glossary() -> Tuple[Dict[str, Dict], str, str]:
    """
    Parse existing glossary and return terms dict, header, footer
    Returns: (terms_dict, glossary_header, glossary_footer)
    """
    with open(EXISTING_GLOSSARY, 'r') as f:
        content = f.read()
    
    # Split into header (before ## Terms), terms section, footer (after last term)
    terms_marker = "## Terms"
    
    if terms_marker not in content:
        raise ValueError("Could not find '## Terms' section in glossary")
    
    header_end = content.find(terms_marker) + len(terms_marker)
    header = content[:header_end]
    
    terms_and_footer = content[header_end:]
    
    # Extract individual term entries
    # Terms start with ### and go until next ### or end
    term_pattern = r'(^### .+?)(?=\n### |\n---|\Z)'
    matches = list(re.finditer(term_pattern, terms_and_footer, re.MULTILINE | re.DOTALL))
    
    existing_terms = {}
    
    for match in matches:
        term_block = match.group(1).strip()
        
        # Extract term name from ### heading
        first_line = term_block.split('\n')[0]
        term_name = first_line.replace('###', '').strip()
        
        # Store full term block
        existing_terms[normalize_term_name(term_name)] = {
            "original_name": term_name,
            "full_block": term_block,
            "normalized": normalize_term_name(term_name)
        }
    
    # Find footer (everything after last term, starting with ---)
    footer_match = re.search(r'\n---\n.*', terms_and_footer, re.DOTALL)
    footer = footer_match.group(0) if footer_match else "\n\n---\n"
    
    return existing_terms, header, footer


def load_candidate_terms() -> List[Dict]:
    """Load all candidate terms from batch YAML files"""
    all_candidates = []
    
    for batch_file in BATCH_FILES:
        filepath = CANDIDATES_DIR / batch_file
        
        if not filepath.exists():
            print(f"⚠️  Warning: {batch_file} not found")
            continue
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        # Handle both 'candidates' and 'terms' keys
        candidates = data.get('candidates', data.get('terms', []))
        
        # Add batch source
        for candidate in candidates:
            candidate['batch_source'] = batch_file
            all_candidates.append(candidate)
    
    return all_candidates


def format_term_entry(term_data: Dict) -> str:
    """Format a term as a glossary entry"""
    term_name = term_data['term']
    definition = term_data.get('definition', 'No definition provided.')
    context = term_data.get('context', '')
    source = term_data.get('source', '')
    related_terms = term_data.get('related_terms', [])
    reference = term_data.get('reference', '')
    
    # Build term entry
    lines = [f"### {term_name}", ""]
    
    # Add definition (handle multi-line)
    if isinstance(definition, list):
        definition = ' '.join(str(d) for d in definition)
    
    # Clean definition
    definition = re.sub(r'\s+', ' ', str(definition)).strip()
    lines.append(definition)
    lines.append("")
    
    # Add context if meaningful
    if context and context not in ['Framework', 'General']:
        lines.append(f"**Context:** {context}  ")
    
    # Add reference/source
    if reference:
        lines.append(f"**Reference:** {reference}  ")
    elif source:
        lines.append(f"**Source:** {source}  ")
    
    # Add related terms
    if related_terms:
        related_str = ", ".join(related_terms)
        lines.append(f"**Related:** {related_str}")
    
    lines.append("")
    
    return "\n".join(lines)


def merge_terms(existing: Dict[str, Dict], candidates: List[Dict]) -> Tuple[Dict, List, List, List]:
    """
    Merge candidate terms with existing
    Returns: (final_terms, new_terms, updated_terms, duplicates)
    """
    final_terms = {}
    new_terms = []
    updated_terms = []
    duplicates = []
    cross_batch_dups = defaultdict(list)
    
    # First pass: collect all candidates by normalized name
    candidates_by_name = defaultdict(list)
    for candidate in candidates:
        norm_name = normalize_term_name(candidate['term'])
        candidates_by_name[norm_name].append(candidate)
    
    # Identify cross-batch duplicates
    for norm_name, cand_list in candidates_by_name.items():
        if len(cand_list) > 1:
            cross_batch_dups[norm_name] = cand_list
    
    # Second pass: merge
    for norm_name, cand_list in candidates_by_name.items():
        # Use first candidate as base (could enhance with merging logic)
        primary_candidate = cand_list[0]
        
        if norm_name in existing:
            # Term exists - preserve existing, note as duplicate
            final_terms[norm_name] = existing[norm_name]
            duplicates.append({
                "term": primary_candidate['term'],
                "existing_name": existing[norm_name]['original_name'],
                "sources": [c.get('batch_source') for c in cand_list]
            })
        else:
            # New term
            final_terms[norm_name] = {
                "original_name": primary_candidate['term'],
                "data": primary_candidate,
                "normalized": norm_name,
                "sources": [c.get('batch_source') for c in cand_list]
            }
            new_terms.append(primary_candidate['term'])
    
    return final_terms, new_terms, updated_terms, list(cross_batch_dups.items())


def generate_new_glossary(existing_terms: Dict, all_terms: Dict, header: str, footer: str) -> str:
    """Generate complete new glossary with all terms alphabetically sorted"""
    
    # Combine existing terms (formatted blocks) and new terms (need formatting)
    all_entries = []
    
    for norm_name, term_info in all_terms.items():
        if 'full_block' in term_info:
            # Existing term - use as-is
            all_entries.append({
                "name": term_info['original_name'],
                "normalized": norm_name,
                "content": term_info['full_block']
            })
        else:
            # New term - format it
            all_entries.append({
                "name": term_info['original_name'],
                "normalized": norm_name,
                "content": format_term_entry(term_info['data'])
            })
    
    # Sort alphabetically by normalized name
    all_entries.sort(key=lambda x: x['normalized'])
    
    # Build glossary
    glossary_content = header + "\n\n"
    
    for entry in all_entries:
        glossary_content += entry['content'] + "\n"
    
    glossary_content += footer
    
    return glossary_content


def main():
    print("=" * 80)
    print("Glossary Integration: Batches 1-4")
    print("=" * 80)
    
    # Step 1: Parse existing glossary
    print("\n📚 Step 1: Parsing existing glossary...")
    existing_terms, header, footer = parse_existing_glossary()
    print(f"   Found {len(existing_terms)} existing terms")
    
    # Step 2: Load candidates
    print("\n📦 Step 2: Loading candidate terms...")
    candidates = load_candidate_terms()
    print(f"   Loaded {len(candidates)} candidate terms from {len(BATCH_FILES)} batches")
    
    # Step 3: Merge and deduplicate
    print("\n🔄 Step 3: Merging and deduplicating...")
    final_terms, new_terms, updated_terms, cross_batch_dups = merge_terms(existing_terms, candidates)
    
    print(f"   Existing terms preserved: {len([t for t in final_terms.values() if 'full_block' in t])}")
    print(f"   New terms to add: {len(new_terms)}")
    print(f"   Duplicates with existing: {len([t for t in final_terms.values() if 'full_block' in t and t['normalized'] in [normalize_term_name(c['term']) for c in candidates]])}")
    print(f"   Cross-batch duplicates: {len(cross_batch_dups)}")
    
    # Step 4: Generate new glossary
    print("\n📝 Step 4: Generating new glossary...")
    new_glossary_content = generate_new_glossary(existing_terms, final_terms, header, footer)
    
    # Calculate stats
    term_count = len(final_terms)
    line_count = new_glossary_content.count('\n')
    
    print(f"   Final term count: {term_count}")
    print(f"   Final line count: {line_count}")
    
    # Step 5: Save outputs
    print("\n💾 Step 5: Saving outputs...")
    
    # Save new glossary
    output_glossary = CURATOR_DIR / "GLOSSARY-integrated.md"
    with open(output_glossary, 'w') as f:
        f.write(new_glossary_content)
    print(f"   New glossary: {output_glossary}")
    
    # Save integration report
    report_lines = [
        "# Glossary Integration Report",
        "",
        f"**Date:** 2026-02-10",
        f"**Agent:** Curator Claire",
        "",
        "## Summary",
        "",
        f"- **Existing terms:** {len(existing_terms)}",
        f"- **Candidate terms:** {len(candidates)}",
        f"- **New terms added:** {len(new_terms)}",
        f"- **Duplicates with existing:** {len([t for n, t in final_terms.items() if 'full_block' in t and n in [normalize_term_name(c['term']) for c in candidates]])}",
        f"- **Cross-batch duplicates:** {len(cross_batch_dups)}",
        f"- **Final term count:** {term_count}",
        "",
        "## New Terms Added",
        ""
    ]
    
    for term_name in sorted(new_terms):
        report_lines.append(f"- {term_name}")
    
    if cross_batch_dups:
        report_lines.extend([
            "",
            "## Cross-Batch Duplicates (Merged)",
            ""
        ])
        for norm_name, cand_list in cross_batch_dups:
            report_lines.append(f"- **{cand_list[0]['term']}** appeared in {len(cand_list)} batches:")
            for cand in cand_list:
                report_lines.append(f"  - {cand.get('batch_source', 'unknown')}")
    
    report_path = CURATOR_DIR / "integration-report.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    print(f"   Integration report: {report_path}")
    
    # Step 6: Summary
    print("\n" + "=" * 80)
    print("INTEGRATION COMPLETE")
    print("=" * 80)
    print(f"Existing terms:        {len(existing_terms)}")
    print(f"Candidates processed:  {len(candidates)}")
    print(f"New terms added:       {len(new_terms)}")
    print(f"Final glossary size:   {term_count} terms, {line_count} lines")
    print(f"\nOutput: {output_glossary}")
    print(f"Report: {report_path}")
    print("=" * 80)
    
    print("\n✅ Integration complete. Review the outputs before committing.")


if __name__ == "__main__":
    main()
