from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_name: str = "Nexora UniSphere AI"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    api_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"

    # --- Supabase ---
    supabase_url: str = "https://your-project.supabase.co"
    supabase_anon_key: str = "your-supabase-anon-key"
    supabase_service_key: str = "your-supabase-service-role-key"

    # --- Pinecone ---
    pinecone_api_key: str = "your-pinecone-api-key"
    pinecone_index_name: str = "nexora-university"
    pinecone_environment: str = "us-east-1"
    pinecone_host: str = ""  # For serverless indexes: https://nexora-university-xxxx.svc.aped-xxxx.pinecone.io

    # --- Groq (Llama 3.3 70B Instruct) ---
    groq_api_key: str = "your-groq-api-key"
    groq_model: str = "llama-3.3-70b-versatile"

    # --- Embeddings (HuggingFace Inference API — BAAI/bge-large-en-v1.5) ---
    hf_api_token: str = ""  # Get free token from https://huggingface.co/settings/tokens
    embedding_model: str = "BAAI/bge-large-en-v1.5"
    embedding_dimension: int = 1024

    # --- Knowledge Base ---
    knowledge_base_path: str = "../knowledge_base"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def clean_pinecone_index(self) -> str:
        return self.pinecone_index_name.strip()

    @property
    def clean_pinecone_host(self) -> str:
        return self.pinecone_host.strip()


settings = Settings()
