from agent import build_search_agent , build_render_agent, writer_chain , critic_chain

def run_research_pipeline(topic:str)->dict:
    state = {}

    # websearch
    
    print("\n"+"=="*50)
    search_agent= build_search_agent()

    search_result= search_agent.invoke({
        'messages': [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state['search_result']= search_result['messages'][-1].content

    print(state['search_result'])

    print("Search Done")
    # render agent
    print("\n"+"=="*50)

    render_agent = build_render_agent()

    render_result = render_agent.invoke({
        'messages': [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })

    state['render_result'] = render_result['messages'][-1].content
    print(state['render_result'])
    print("Scrapping Done")
    # writer 
    print("\n"+"=="*50)  
    research_combine = {
     
        "research": {
f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['render_result']}"
        }
    }

    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research": research_combine
    })

    print(state['report'])

    print("Report Done")

    print("\n"+ "=="*50)
    #  critic 

    state['feedback'] =critic_chain.invoke({
        "report": state['report']
    })

    

    print("Final Result Done")


    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    result = run_research_pipeline(topic)

    print(result['report'])
    print(result['feedback'])