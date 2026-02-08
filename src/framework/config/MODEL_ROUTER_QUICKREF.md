# Model Router Quick Reference

## Configuration Location
```
ops/config/model_router.yaml
```

## Validation Script
```bash
# Basic validation
python ops/scripts/validate-model-router.py

# Strict mode (warnings as errors)
python ops/scripts/validate-model-router.py --strict

# JSON output for CI
python ops/scripts/validate-model-router.py --format json

# Validate custom file
python ops/scripts/validate-model-router.py --file /path/to/config.yaml
```

## Quick Model Reference

### By Role
- **Analysis:** claude-3-opus → gpt-5-pro → llama-3.1-70b-instruct
- **Creative:** gpt-5-turbo → claude-3-sonnet → llama-3.2-vision
- **Coding:** codestral-latest → deepseek-coder-v2 → llama-3.1-8b-instruct
- **General:** claude-3-sonnet → gpt-4.1-turbo → llama-3.1-70b-instruct

### By Router
- **OpenRouter:** GPT-5, GPT-4.1, Claude 3, Llama 3.1 (large), DeepSeek Chat
- **OpenCode.ai:** Codestral, DeepSeek Coder, Llama 3.1 (small)
- **Direct API:** GPT-4.1-preview (advanced features)

### Pricing Tiers
- **Premium:** $10-15/1K input, $30-75/1K output (GPT-5 Pro, Claude Opus)
- **Mid-tier:** $3-5/1K input, $10-15/1K output (GPT-4.1, Claude Sonnet)
- **Budget:** $0.06-0.5/1K input, $0.06-1.5/1K output (Llama, DeepSeek)

### Context Windows
- **Small (8K-32K):** Codestral, DeepSeek Chat
- **Large (128K):** GPT-4.1, GPT-5, Llama 3.1, DeepSeek Coder
- **XLarge (200K):** Claude 3 series, GPT-5 Pro

## Adding New Models

1. Copy an existing model entry as template
2. Update: router, identifier, context_window, pricing, default_role
3. Set fallback_to (another model key or null)
4. Add new capabilities to allowed_capabilities list if needed
5. Run validator: `python ops/scripts/validate-model-router.py`
6. Run tests: `pytest validation/model_router/`

## Fallback Chain Example
```yaml
gpt-5-pro:
  fallback_to: gpt-5-turbo
  
gpt-5-turbo:
  fallback_to: gpt-4.1-turbo
  
gpt-4.1-turbo:
  fallback_to: claude-3-sonnet
  
claude-3-sonnet:
  fallback_to: llama-3.1-70b-instruct
  
llama-3.1-70b-instruct:
  fallback_to: llama-3.1-8b-instruct
  
llama-3.1-8b-instruct:
  fallback_to: null  # Terminal fallback
```

## Testing
```bash
# Run all tests
pytest validation/model_router/ -v

# Run acceptance tests only
pytest validation/model_router/test_acceptance.py -v

# Run unit tests only
pytest validation/model_router/test_unit.py -v
```

## References
- [ADR-020: Multi-Tier Agentic Runtime](../../docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md)
- [ADR-021: Model Routing Strategy](../../docs/architecture/adrs/ADR-021-model-routing-strategy.md)
- [Platform Next Steps](../../docs/architecture/assessments/platform_next_steps.md)
- [Work Log](../../work/logs/build-automation/2025-11-30T1201-build-automation-model-router-config.md)
