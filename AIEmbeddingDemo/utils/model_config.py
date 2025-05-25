from config import CONSTS
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding


##################### AZURE OPENAI CONFIGURATION ############################

azure_openai_llm = AzureOpenAI(
                    model=CONSTS.model_name,
                    deployment_name=CONSTS.engine_name,
                    api_key=CONSTS.api_key,
                    azure_endpoint=CONSTS.api_endpoint,
                    api_version=CONSTS.api_version,
                    )

azure_openai_embed_model = AzureOpenAIEmbedding(
                    model=CONSTS.emb_model_name,
                    deployment_name=CONSTS.emb_engine_name,
                    api_key=CONSTS.api_key,
                    azure_endpoint=CONSTS.api_endpoint,
                    api_version=CONSTS.api_version,
                    )

#############################################################################