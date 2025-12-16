from datetime import datetime, timezone
from typing import List, Optional, Literal
from enum import Enum
import uuid
import hashlib
from pydantic import BaseModel, Field, computed_field, model_validator

# ==========================================
# 1. INFRASTRUCTURE TAXONOMY (The Body)
# ==========================================

class StorageTier(str, Enum):
    """
    Physical data gravity mapping.
    Optimized for heterogeneous compute topologies (RAM -> NVMe -> ZFS -> Tape).
    """
    T0_HOT_RAM = "T0_RAM_Graph"     # NetworkX Graph (Millisecond Access)
    T1_HOT_NVME = "T1_NVMe_Index"   # Active Vector Index (Qdrant/Milvus)
    T2_WARM_POOL = "T2_ZFS_Pool"    # Active Project Context
    T3_COLD_LAKE = "T3_QNAP_Main"   # Archived Memory Lake
    T4_DEEP_ARCHIVE = "T4_QNAP_Sec" # Immutable Audit Logs

class DataClassification(str, Enum):
    """
    Security Access Control List (SACL).
    'RESTRICTED' triggers hardware-enforced audit logging (Optical Diode).
    """
    PUBLIC = "public"           # Safe for external consensus
    INTERNAL = "internal"       # Local inference only
    RESTRICTED = "restricted"   # Encrypted + Diode Logged

class KnowledgeDomain(str, Enum):
    """Ontology for the Tutor/Mastery modules."""
    GENERAL = "general"
    FINANCE = "finance"
    PHYSICS_QFT = "physics_qft"
    QUANTUM_COMP = "quantum_comp"
    NEUROSCIENCE = "neuroscience"
    SYSTEMS = "systems"

# ==========================================
# 2. HOMEOSTATIC STATE (The Soul)
# ==========================================

class LatentStateContext(BaseModel):
    """
    Snapshot of the agent's internal homeostatic state at memory creation.
    Enables state-dependent retrieval (e.g., retrieving memories formed under high dissonance).
    """
    # 8-dim vector (Plutchik space) representing internal affect
    affect_vector: List[float] = Field(..., min_length=8, max_length=8)
    
    # 0.0 (Stable) -> 1.0 (Critical). The driver of active inquiry/curiosity.
    dissonance_score: float = Field(..., ge=0.0, le=1.0)
    
    # The exploration temperature parameter used during this event
    exploration_rate: float = Field(..., ge=0.0, le=2.0)

# ==========================================
# 3. CAUSAL TOPOLOGY (The Logic)
# ==========================================

class EdgeRelation(str, Enum):
    """Defines the causal or logical nature of the link."""
    CAUSES = "causes"           # A -> B (Temporal/Logical)
    CONTRADICTS = "contradicts" # A != B (Triggers Dissonance)
    REINFORCES = "reinforces"   # A supports B (Increases Confidence)
    RESOLVES = "resolves"       # A answers Question B
    MENTIONS = "mentions"       # Loose association

class CausalEdge(BaseModel):
    """Directed, typed edge for the causal graph."""
    target_id: uuid.UUID
    relation: EdgeRelation
    weight: float = Field(1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==========================================
# 4. EPISTEMIC AUTHORITY (The Committee)
# ==========================================

class ModelContributor(BaseModel):
    """Agent participation in consensus building."""
    model: str = Field(..., json_schema_extra={"example": "DeepSeek-R1-Full"})
    role: Literal["proposer", "critic", "synthesizer", "human_oracle"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    contribution_hash: str = Field(..., min_length=64, max_length=64)

class ConsensusProvenance(BaseModel):
    """
    Cryptographic audit trail for truth establishment.
    Prevents hallucination cascades in rigorous domains (Math/Physics).
    """
    method: Literal["unanimous", "majority_vote", "human_override"]
    contributors: List[ModelContributor] = Field(..., min_length=1)
    consensus_score: float = Field(..., ge=0.0, le=1.0, description="0.0=Contested, 1.0=Axiom")
    dissent_notes: Optional[str] = None
    established_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @computed_field
    @property
    def integrity_hash(self) -> str:
        """Immutable hash of the consensus event."""
        payload = f"{self.method}{self.consensus_score}{''.join(c.contribution_hash for c in self.contributors)}"
        return hashlib.sha3_256(payload.encode()).hexdigest()

# ==========================================
# 5. DATA GRAVITY & ARTIFACTS
# ==========================================

class FileType(str, Enum):
    PDF = "pdf"
    JUPYTER = "jupyter"
    SIM_LOG = "sim_log"
    CODEBASE = "codebase"
    DATASET = "dataset"

class ArtifactPointer(BaseModel):
    """Pointer to external storage objects, keeping the Vector Index lean."""
    tier: StorageTier
    path: str = Field(..., pattern=r"^/mnt/[a-zA-Z0-9_\-/]+\.\w+$")
    file_type: FileType
    checksum: str = Field(..., min_length=64, max_length=64)
    size_mb: float = Field(..., gt=0)

# ==========================================
# 6. THE SYMBIOTE NODE (MemoryNode v5)
# ==========================================

class NodeType(str, Enum):
    EPISODIC = "episodic"   # Interaction logs
    CONCEPT = "concept"     # Synthesized knowledge
    PROOF = "proof"         # Rigorous derivation
    ARTIFACT = "artifact"   # File pointer
    QUESTION = "question"   # Active curiosity driver

class MasteryState(BaseModel):
    """User proficiency tracking for adaptive tutoring."""
    domain: KnowledgeDomain
    user_proficiency: float = Field(0.0, ge=0.0, le=1.0)
    last_verified: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
   
class IdentityBinding(BaseModel):
    """
    Biological Plasticity.
    Governs how tightly this memory is bound to the agent's identity.
    """
    weight: float = Field(0.0, ge=0.0, le=1.0, description="0.0=Ephemeral, 1.0=Core Belief")
    drift_pressure: float = Field(0.0, ge=0.0, description="Accumulated evidence contradicting this node")
    is_protected: bool = Field(False, description="Immunity to garbage collection")

class MemoryUtility(BaseModel):
    """
    Metabolic Metrics.
    Used by the 'Dream Cycle' to prune (forget) or compress memories.
    """
    access_count: int = 0
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    predictive_value: float = Field(0.0, description="Reward signal: Did this help predict user intent?")
    redundancy_score: float = Field(0.0, description="Cluster density overlap (for compression)")

class RecallDynamics(BaseModel):
    """
    Entropy & Distortion.
    Tracks how the narrative changes each time it is remembered (re-consolidation).
    """
    recall_count: int = 0
    distortion_score: float = Field(0.0, description="Semantic drift from original event")
    last_reinforced: Optional[datetime] = None
    
class MemoryNode(BaseModel):
    """
    Atomic unit of the Edubba Protocol v5.
    Combines Biological Fidelity with Epistemic Rigor.
    """
    # --- Identity & Taxonomy ---
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    type: NodeType
    domains: List[KnowledgeDomain] = Field(..., min_length=1)
    
    # --- Infrastructure Mapping ---
    storage_tier: StorageTier = StorageTier.T1_HOT_NVME
    classification: DataClassification = DataClassification.INTERNAL
    
    # --- Content ---
    content_summary: str = Field(..., min_length=10)
    artifact: Optional[ArtifactPointer] = None
    
    # --- Vector Representation ---
    embedding: List[float] = Field(...)
    embedding_model: str = "bge-m3-v1.5"
    embedding_version: str = "1.0"
    
    # --- The Soul (Latent State) ---
    latent_context: Optional[LatentStateContext] = None
    
    # --- Biological Dynamics (RESTORED) ---
    identity: IdentityBinding = Field(default_factory=IdentityBinding)
    utility: MemoryUtility = Field(default_factory=MemoryUtility)
    recall: RecallDynamics = Field(default_factory=RecallDynamics)

    # --- Epistemic Rigor (The Truth) ---
    provenance: ConsensusProvenance
    mastery: Optional[MasteryState] = None
    
    # --- Causal Graph (The Logic) ---
    edges: List[CausalEdge] = Field(default_factory=list)
    
    # --- Future Proofing ---
    neuromorphic_signature: Optional[str] = Field(None)

    # --- Metadata ---
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # --- Validators ---
    @model_validator(mode='after')
    def validate_embedding_dimensions(self) -> 'MemoryNode':
        """
        Validates embedding dimensions based on the model.
        Supports future extensibility for other models (e.g., text-embedding-3-large).
        """
        # Define expected dimensions for supported models
        MODEL_DIMENSIONS = {
            "bge-m3-v1.5": 1024,
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            # Add future models here
        }
        
        expected_dim = MODEL_DIMENSIONS.get(self.embedding_model)
        
        # If model is known, enforce exact dimension
        if expected_dim and len(self.embedding) != expected_dim:
            raise ValueError(
                f"Embedding dimension mismatch for model '{self.embedding_model}'. "
                f"Expected {expected_dim}, got {len(self.embedding)}."
            )
        
        # If model is unknown, ensure at least some minimum sanity check
        # This allows for custom models without crashing, but flags potentially empty vectors
        if not expected_dim and len(self.embedding) < 8:
             raise ValueError(f"Embedding length {len(self.embedding)} is too short for a valid vector.")

        return self

    @model_validator(mode='after')
    def validate_restricted_access(self) -> 'MemoryNode':
        if self.classification == DataClassification.RESTRICTED and not self.artifact:
            raise ValueError("RESTRICTED classification requires artifact pointer.")
        return self

    @computed_field
    @property
    def diode_packet(self) -> Optional[str]:
        if self.classification == DataClassification.RESTRICTED:
            dissonance = self.latent_context.dissonance_score if self.latent_context else 0.0
            return (
                f"SHA:{self.provenance.integrity_hash}|"
                f"ID:{self.id}|"
                f"DOM:{','.join(self.domains)}|"
                f"DISS:{dissonance:.2f}"
            )
        return None