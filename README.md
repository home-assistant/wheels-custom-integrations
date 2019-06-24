[![Build Status](https://dev.azure.com/home-assistant/Hass.io/_apis/build/status/custom-components-wheels?branchName=master)](https://dev.azure.com/home-assistant/Hass.io/_build/latest?definitionId=14&branchName=master)

# Custom Components Wheels
Custom components wheels hosted by Home Assistant repository

## Custom component provider

Add a custom_components.json to components folder like:

```json
{
  "name": "Name of Component",
  "owner": ["@owner"],
  "manifest": "https://url/of/manifest.json",
  "url": "https://url/of/component",
}
```
