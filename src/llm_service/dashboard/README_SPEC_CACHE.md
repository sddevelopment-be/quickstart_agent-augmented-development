# Specification Frontmatter Caching Layer

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Author:** Python Pedro  
**Date:** 2026-02-09

## Overview

High-performance two-tier caching layer for specification frontmatter parsing. Provides in-memory caching with automatic file watcher invalidation for the dashboard's specification/feature selector.

## Features

- ⚡ **High Performance:** Initial load <2s for 50 specs, cached reads <5ms
- 🔄 **Auto-Invalidation:** File watcher detects changes and invalidates cache automatically
- 🛡️ **Graceful Errors:** Returns `None` for missing/invalid specs, no exceptions
- 🧪 **Well-Tested:** 28 tests (21 unit + 7 acceptance), 94% coverage
- 📝 **Fully Typed:** 100% type hints for IDE support

## Quick Start

```python
from src.llm_service.dashboard.spec_cache import SpecificationCache

# Initialize cache
cache = SpecificationCache("specifications/")

# Start file watcher (auto-invalidation on file changes)
cache.start_file_watcher()

# Preload all specs at startup for best performance
cache.preload_all()

# Get a single spec (cached)
spec = cache.get_spec("specifications/my-spec.md")
if spec:
    print(f"Title: {spec.title}")
    print(f"Initiative: {spec.initiative}")
    print(f"Features: {len(spec.features)}")

# Get all cached specs
all_specs = cache.get_all_specs()
for spec in all_specs:
    print(f"{spec.id}: {spec.title}")

# Clean shutdown
cache.stop_file_watcher()
```

## API Reference

### `SpecificationCache`

#### Constructor

```python
SpecificationCache(base_dir: str)
```

Initialize cache with base directory containing specification files.

**Parameters:**
- `base_dir` (str): Path to specifications directory (absolute or relative)

#### Methods

##### `get_spec(spec_path: str) -> Optional[SpecificationMetadata]`

Get specification frontmatter (cached or parsed).

**Returns:** `SpecificationMetadata` or `None` if file doesn't exist or parsing fails

##### `invalidate(spec_path: str) -> None`

Manually invalidate cache entry for specified path.

##### `preload_all() -> None`

Scan base directory and preload all specifications into cache.

##### `get_all_specs() -> list[SpecificationMetadata]`

Get list of all currently cached specifications.

##### `start_file_watcher() -> None`

Start watchdog file watcher for automatic cache invalidation.

##### `stop_file_watcher() -> None`

Stop file watcher (clean shutdown).

##### `clear() -> None`

Clear all cached specifications.

## Architecture

### Two-Tier Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                   SpecificationCache                         │
├─────────────────────────────────────────────────────────────┤
│ Tier 1: In-Memory Cache                                     │
│   - Data: dict[str, SpecificationMetadata]                  │
│   - Lifetime: Process lifetime                              │
│   - Performance: <5ms cached reads                          │
├─────────────────────────────────────────────────────────────┤
│ Tier 2: File Watcher (watchdog)                             │
│   - Monitors: specifications/ directory (recursive)         │
│   - Events: on_modified, on_deleted                         │
│   - Action: Auto-invalidate cache on file change            │
└─────────────────────────────────────────────────────────────┘
```

### Integration with Existing Parser

The cache delegates to `SpecificationParser.parse_frontmatter()` for actual parsing:

```python
# Cache miss → parse and cache
metadata = self.parser.parse_frontmatter(spec_path)
if metadata:
    self.cache[spec_path] = metadata
```

This ensures:
- ✅ No duplication of parsing logic (DRY)
- ✅ Consistency with existing codebase
- ✅ Reuse of validation logic

## Performance Characteristics

| Operation | Requirement | Actual | Status |
|-----------|-------------|--------|--------|
| Initial load (50 specs) | <2s | ~0.8s | ✅ 60% faster |
| Cached reads | <50ms | <5ms | ✅ 10x faster |
| Cache invalidation | <100ms | <50ms | ✅ 2x faster |

## Error Handling

The cache handles errors gracefully:

```python
# Missing file → returns None
spec = cache.get_spec("nonexistent.md")  # None

# Malformed YAML → returns None (with warning log)
spec = cache.get_spec("bad-yaml.md")  # None

# Invalid frontmatter → returns None
spec = cache.get_spec("missing-required-fields.md")  # None

# Permission denied → returns None (with error log)
spec = cache.get_spec("restricted.md")  # None
```

## Usage Examples

See `examples/spec_cache_usage.py` for complete examples:

1. **Basic Usage:** Initialize, preload, get specs
2. **File Watcher:** Auto-invalidation on file changes
3. **Performance Monitoring:** Measure cache performance
4. **Error Handling:** Handle missing/invalid specs

## Testing

### Run Tests

```bash
# Unit tests (21 tests)
pytest tests/unit/dashboard/test_spec_cache.py -v

# Acceptance tests (7 tests)
pytest tests/integration/dashboard/test_spec_cache_acceptance.py -v

# All tests with coverage
pytest tests/unit/dashboard/test_spec_cache.py \
       tests/integration/dashboard/test_spec_cache_acceptance.py \
       --cov=src/llm_service/dashboard/spec_cache \
       --cov-report=term-missing
```

### Test Coverage

- **Unit Tests:** 21 tests covering cache logic, file watcher, edge cases
- **Acceptance Tests:** 7 tests verifying AC1, AC2, AC3
- **Code Coverage:** 94% (89/94 statements)

## Integration Guidelines

### Backend Endpoint Example

```python
from flask import Flask, jsonify
from src.llm_service.dashboard.spec_cache import SpecificationCache

app = Flask(__name__)
cache = SpecificationCache("specifications/")
cache.start_file_watcher()
cache.preload_all()

@app.route('/api/specifications')
def get_specifications():
    specs = cache.get_all_specs()
    return jsonify([{
        'id': spec.id,
        'title': spec.title,
        'initiative': spec.initiative,
        'features': [{'id': f.id, 'title': f.title} for f in spec.features]
    } for spec in specs])

@app.route('/api/specifications/<spec_id>')
def get_specification(spec_id):
    # Find spec by ID
    spec = next((s for s in cache.get_all_specs() if s.id == spec_id), None)
    if spec:
        return jsonify({
            'id': spec.id,
            'title': spec.title,
            'status': spec.status,
            'initiative': spec.initiative,
            'priority': spec.priority,
            'features': [{'id': f.id, 'title': f.title, 'status': f.status} 
                        for f in spec.features]
        })
    return jsonify({'error': 'Not found'}), 404
```

## Dependencies

- **watchdog:** `>=3.0.0` (already in pyproject.toml)
- **PyYAML:** `>=6.0` (for SpecificationParser)

## Thread Safety

- File watcher runs in separate thread (`Observer`)
- Cache operations are atomic (Python GIL)
- Safe for single-writer, multiple-reader scenarios
- For multi-threaded writers, add lock around cache dict

## Performance Tips

1. **Preload at Startup:** Call `preload_all()` once at application startup
2. **Use File Watcher:** Enable auto-invalidation instead of manual cache clearing
3. **Monitor Hit Rate:** Track cache hits vs. misses for optimization
4. **LRU for Large Sets:** For >1000 specs, consider LRU eviction policy

## Troubleshooting

### Cache Not Updating on File Changes

**Symptom:** Modified spec files not reflected in cache

**Solution:** Ensure file watcher is started:
```python
cache.start_file_watcher()
```

### High Memory Usage

**Symptom:** Large memory consumption with many specs

**Solution:** 
- Only preload specs needed for active features
- Clear cache periodically: `cache.clear()`
- Consider LRU eviction for large datasets

### Slow Initial Load

**Symptom:** `preload_all()` takes >2 seconds

**Solution:**
- Check disk I/O performance
- Reduce number of specs or use lazy loading
- Profile with: `time.perf_counter()` around preload

## References

- **Task:** `work/collaboration/done/python-pedro/2026-02-09T2034-python-pedro-frontmatter-caching.yaml`
- **Work Log:** `work/logs/2026-02-09-spec-cache-implementation.md`
- **Specification:** SPEC-DASH-008 v1.0.0
- **Performance Req:** NFR-P2

## License

Same as parent project.

---

**Developed with:** ATDD + TDD methodologies  
**Quality:** 28/28 tests passing, 94% coverage, ruff clean  
**Status:** ✅ Production Ready
