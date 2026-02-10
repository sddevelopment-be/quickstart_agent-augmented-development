#!/usr/bin/env python3
"""
Glossary Term Parser and Consolidator
Parses candidate terms from batch summaries and YAML files
Creates master term database for curation
"""

import yaml
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

# Paths
WORKSPACE_ROOT = Path("/home/runner/work/quickstart_agent-augmented-development/quickstart_agent-augmented-development")
CANDIDATES_DIR = WORKSPACE_ROOT / "work" / "glossary-candidates"
CURATOR_DIR = WORKSPACE_ROOT / "work" / "curator"
EXISTING_GLOSSARY = WORKSPACE_ROOT / "doctrine" / "GLOSSARY.md"

# Batch files
BATCHES = [
    {
        "name": "Batch 1: Directives",
        "summary": "batch1-directives-extraction-summary.md",
        "yaml": "batch1-directives-candidates.yaml",
        "source_layer": "directives"
    },
    {
        "name": "Batch 2: Approaches",
        "summary": "batch2-approaches-extraction-summary.md",
        "yaml": "batch2-approaches-candidates.yaml",
        "source_layer": "approaches"
    },
    {
        "name": "Batch 3: Tactics",
        "summary": "batch3-tactics-extraction-summary.md",
        "yaml": "batch3-tactics-candidates.yaml",
        "source_layer": "tactics"
    },
    {
        "name": "Batch 4: Agents",
        "summary": "batch4-agents-extraction-summary.md",
        "yaml": "batch4-agents-candidates.yaml",
        "source_layer": "agents"
    }
]


def parse_existing_glossary() -> Dict[str, Any]:
    """Parse existing glossary to identify current terms"""
    existing_terms = {}
    
    with open(EXISTING_GLOSSARY, 'r') as f:
        content = f.read()
    
    # Extract terms using ## heading pattern
    term_pattern = r'^### (.+?)$\n\n((?:(?!^###).)+)'
    matches = re.finditer(term_pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        term_name = match.group(1).strip()
        term_content = match.group(2).strip()
        
        # Extract related terms
        related_pattern = r'\*\*Related:\*\* (.+?)(?:\n|$)'
        related_match = re.search(related_pattern, term_content)
        related_terms = []
        if related_match:
            related_terms = [t.strip() for t in related_match.group(1).split(',')]
        
        # Extract reference
        ref_pattern = r'\*\*Reference:\*\* (.+?)(?:\n|$)'
        ref_match = re.search(ref_pattern, term_content)
        reference = ref_match.group(1).strip() if ref_match else None
        
        existing_terms[term_name.lower()] = {
            "name": term_name,
            "definition": term_content,
            "related_terms": related_terms,
            "reference": reference,
            "source": "existing"
        }
    
    return existing_terms


def parse_yaml_candidates(yaml_file: Path) -> List[Dict[str, Any]]:
    """Parse YAML candidate file"""
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Handle both 'candidates' and 'terms' keys
    if 'candidates' in data:
        return data['candidates']
    elif 'terms' in data:
        return data['terms']
    else:
        return []


def normalize_term_name(name: str) -> str:
    """Normalize term name for comparison"""
    # Remove parenthetical context
    name = re.sub(r'\s*\([^)]+\)\s*', '', name)
    return name.strip().lower()


def parse_summary_markdown(summary_file: Path, batch_name: str) -> List[Dict[str, Any]]:
    """
    Parse term list from summary markdown file
    This is needed because summaries contain the full list,
    while YAML files contain only selected high-confidence terms
    """
    terms = []
    
    with open(summary_file, 'r') as f:
        content = f.read()
    
    # Look for numbered term lists (e.g., "1. **Term Name** - Definition")
    term_pattern = r'^\d+\.\s+\*\*(.+?)\*\*\s*[-–—]\s*(.+?)(?=^\d+\.|\Z)'
    matches = re.finditer(term_pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        term_name = match.group(1).strip()
        definition = match.group(2).strip().replace('\n', ' ')
        
        # Clean up definition
        definition = re.sub(r'\s+', ' ', definition)
        
        terms.append({
            "term": term_name,
            "definition": definition,
            "source": f"{batch_name} (summary)",
            "confidence": "high"  # Assume high for summary terms
        })
    
    return terms


def merge_term_sources(candidates: List[Dict[str, Any]], existing: Dict[str, Any]) -> Dict[str, Any]:
    """Merge candidate terms from multiple sources"""
    merged = {}
    duplicates = []
    
    for candidate in candidates:
        term_key = normalize_term_name(candidate.get('term', ''))
        
        if not term_key:
            continue
        
        # Check if exists in current glossary
        if term_key in existing:
            duplicates.append({
                "term": candidate.get('term'),
                "existing": existing[term_key]['name'],
                "source": candidate.get('source')
            })
            # Enhance existing term with additional context
            if term_key not in merged:
                merged[term_key] = existing[term_key].copy()
                merged[term_key]['sources'] = [existing[term_key]['source']]
                merged[term_key]['definitions'] = [existing[term_key]['definition']]
            
            # Add candidate as alternative definition
            merged[term_key]['sources'].append(candidate.get('source'))
            merged[term_key]['definitions'].append(candidate.get('definition'))
        else:
            # New term
            if term_key not in merged:
                merged[term_key] = {
                    "name": candidate.get('term'),
                    "definition": candidate.get('definition'),
                    "context": candidate.get('context', ''),
                    "source": candidate.get('source'),
                    "related_terms": candidate.get('related_terms', []),
                    "confidence": candidate.get('confidence', 'high'),
                    "enforcement_tier": candidate.get('enforcement_tier', 'advisory'),
                    "sources": [candidate.get('source')],
                    "definitions": [candidate.get('definition')]
                }
            else:
                # Duplicate within candidates
                merged[term_key]['sources'].append(candidate.get('source'))
                merged[term_key]['definitions'].append(candidate.get('definition'))
    
    return merged, duplicates


def main():
    print("=" * 80)
    print("Glossary Candidate Parser")
    print("=" * 80)
    
    # Parse existing glossary
    print("\n📚 Parsing existing glossary...")
    existing_terms = parse_existing_glossary()
    print(f"   Found {len(existing_terms)} existing terms")
    
    # Parse all batches
    all_candidates = []
    batch_stats = []
    
    for batch in BATCHES:
        print(f"\n📦 Processing {batch['name']}...")
        
        yaml_file = CANDIDATES_DIR / batch['yaml']
        summary_file = CANDIDATES_DIR / batch['summary']
        
        # Parse YAML candidates (high-confidence structured data)
        yaml_terms = []
        if yaml_file.exists():
            yaml_terms = parse_yaml_candidates(yaml_file)
            print(f"   YAML: {len(yaml_terms)} terms")
        
        # Parse summary markdown (complete term list)
        summary_terms = []
        if summary_file.exists():
            summary_terms = parse_summary_markdown(summary_file, batch['name'])
            print(f"   Summary: {len(summary_terms)} terms")
        
        # Combine (YAML has more structure, summary has more coverage)
        # Create lookup by normalized name
        yaml_lookup = {normalize_term_name(t.get('term', '')): t for t in yaml_terms}
        
        for term in summary_terms:
            norm_name = normalize_term_name(term['term'])
            if norm_name in yaml_lookup:
                # Merge: YAML structure + summary definition if missing
                merged_term = yaml_lookup[norm_name].copy()
                if not merged_term.get('definition'):
                    merged_term['definition'] = term['definition']
                all_candidates.append(merged_term)
            else:
                # Summary-only term
                all_candidates.append({
                    **term,
                    'context': batch['source_layer'],
                    'status': 'candidate',
                    'enforcement_tier': 'advisory'
                })
        
        batch_stats.append({
            "name": batch['name'],
            "yaml_count": len(yaml_terms),
            "summary_count": len(summary_terms),
            "total": max(len(yaml_terms), len(summary_terms))
        })
    
    print(f"\n📊 Total candidates collected: {len(all_candidates)}")
    
    # Merge and deduplicate
    print("\n🔄 Merging and deduplicating...")
    merged_terms, duplicates = merge_term_sources(all_candidates, existing_terms)
    
    print(f"   Unique terms after merge: {len(merged_terms)}")
    print(f"   Duplicates with existing: {len([d for d in duplicates if 'existing' in d])}")
    print(f"   Cross-batch duplicates: {len([k for k, v in merged_terms.items() if len(v.get('sources', [])) > 1])}")
    
    # Save results
    output_file = CURATOR_DIR / "parsed-terms.json"
    with open(output_file, 'w') as f:
        json.dump({
            "existing_count": len(existing_terms),
            "candidate_count": len(all_candidates),
            "merged_count": len(merged_terms),
            "duplicate_count": len(duplicates),
            "batch_stats": batch_stats,
            "duplicates": duplicates,
            "merged_terms": {k: v for k, v in merged_terms.items()}
        }, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    
    # Summary report
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Existing glossary terms:      {len(existing_terms)}")
    print(f"Candidate terms collected:    {len(all_candidates)}")
    print(f"Unique terms after merge:     {len(merged_terms)}")
    print(f"Terms overlapping existing:   {len([d for d in duplicates if 'existing' in d])}")
    print(f"Cross-batch duplicates:       {len([k for k, v in merged_terms.items() if len(v.get('sources', [])) > 1])}")
    print(f"\nProjected final glossary:     ~{len(existing_terms) + len(merged_terms) - len([d for d in duplicates if 'existing' in d])} terms")
    print("=" * 80)


if __name__ == "__main__":
    main()
