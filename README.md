# ezoidc - Buildkite plugin


## Example

Add the following to your `pipeline.yml`:

```yaml
steps:
  - label: Load variables
    command: |
      ...
    plugins: 
      - ezoidc/kv#v1:
          org: org-name
```

## Configuration

### `org` (Required, string)

