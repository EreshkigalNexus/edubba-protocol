import pytest
import uuid
from datetime import datetime
from src.schema import (
    MemoryNode, NodeType, KnowledgeDomain, StorageTier, DataClassification,
    ConsensusProvenance, ModelContributor, LatentStateContext, 
    ArtifactPointer, FileType, MasteryState, EdgeRelation, CausalEdge
)

# --- FIXTURES ---

@pytest.fixture
def base_provenance():
    return ConsensusProvenance(
        method="unanimous",
        contributors=[
            ModelContributor(
                model="DeepSeek-R1-Full",
                role="proposer",
                confidence=0.99,
                contribution_hash="a" * 64
            )
        ],
        consensus_score=0.99
    )

@pytest.fixture
def base_embedding():
    return [0.05] * 1024

@pytest.fixture
def base_latent_context():
    return LatentStateContext(
        affect_vector=[0.1] * 8,
        dissonance_score=0.1,
        exploration_rate=0.5
    )

# --- LIFECYCLE SCENARIOS ---

def test_lifecycle_mastery_update(base_embedding, base_provenance):
    """
    Scenario:
    1. Agent learns a new concept (Node Created).
    2. Agent demonstrates proficiency (Mastery Updated).
    3. Retrieval filters based on mastery.
    """
    # 1. Creation
    node = MemoryNode(
        type=NodeType.CONCEPT,
        domains=[KnowledgeDomain.QUANTUM_COMP],
        content_summary="Shor's Algorithm Basics",
        embedding=base_embedding,
        provenance=base_provenance,
    )
    assert node.mastery is None
    
    # 2. Mastery Update
    # Simulating an update - in a real app this would likely be a database update, 
    # but here we update the object state.
    new_mastery = MasteryState(
        domain=KnowledgeDomain.QUANTUM_COMP,
        user_proficiency=0.85
    )
    node.mastery = new_mastery
    
    assert node.mastery.user_proficiency == 0.85
    assert node.mastery.domain == KnowledgeDomain.QUANTUM_COMP
    
    # 3. Simulated Retrieval Filter
    # Query: Find concepts where proficiency > 0.8
    assert node.mastery.user_proficiency > 0.8

def test_lifecycle_dissonance_retrieval(base_embedding, base_provenance, base_latent_context):
    """
    Scenario:
    1. Create memories with different dissonance scores.
    2. Simulate retrieval of 'high conflict' memories.
    """
    # High Dissonance Node
    high_diss_context = base_latent_context.model_copy()
    high_diss_context.dissonance_score = 0.9
    
    node_high = MemoryNode(
        type=NodeType.EPISODIC,
        domains=[KnowledgeDomain.GENERAL],
        content_summary="Conflicting Evidence",
        embedding=base_embedding,
        provenance=base_provenance,
        latent_context=high_diss_context
    )
    
    # Low Dissonance Node
    low_diss_context = base_latent_context.model_copy()
    low_diss_context.dissonance_score = 0.1
    
    node_low = MemoryNode(
        type=NodeType.EPISODIC,
        domains=[KnowledgeDomain.GENERAL],
        content_summary="Routine Confirmation",
        embedding=base_embedding,
        provenance=base_provenance,
        latent_context=low_diss_context
    )
    
    memory_bank = [node_high, node_low]
    
    # Retrieval: Get memories where dissonance > 0.5
    high_conflict_memories = [
        m for m in memory_bank 
        if m.latent_context and m.latent_context.dissonance_score > 0.5
    ]
    
    assert len(high_conflict_memories) == 1
    assert high_conflict_memories[0].id == node_high.id

def test_lifecycle_security_escalation(base_embedding, base_provenance, base_latent_context):
    """
    Scenario:
    1. Memory starts as INTERNAL.
    2. Logic determines it must be RESTRICTED.
    3. Update fails without artifact.
    4. Artifact added, update succeeds.
    5. Audit log (diode packet) is generated.
    """
    node = MemoryNode(
        type=NodeType.PROOF,
        domains=[KnowledgeDomain.FINANCE],
        content_summary="Market Analysis",
        embedding=base_embedding,
        provenance=base_provenance,
        latent_context=base_latent_context,
        classification=DataClassification.INTERNAL
    )
    
    assert node.diode_packet is None
    
    # Attempt to escalate to RESTRICTED without artifact
    # Note: modifying the field directly won't trigger validation in standard python assignment 
    # unless we re-validate. In Pydantic v2, we can validate assignment if configured, 
    # but MemoryNode doesn't have validate_assignment=True config visible.
    # However, for the purpose of the test, we can check if `MemoryNode(**node.model_dump())` fails
    # or if we manually invoke validation.
    
    # Let's simulate the update by creating a new version of the node (common in immutable patterns)
    node_data = node.model_dump()
    node_data['classification'] = DataClassification.RESTRICTED
    
    with pytest.raises(ValueError, match="RESTRICTED classification requires artifact pointer"):
        MemoryNode(**node_data)
        
    # Now add artifact
    artifact = ArtifactPointer(
        tier=StorageTier.T4_DEEP_ARCHIVE,
        path="/mnt/finance/audit.pdf",
        file_type=FileType.PDF,
        checksum="f" * 64,
        size_mb=1.2
    )
    node_data['artifact'] = artifact
    
    # Should pass now
    secure_node = MemoryNode(**node_data)
    
    assert secure_node.classification == DataClassification.RESTRICTED
    assert secure_node.diode_packet is not None
    assert "DISS:0.10" in secure_node.diode_packet

def test_embedding_model_validation():
    """
    Verifies the dynamic embedding validation logic.
    """
    prov = ConsensusProvenance(
        method="unanimous",
        contributors=[ModelContributor(model="x", role="proposer", confidence=1, contribution_hash="a"*64)],
        consensus_score=1
    )
    
    # 1. Correct BGE-M3 (1024)
    MemoryNode(
        type=NodeType.CONCEPT,
        domains=[KnowledgeDomain.GENERAL],
        content_summary="test content summary",
        embedding=[0.1]*1024,
        embedding_model="bge-m3-v1.5",
        provenance=prov
    )
    
    # 2. Incorrect BGE-M3
    with pytest.raises(ValueError, match="Expected 1024, got 10"):
        MemoryNode(
            type=NodeType.CONCEPT,
            domains=[KnowledgeDomain.GENERAL],
            content_summary="test content summary",
            embedding=[0.1]*10,
            embedding_model="bge-m3-v1.5",
            provenance=prov
        )
        
    # 3. Correct OpenAI Small (1536)
    MemoryNode(
        type=NodeType.CONCEPT,
        domains=[KnowledgeDomain.GENERAL],
        content_summary="test content summary",
        embedding=[0.1]*1536,
        embedding_model="text-embedding-3-small",
        provenance=prov
    )
    
    # 4. Unknown Model (sanity check > 8)
    MemoryNode(
        type=NodeType.CONCEPT,
        domains=[KnowledgeDomain.GENERAL],
        content_summary="test content summary",
        embedding=[0.1]*128,
        embedding_model="custom-finetune-v1",
        provenance=prov
    )
    
    # 5. Unknown Model too short
    with pytest.raises(ValueError, match="too short"):
        MemoryNode(
            type=NodeType.CONCEPT,
            domains=[KnowledgeDomain.GENERAL],
            content_summary="test content summary",
            embedding=[0.1]*4,
            embedding_model="custom-finetune-v1",
            provenance=prov
        )

