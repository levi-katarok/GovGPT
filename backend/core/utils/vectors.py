from concurrent.futures import ThreadPoolExecutor
from typing import List

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from llm.utils.summarization import llm_summerize
from logger import get_logger
from models.settings import BrainSettings, CommonsDep, common_dependencies
from pydantic import BaseModel

logger = get_logger(__name__)


class Neurons(BaseModel):
    commons: CommonsDep
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none

    def create_vector(self, doc, user_openai_api_key=None):
        logger.info("adding new vector for document")
        if user_openai_api_key:
            self.commons["documents_vector_store"]._embedding = OpenAIEmbeddings(
                openai_api_key=user_openai_api_key
            )  # pyright: ignore reportPrivateUsage=none
        try:
            sids = self.commons["documents_vector_store"].add_documents([doc])
            if sids and len(sids) > 0:
                return sids

        except Exception as e:
            logger.error(f"Error creating vector for document {e}")

    def create_vectors(self, doc_array, user_openai_api_key=None):
        logger.info("adding new vector for document")
        if user_openai_api_key:
            self.commons["documents_vector_store"]._embedding = OpenAIEmbeddings(
                openai_api_key=user_openai_api_key
            )  # pyright: ignore reportPrivateUsage=none
        try:
            sids = self.commons["documents_vector_store"].add_documents(doc_array)
            if sids and len(sids) > 0:
                return sids

        except Exception as e:
            logger.error(f"Error creating vector for document {e}")

    def create_embedding(self, content):
        return self.commons["embeddings"].embed_query(content)

    def similarity_search(self, query, table="match_summaries", top_k=5, threshold=0.5):
        query_embedding = self.create_embedding(query)
        summaries = (
            self.commons["supabase"]
            .rpc(
                table,
                {
                    "query_embedding": query_embedding,
                    "match_count": top_k,
                    "match_threshold": threshold,
                },
            )
            .execute()
        )
        return summaries.data


def create_summary(commons: CommonsDep, document_id, content, metadata):
    logger.info(f"Summarizing document {content[:100]}")
    summary = llm_summerize(content)
    logger.info(f"Summary: {summary}")
    metadata["document_id"] = document_id
    summary_doc_with_metadata = Document(page_content=summary, metadata=metadata)
    sids = commons["summaries_vector_store"].add_documents([summary_doc_with_metadata])
    if sids and len(sids) > 0:
        commons["supabase"].table("summaries").update(
            {"document_id": document_id}
        ).match({"id": sids[0]}).execute()


def error_callback(exception):
    print("An exception occurred:", exception)


def process_batch(batch_ids: List[str]):
    commons = common_dependencies()
    supabase = commons["supabase"]
    try:
        if len(batch_ids) == 1:
            return (
                supabase.table("vectors")
                .select(
                    "name:metadata->>file_name, size:metadata->>file_size",
                    count="exact",
                )
                .eq("id", batch_ids[0])  # Use parameter binding for single ID
                .execute()
            ).data
        else:
            return (
                supabase.table("vectors")
                .select(
                    "name:metadata->>file_name, size:metadata->>file_size",
                    count="exact",
                )
                .in_("id", batch_ids)  # Use parameter binding for multiple IDs
                .execute()
            ).data
    except Exception as e:
        logger.error("Error retrieving batched vectors", e)


def get_unique_files_from_vector_ids(vectors_ids: List[str]):
    # Move into Vectors class
    """
    Retrieve unique user data vectors.
    """

    # constants
    BATCH_SIZE = 5

    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(vectors_ids), BATCH_SIZE):
            batch_ids = vectors_ids[i : i + BATCH_SIZE]
            future = executor.submit(process_batch, batch_ids)
            futures.append(future)

        # Retrieve the results
        vectors_responses = [future.result() for future in futures]

    documents = [item for sublist in vectors_responses for item in sublist]
    unique_files = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    return unique_files
