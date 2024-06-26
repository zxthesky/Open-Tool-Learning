# Open Tool Learning

## Ⅰ Support

### LLM

`LLaMA`

### Dataset



### Retriever




## Ⅱ Format

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




## Ⅲ Code Catalog

### agent

core class

### chat

chat history and chat template

### data

data preprocessing，load

### document

extra document process module for RAG

### LLM

foundation model

### process

format the answer text, ...

### retrieval

### tool

tool_pool information and execution

### types

type checking

### utils

logging , file io

