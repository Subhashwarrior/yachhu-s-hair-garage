import streamlit as st
import needle

# Define the FAQ tool (same as in your main bot)
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
    if any(k in q for k in ["return", "refund", "exchange", "send back", "item back", "return it"]):
        result = answers["returns"]
    elif any(k in q for k in ["ship", "delivery", "shipping", "track", "deliver"]):
        result = answers["shipping"]
    elif any(k in q for k in ["warranty", "guarantee", "broken", "defect"]):
        result = answers["warranty"]
    elif any(k in q for k in ["hour", "open", "close", "time", "store open", "business hours"]):
        result = answers["hours"]
    elif any(k in q for k in ["price", "cost", "discount", "bulk", "pricing"]):
        result = answers["pricing"]
    elif any(k in q for k in ["contact", "email", "phone", "call", "support"]):
        result = answers["contact"]
    elif any(k in q for k in ["privacy", "data", "gdpr", "secret", "information"]):
        result = answers["privacy"]
    else:
        result = "No FAQ found. Contact support@company.com for help."
    return {"query": query, "answer": result, "grounded": True}

# Cache the agent so it's not recreated on every interaction
@st.cache_resource
def get_agent():
    return needle.Needle(tools=[faq_lookup],
                         system="You are BizAssist, a helpful business FAQ assistant. "
                                "When a customer asks a question, use the faq_lookup tool. "
                                "Always respond with the exact answer from the tool — never invent prices, policies, or procedures. "
                                "Keep answers under 3 sentences. Be professional and friendly.")

agent = get_agent()

st.title("🤖 BizAssist FAQ Chatbot")
st.caption("Powered by Needle 3 (121M params) — runs on CPU, no GPU needed")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about our business..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Run the agent
            result = agent.run(prompt)

            # Extract answer: try agent results first, then fallback to direct tool call
            answer = None
            if result.get('results'):
                for r in result['results']:
                    if isinstance(r, dict) and 'answer' in r:
                        answer = r['answer']
                        break
            if not answer:
                # Fallback: call the tool directly (guaranteed to work)
                direct = faq_lookup(prompt)
                answer = direct['answer']

            st.markdown(answer)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar with info
with st.sidebar:
    st.header("About")
    st.write("""
    This demo uses **Needle 3** — a 121M parameter foundation model designed for
    tool-calling and structured extraction. It runs entirely on CPU (~30MB total footprint).

    **How it works:**
    1. Your question → Needle 3 intent classifier
    2. Needle calls the `faq_lookup` tool with your full query
    3. The tool returns a business answer from our knowledge base
    4. The answer is displayed back to you

    If the question is outside our FAQ scope, the bot will politely refuse
    (you'll see a message like "No FAQ found...") rather than making up information.
    """)
    st.divider()
    st.subheader("Technical Specs")
    st.code("""
    Model: Needle 3 (Cactus Compute)
    Parameters: 121M total (~50M arithmetic)
    Size: 29MB .cact (2-bit quantized)
    Engine: ~1MB C++ binary
    Hardware: CPU only (phone, watch, laptop)
    """)
    st.caption("Built for the MBA FAQ Chatbot Project")