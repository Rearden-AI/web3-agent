For this Rearden AI Agent we have used:

- llama3-70B model (without fine-tuning);
- we are using RAG and vector DBs to store data in chunks;
- we have implemented LangChain to route request by different intents
    - we have several nodes for knowledge domains (like Sui docs and ecosystem) and nodes that are responsible for web3 actions (like transaction building);
    - when LangChain detects an intent related to web3 transaction, it refers to the RAG where exact formats and requirements are listed;
- as for now we have added to our agent:
    - Sui docs;
    - Sui meme coins ecosystem (FUD & SCB);
    - Sui transactions:
        - swaps on Cetus (with supported assets);

1. We build LangGraph nodes using LangChain chains and pass state object through these nodes.
2. Each LangGraph node is responsible for an atomic operation with LLM. Like decide if user want’s to know actual trending meme coins, find appropriate knowledge in documentation or execute some actions.
3. Each LangGraph node changes the state object, so we can handle one node’s result by the next node.
4. We can pass the state object right to the next node or to the router and he will will decide, which node will be activated next. E.g. first node found out that user needs a help with documentation, then router passes the state object to the node, that is responsible for work with documentation.
5. Iteratively passing the state object through nodes and routers we can handle any user’s request of any complexity by simply adding nodes that handle simple atomic tasks, making all the system robust and predictable.
6. Rearden is an open-source protocol and anyone is able to add new LangGraph nodes extending amount of covered domains based on public and transparent requests processing. The novel approach of we are currently developing at Rearden AI will significantly increase the speed of adding new nodes process, when any contributor will be able to extend Rearden capabilities and ~~conquer the world~~ make web3 world open for everyone.