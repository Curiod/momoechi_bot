from whoosh import index
from whoosh.qparser import QueryParser
import asyncio

async def search_document(ix: index.Index, query_str: str):
    return await asyncio.to_thread(perform_search, ix, query_str)

def perform_search(ix: index.Index, query_str: str):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(' OR '.join(query_str.split()))
        results = searcher.search(query, limit=20)
        return [result.fields()['id'] for result in results]