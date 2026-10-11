import needle

def get_weather(city: str):
    """Get current weather for a city."""
    return {"city": city, "temp_c": 27, "sky": "clear"}

# Create the AI agent bound to your tool
agent = needle.Needle(tools=[get_weather])

# Run a query
result = agent.run("what is the weather in Lagos?")
print("Full result:", result)
print("Tool calls:", result.get("function_calls"))
print("Executed results:", result.get("results"))
print("Confidence score:", result.get("confidence"))
