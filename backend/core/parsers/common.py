import time

from langchain.schema import Document
from models.brains import Brain
from models.files import File
from models.settings import CommonsDep
from utils.vectors import Neurons
from logger import get_logger

logger = get_logger(__name__)


async def process_file(
    commons: CommonsDep,
    file: File,
    loader_class,
    enable_summarization,
    brain_id,
    user_openai_api_key,
):
    dateshort = time.strftime("%Y%m%d")

    file.compute_documents(loader_class)

    logger.info(f"Length of vectors: {len(file.documents)}")

    all_docs_with_metadata = []
    for doc in file.documents:  # pyright: ignore reportPrivateUsage=none
        logger.info(f"Document page : {doc.metadata['page']}")
        start_time = time.time()
        metadata = {
            "file_sha1": file.file_sha1,
            "file_size": file.file_size,
            "file_name": file.file_name,
            "chunk_size": file.chunk_size,
            "chunk_overlap": file.chunk_overlap,
            "date": dateshort,
            "summarization": "true" if enable_summarization else "false",
        }

        doc_with_metadata = Document(page_content=doc.page_content, metadata=metadata)
        all_docs_with_metadata.append(doc_with_metadata)
        logger.info(f"Time to create one document: {time.time() - start_time} seconds")

        # start_time = time.time()
        
        # logger.info(f"Time to create one neuron: {time.time() - start_time} seconds")

        start_time = time.time()
        
        logger.info(f"Time to create one neuron vector: {time.time() - start_time} seconds")
        
        # add_usage(stats_db, "embedding", "audio", metadata={"file_name": file_meta_name,"file_type": ".txt", "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})

        # created_vector_id = created_vector[0]  # pyright: ignore reportPrivateUsage=none

       
        
        # start_time = time.time()
        # brain.create_brain_vector(created_vector_id, file.file_sha1)
        # logger.info(f"Time to create one brain vector: {time.time() - start_time} seconds")

    neurons = Neurons(commons=commons)
    created_vectors = neurons.create_vectors(all_docs_with_metadata, user_openai_api_key)
    brain = Brain(id=brain_id)

    brain.create_brain_vectors(created_vectors, file.file_sha1)
    print(created_vectors[0])
    return
