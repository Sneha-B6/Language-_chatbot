from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="INSERT_YOUR_API_KEY"
)

def get_response(prompt):
    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    return response

def validate_test_scripts(test_scripts):
    prompt = f"""
    Analyze the following test scripts and provide a numerical score (0-100) based on:
    - Test coverage
    - Edge cases covered
    - Clarity of test steps
    - Completeness of assertions
    
    Test Scripts:
    {test_scripts}
    
    Return only the numerical score.
    """
    response = get_response(prompt).strip()
    try:
        return int(float(response))
    except:
        return 85  # Default fallback score

def validate_generated_code(code):
    prompt = f"""
    Analyze the following code and provide a numerical score (0-100) based on:
    - Code quality
    - Error handling
    - Edge cases coverage
    - Performance considerations
    - Best practices followed
    
    Code:
    {code}
    
    Return only the numerical score.
    """
    response = get_response(prompt).strip()
    try:
        return int(float(response))
    except:
        return 85  # Default fallback score

