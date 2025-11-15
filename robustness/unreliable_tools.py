import logging
import random
import robustness.chaos_tools as chaos_tools
# from langchain_valyu import ValyuSearchTool


logger = logging.getLogger(__name__)
MAX_INPUT_LENGTH = 1024 # Example constraint

def validate_input(input_data: str):
    """
    Checks if the input is valid.
    Returns True if valid, False otherwise.
    """
    if not input_data:
        logger.warning("Validation failed: Input is empty.")
        return False
        
    if not isinstance(input_data, str):
        logger.warning("Validation failed: Input is not a string.")
        return False
        
    if len(input_data) > MAX_INPUT_LENGTH:
        logger.warning(f"Validation failed: Input exceeds {MAX_INPUT_LENGTH} chars.")
        return False
        
    logger.debug("Validation successful.")
    return True



def addition(nums: list[int]) -> dict:
    '''calculate the sum of several numbers.
        nums: list of numbers need to be add together

        result it return is a dict includes two parts, the first is the status of success of this function(1 for success, -1 for error).
        the second part is an int, the sum of all numbsers in nums.
    '''

    status = 1

    ans = 0
    for n in nums:
        ans += n
    
    return {"status":status, "result":ans}

def multiplication(nums: list[int]) -> dict:
    '''calculate the product of several numbers.
        nums: list of numbers need to be multiplied together

        result it return is a dict includes two parts, the first is the status of success of this function(1 for success, -1 for error).
        the second part is an int, the product of all numbsers in nums.
    '''

    status = 1

    ans = 1
    try:
        for n in nums:
            ans *= n
    except:
        status = -1
    
    result = {"status":status, "result":ans}
    
    return chaos_tools.null_result_executor(result)



# @tool
# def search_the_web(API_KEY: str, query: str, max_result_num: int,relevance_threshold: int, search_type: str) -> dict:
#     '''search the web for answer
    
#         args:
#             API_KEY: the api key for initialize the searching tool.(only composed by letters and numbers) Get one at platform.valyu.ai
#             query: The query string for the search
#             max_result_sum: Maximum number of results to return (1-20)
#             relevance_threshold: Minimum relevance score for results (0.0-1.0)
#             search_type: 
#     '''
#     search_tool = ValyuSearchTool(
#     valyu_api_key=API_KEY,
#     # Optional: configure search parameters (can also be set per-call)
#     search_type=search_type,  # Search both proprietary and web sources
#     max_num_results=max_result_num,   # Limit results
#     relevance_threshold=relevance_threshold,  # Minimum relevance score
#     # max_price=20.0  # Maximum cost in dollars
#     )

#     search_result = search_tool._run()



    