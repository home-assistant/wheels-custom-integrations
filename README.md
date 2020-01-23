[![Build Status](https://dev.azure.com/home-assistant/Hass.io/_apis/build/status/custom-components%20CI?branchName=master)](https://dev.azure.com/home-assistant/Hass.io/_build/latest?definitionId=46&branchName=master)

# Custom Components Wheels
Custom components wheels hosted by Home Assistant repository

## Custom component provider

Add a custom_components.json to components folder like:

```json
{
  "name": "Name of Component",
  "owner": ["owner"],
  "manifest": "https://url/of/manifest.json",
  "url": "https://url/of/component",
}
```
**Note all links in the json must be direct links as http 302 redirects will not be followed.**
