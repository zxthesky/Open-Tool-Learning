# Open Tool Learning


### LLM



### Dataset

API-Bank

ToolEyes

ToolTalk

SoAyBench

### Tool Format

```python
{
    "name": "get_current_temperature",
    "description": "Get the current temperature for a specific location",
    "parameters": 
    {
          "type": "object",
          "properties": 
           {
            "location": {
              "type": "string",
              "description": "The city and state, e.g., San Francisco, CA"
            },
            "unit": {
              "type": "string",
              "enum": ["Celsius", "Fahrenheit"],
              "description": "The temperature unit to use. Infer this from the user's location."
            }
     },
     "required": ["location", "unit"]
}
```

### Chat Template

