#!/usr/bin/env python3
"""
Fake claude-code CLI for integration testing.

This script simulates the claude-code CLI behavior for testing purposes,
accepting --model and --prompt parameters and returning realistic responses.

Usage:
    fake_claude_cli.py --model <model> --prompt <prompt>

Examples:
    fake_claude_cli.py --model claude-3-opus-20240229 --prompt "Write code"
"""

import sys
import json
import time
import argparse


def main():
    """Main entry point for fake claude CLI."""
    parser = argparse.ArgumentParser(description="Fake claude-code CLI for testing")
    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--prompt", required=True, help="User prompt")
    parser.add_argument("--format", default="text", choices=["text", "json"], 
                       help="Output format")
    parser.add_argument("--error", default=None, 
                       help="Simulate error (values: invalid-model, timeout, api-error)")
    parser.add_argument("--delay", type=float, default=0.1,
                       help="Simulated processing delay in seconds")
    
    args = parser.parse_args()
    
    # Simulate processing delay
    time.sleep(args.delay)
    
    # Handle error simulation
    if args.error == "invalid-model":
        print(f"Error: Invalid model '{args.model}'", file=sys.stderr)
        print("Valid models: claude-3-opus-20240229, claude-3-5-sonnet-20240620, claude-3-haiku-20240307", 
              file=sys.stderr)
        sys.exit(1)
    
    elif args.error == "timeout":
        # Simulate hanging (wait longer than typical test timeout)
        time.sleep(60)
        sys.exit(1)
    
    elif args.error == "api-error":
        print("Error: API authentication failed", file=sys.stderr)
        print("Please check your ANTHROPIC_API_KEY environment variable", file=sys.stderr)
        sys.exit(2)
    
    # Validate model (basic check)
    valid_models = [
        "claude-3-opus-20240229",
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307"
    ]
    
    if args.model not in valid_models:
        print(f"Warning: Model '{args.model}' not in standard list", file=sys.stderr)
    
    # Generate response based on prompt
    response_text = generate_response(args.prompt, args.model)
    
    # Output in requested format
    if args.format == "json":
        output_json(response_text, args.model, args.prompt)
    else:
        output_text(response_text)


def generate_response(prompt: str, model: str) -> str:
    """
    Generate simulated LLM response based on prompt.
    
    Args:
        prompt: User prompt
        model: Model name
    
    Returns:
        Simulated response text
    """
    # Generate different responses based on prompt content
    prompt_lower = prompt.lower()
    
    if "write" in prompt_lower and "function" in prompt_lower:
        return """def example_function(x, y):
    '''
    Example function that adds two numbers.
    
    Args:
        x: First number
        y: Second number
    
    Returns:
        Sum of x and y
    '''
    return x + y"""
    
    elif "error" in prompt_lower or "fail" in prompt_lower:
        return "I notice you're asking about errors. Here's an example of error handling in Python:\n\ntry:\n    result = risky_operation()\nexcept Exception as e:\n    print(f'Error: {e}')"
    
    elif "test" in prompt_lower:
        return "Here's a simple test example using pytest:\n\ndef test_addition():\n    assert 1 + 1 == 2\n    assert 2 + 2 == 4"
    
    else:
        # Generic response
        return f"This is a simulated response from {model} for the prompt: '{prompt[:50]}...'"


def output_text(response_text: str):
    """Output response as plain text."""
    print(response_text)


def output_json(response_text: str, model: str, prompt: str):
    """Output response as JSON with metadata."""
    output = {
        "response": response_text,
        "model": model,
        "tokens": len(response_text.split()) + len(prompt.split()),
        "cost_usd": 0.01,  # Fake cost
        "metadata": {
            "prompt_length": len(prompt),
            "response_length": len(response_text),
        }
    }
    
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
