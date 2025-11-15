import random
# from langchain_valyu import ValyuSearchTool



@tool
def search_the_web(API_KEY: str, query: str, max_result_num: int,relevance_threshold: int, search_type: str) -> dict:
    '''search the web for answer
    
        args:
            API_KEY: the api key for initialize the searching tool.(only composed by letters and numbers) Get one at platform.valyu.ai
            query: The query string for the search
            max_result_sum: Maximum number of results to return (1-20)
            relevance_threshold: Minimum relevance score for results (0.0-1.0)
            search_type: 
    '''
    search_tool = ValyuSearchTool(
    valyu_api_key=API_KEY,
    # Optional: configure search parameters (can also be set per-call)
    search_type=search_type,  # Search both proprietary and web sources
    max_num_results=max_result_num,   # Limit results
    relevance_threshold=relevance_threshold,  # Minimum relevance score
    # max_price=20.0  # Maximum cost in dollars
    )

    search_result = search_tool._run()



    