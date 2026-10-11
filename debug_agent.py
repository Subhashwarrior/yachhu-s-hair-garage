import needle
import json

@needle.tool
def faq_lookup(query: str):
    """Retrieve a business FAQ answer from the user's query text."""
    q = query.lower()
    answers = {
        "returns": "30-day return policy. Original packaging required. Refunds: 5-7 business days.",
        "shipping": "Standard: 3-5 days. Expedited available. International rates vary.",
        "warranty": "1-year limited warranty on all products. Extended warranties available.",
        "hours": "Mon-Fri 9AM-6PM EST. Weekend: email only.",
        "pricing": "Competitive pricing. Bulk discounts start at $1,000.",
        "contact": "support@company.com or (555) 123-4567. Response within 24h.",
        "privacy": "Data encrypted. No info sold. GDPR compliant.",
    }
    if any(k in q for k in ["return", "refund", "exchange", "send back"]):
        result = answers["returns"]
    elif any(k in q for k in ["ship", "delivery", "shipping", "track"]):
        result = answers["shipping"]
    elif any(k in q for k in ["warranty", "guarantee", "broken"]):
        result = answers["warranty"]
    elif any(k in q for k in ["hour", "open", "close", "time"]):
        result = answers["hours"]
    elif any(k in q for k in ["price", "cost", "discount", "bulk"]):
        result = answers["pricing"]
    elif any(k in q for k in ["contact", "email", "phone", "call"]):
        result = answers["contact"]
    elif any(k in q for k in ["privacy", "data", "gdpr", "secret"]):
        result = answers["privacy"]
    else:
        result = "No FAQ found. Contact support@company.com for help."
    return {"query": query, "answer": result, "grounded": True}

# Create agent and inspect its internal state
agent = needle.Needle(tools=[faq_lookup])

print("=== AGENT DEBUG INFO ===")
print(f"Number of tools: {agent._n_tools}")
print(f"Tools JSON: {agent._tools_json}")
print(f"Functions dict: {list(agent._functions.keys())}")
print(f"Tool schemas: {agent._tool_schemas}")
print()

# Test the tool directly first
print("=== DIRECT TOOL TEST ===")
direct_result = faq_lookup("Can I return an item?")
print(f"Direct result: {direct_result}")
print()

# Now test through agent
print("=== AGENT RUN TEST ===")
result = agent.run("Can I return an item I bought last week?")
print(f"Query: Can I return an item I bought last week?")
print(f"Response type: {result.get('type')}")
print(f"Reasoning: {result.get('reasoning')}")
print(f"Confidence: {result.get('confidence')}")
print(f"Function calls: {result.get('function_calls')}")
print(f"Results: {result.get('results')}")
print()

# Let's also test a simpler query
print("=== SIMPLE QUERY TEST ===")
result2 = agent.run("return")
print(f"Query: return")
print(f"Response type: {result2.get('type')}")
print(f"Reasoning: {result2.get('reasoning')}")
print(f"Confidence: {result2.get('confidence')}")
print(f"Function calls: {result2.get('function_calls')}")
print(f"Results: {result2.get('results')}")