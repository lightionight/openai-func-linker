# this file using for description function format for pinecone save ##


## function format

- function_name: 
- function_keyword: use for match user search base on user input
- function_url: where the function context it is, for now just using github via jsdelivr to fetch it.
- function_category: function category, there using still considering

vector store in pinecone, and using pinecone search to match user input, and return the function vector, then using the function vector to fetch the function context from github via jsdelivr.

vector store function keyword
'''

'''

pinecone store context format
'''
{
    "name": "abs",
    "keyword": ["abs"],
    "url": "https://cdn.jsdelivr.net/gh/DevilTea/pinecone/function_vector/abs.md",
    "category": "math"
}
'''