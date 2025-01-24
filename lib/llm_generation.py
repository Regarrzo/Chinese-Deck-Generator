import llm
from joblib import Memory

# Model with strong Chinese performance
model = llm.get_model("openrouter/deepseek/deepseek-chat")
memory = Memory("cachedir")

# Crime against humanity, but it works
def error_try_again(f):
    def wrapper(*args, **kwargs):
        for i in range(10):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
        
        raise ValueError("Tried regenerating LLM output 10 times and failed each time. Something is wrong.")
    
    return wrapper

@memory.cache
@error_try_again
def llm_is_sentence_good(sentence: str):
    prompt = f"Is this Chinese sentence gramatically correct? Answer with only the letter Y if yes and N if no. {sentence}"
    response = model.prompt(prompt, stream=False, max_tokens=1, temperature=0.0)

    if "Y" in response:
        return True
    elif "N" in response:
        return False
    else:
        raise ValueError(f"Unexpected response: {response}")
    
@memory.cache
@error_try_again
def llm_make_example_sentences(word: str, n=3):
    prompt = f'列出使用此词的 {n} 个例句。每个示例都用 <br> 分隔，并以"1. example<br>2. example<br>..." 的形式编号： {word}'
    response = str(model.prompt(prompt, stream=False, max_tokens=250))
    response.replace("<br>", "\n")
    response.replace("\n\n", "\n")
    return response

@memory.cache
@error_try_again
def llm_definition_and_pinyin(word: str):
    example = "hǎo: good\nhào: to be fond of; to have a tendency to; to be prone to"
    prompt = f"ALWAYS stick with the same format as the example: {example}. Write the English definition(s) of the word {word} along with the pinyin pronunciation(s):"
    response = str(model.prompt(prompt, stream=False, max_tokens=250))
    
    definition_and_pinyin = response

    # get just the definitions
    definitions = definition_and_pinyin.split("\n")
    definitions = [definition.split(":")[1].strip() for definition in definitions]
    definitions = "\n".join(definitions)

    # get just the pinyin
    pinyin = definition_and_pinyin.split("\n")
    pinyin = [pinyin.split(":")[0].strip() for pinyin in pinyin]
    pinyin = "\n".join(pinyin)

    return definition_and_pinyin, definitions, pinyin

@memory.cache
@error_try_again
def llm_get_traditional_version(word: str):
    prompt = f"只回应一个词。其他什么都别写。《{word}》的繁体字是: "
    response = str(model.prompt(prompt, stream=False, max_tokens=50))
    return response
