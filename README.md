# Custom Components Wheels
Custom components wheels hosted by Home Assistant repository

## Custom component provider

Add a custom_components.json to components folder like:

```json
{
  "name": "Name of Component",
  "owner": ["owner"],
  "manifest": "https://url/of/manifest.json",
  "url": "https://url/of/component"
}
```

**Note**: All URLs in the JSON must be direct links. URLs with HTTP redirects (301 or 302) redirects will not be followed.
