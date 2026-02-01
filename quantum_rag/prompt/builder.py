def build_prompt(query, docs):
    ctx = "\n".join(docs)
    return f"""Answer using the context.

Context:
{ctx}

Question:
{query}
"""
