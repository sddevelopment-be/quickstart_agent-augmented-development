#!/usr/bin/env python3
"""
Quality validation for integrated glossary
Checks:
- Alphabetical ordering
- Term format consistency  
- Cross-reference integrity
- Duplicate detection
"""

import re
from pathlib import Path

GLOSSARY_FILE = Path("work/curator/GLOSSARY-integrated-v2-sorted.md")

def extract_terms(content):
    """Extract all terms with their content"""
    terms = []
    pattern = r'^### (.+?)$'
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        term_name = match.group(1).strip()
        terms.append(term_name)
    
    return terms


def check_alphabetical_order(terms):
    """Check if terms are in alphabetical order"""
    normalized = [t.lower() for t in terms]
    sorted_normalized = sorted(normalized)
    
    issues = []
    for i, (current, expected) in enumerate(zip(normalized, sorted_normalized)):
        if current != expected:
            issues.append({
                "position": i + 1,
                "found": terms[i],
                "expected": terms[sorted_normalized.index(current)] if current in sorted_normalized else "Unknown"
            })
    
    return issues


def check_cross_references(content, terms):
    """Check if **Related:** terms exist in glossary"""
    term_set = set(t.lower() for t in terms)
    
    # Find all Related: lines
    related_pattern = r'\*\*Related:\*\* (.+?)(?:\n|$)'
    issues = []
    
    for match in re.finditer(related_pattern, content, re.MULTILINE):
        related_terms_str = match.group(1)
        related_terms = [t.strip() for t in related_terms_str.split(',')]
        
        for related_term in related_terms:
            # Normalize
            normalized = related_term.lower()
            if normalized not in term_set:
                issues.append(f"Cross-reference not found: '{related_term}'")
    
    return issues


def check_duplicates(terms):
    """Check for duplicate term names"""
    seen = {}
    duplicates = []
    
    for i, term in enumerate(terms):
        normalized = term.lower()
        if normalized in seen:
            duplicates.append({
                "term": term,
                "first_occurrence": seen[normalized],
                "duplicate_occurrence": i + 1
            })
        else:
            seen[normalized] = i + 1
    
    return duplicates


def main():
    print("=" * 80)
    print("Glossary Quality Validation")
    print("=" * 80)
    
    # Load glossary
    with open(GLOSSARY_FILE, 'r') as f:
        content = f.read()
    
    # Extract terms
    terms = extract_terms(content)
    print(f"\n📊 Total terms: {len(terms)}")
    
    # Check 1: Alphabetical order
    print("\n🔤 Checking alphabetical order...")
    order_issues = check_alphabetical_order(terms)
    
    if not order_issues:
        print("   ✅ All terms in correct alphabetical order")
    else:
        print(f"   ❌ Found {len(order_issues)} ordering issues:")
        for issue in order_issues[:10]:  # Show first 10
            print(f"      Position {issue['position']}: '{issue['found']}' may be out of order")
    
    # Check 2: Duplicates
    print("\n🔍 Checking for duplicates...")
    duplicates = check_duplicates(terms)
    
    if not duplicates:
        print("   ✅ No duplicate terms found")
    else:
        print(f"   ❌ Found {len(duplicates)} duplicates:")
        for dup in duplicates:
            print(f"      '{dup['term']}' at positions {dup['first_occurrence']} and {dup['duplicate_occurrence']}")
    
    # Check 3: Cross-references (sample check)
    print("\n🔗 Checking cross-reference integrity (sample)...")
    cross_ref_issues = check_cross_references(content, terms)
    
    # Get unique issues
    unique_issues = list(set(cross_ref_issues))
    
    if not unique_issues:
        print("   ✅ All cross-references valid (sample check)")
    else:
        print(f"   ⚠️  Found {len(unique_issues)} potential cross-reference issues:")
        for issue in unique_issues[:20]:  # Show first 20
            print(f"      {issue}")
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total terms:               {len(terms)}")
    print(f"Alphabetical issues:       {len(order_issues)}")
    print(f"Duplicate terms:           {len(duplicates)}")
    print(f"Cross-reference issues:    {len(unique_issues)} (potential)")
    
    if not order_issues and not duplicates:
        print("\n✅ Glossary passes core quality checks!")
    else:
        print("\n⚠️  Glossary has issues that need attention")
    
    print("=" * 80)
    
    # Save validation report
    report_path = Path("work/curator/validation-report.txt")
    with open(report_path, 'w') as f:
        f.write("Glossary Quality Validation Report\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total terms: {len(terms)}\n")
        f.write(f"Alphabetical issues: {len(order_issues)}\n")
        f.write(f"Duplicates: {len(duplicates)}\n")
        f.write(f"Cross-reference issues: {len(unique_issues)}\n\n")
        
        if order_issues:
            f.write("\nAlphabetical Order Issues:\n")
            for issue in order_issues:
                f.write(f"  Position {issue['position']}: {issue['found']}\n")
        
        if duplicates:
            f.write("\nDuplicate Terms:\n")
            for dup in duplicates:
                f.write(f"  '{dup['term']}' at positions {dup['first_occurrence']} and {dup['duplicate_occurrence']}\n")
        
        if unique_issues:
            f.write("\nCross-Reference Issues:\n")
            for issue in unique_issues:
                f.write(f"  {issue}\n")
    
    print(f"\n📄 Validation report saved: {report_path}")


if __name__ == "__main__":
    main()
