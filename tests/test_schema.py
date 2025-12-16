import pytest
import uuid
from src.schema import (
    MemoryNode, NodeType, KnowledgeDomain, StorageTier, DataClassification,
    ConsensusProvenance, ModelContributor, LatentStateContext, 
    ArtifactPointer, FileType, IdentityBinding, MemoryUtility, RecallDynamics,
    CausalEdge, EdgeRelation
)

# --- FIXTURES (Standardized Test Data) ---

@pytest.fixture
def valid_embedding():
    """Generates a mock 1024-dim vector for BGE-M3."""
    return [0.05] * 1024

@pytest.fixture
def valid_provenance():
    """Creates a valid consensus object."""
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
def valid_latent_context():
    """Creates a snapshot of internal homeostatic state."""
    return LatentStateContext(
        affect_vector=[0.1] * 8,
        dissonance_score=0.2,
        exploration_rate=0.5
    )

# --- TEST CASES ---

def test_symbiote_biology(valid_embedding, valid_provenance, valid_latent_context):
    """
    Verifies that the v5.0 node correctly initializes all biological and logical organs.
    This proves the system is 'alive' (State + Identity + Logic) and not just a database.
    """
    node = MemoryNode(
        type=NodeType.CONCEPT,
        domains=[KnowledgeDomain.SYSTEMS],
        content_summary="Symbiote Initialization Test",
        embedding=valid_embedding,
        provenance=valid_provenance,
        latent_context=valid_latent_context,
        # Explicitly setting biological dynamics to test plasticity
        identity=IdentityBinding(weight=0.9, is_protected=True),
        utility=MemoryUtility(predictive_value=0.8),
        recall=RecallDynamics(recall_count=1)
    )

    # 1. Check Biological Fidelity
    assert node.identity.weight == 0.9
    assert node.identity.is_protected is True
    assert node.utility.predictive_value == 0.8
    
    # 2. Check Logic Graph (Verifies Causal Reasoning is enabled)
    edge = CausalEdge(
        target_id=uuid.uuid4(), 
        relation=EdgeRelation.CAUSES,
        weight=0.95
    )
    node.edges.append(edge)
    assert len(node.edges) == 1
    assert node.edges[0].relation == EdgeRelation.CAUSES
    assert node.edges[0].weight == 0.95

def test_security_validator_happy_path(valid_embedding, valid_provenance):
    """
    Ensures RESTRICTED data is allowed IF a physical artifact is present.
    """
    artifact = ArtifactPointer(
        tier=StorageTier.T4_DEEP_ARCHIVE,
        path="/mnt/secure/log.pdf",
        file_type=FileType.PDF,
        checksum="b" * 64,
        size_mb=10.0
    )
    
    node = MemoryNode(
        type=NodeType.ARTIFACT,
        domains=[KnowledgeDomain.FINANCE],
        content_summary="Secure Ledger",
        embedding=valid_embedding,
        provenance=valid_provenance,
        classification=DataClassification.RESTRICTED,
        artifact=artifact
    )
    
    assert node.classification == DataClassification.RESTRICTED
    assert node.diode_packet is not None
    assert "SHA:" in node.diode_packet

def test_security_validator_failure(valid_embedding, valid_provenance):
    """
    Ensures the system REJECTS restricted data if no artifact pointer exists.
    This verifies the Air-Gap logic works.
    """
    with pytest.raises(ValueError, match="RESTRICTED classification requires artifact pointer"):
        MemoryNode(
            type=NodeType.EPISODIC,
            domains=[KnowledgeDomain.GENERAL],
            content_summary="Leak Attempt",
            embedding=valid_embedding,
            provenance=valid_provenance,
            classification=DataClassification.RESTRICTED,
            artifact=None # Missing Artifact -> Must Fail
        )

def test_audit_logging_psychometrics(valid_embedding, valid_provenance, valid_latent_context):
    """
    Verifies that the Optical Diode packet correctly captures the internal state (Dissonance).
    This is the critical 'Psychological Forensics' feature.
    """
    node = MemoryNode(
        type=NodeType.PROOF,
        domains=[KnowledgeDomain.PHYSICS_QFT],
        content_summary="Restricted Derivation",
        embedding=valid_embedding,
        provenance=valid_provenance,
        latent_context=valid_latent_context, # Dissonance = 0.2
        classification=DataClassification.RESTRICTED,
        artifact=ArtifactPointer(
            tier=StorageTier.T4_DEEP_ARCHIVE,
            path="/mnt/qft/proof.pdf",
            file_type=FileType.PDF,
            checksum="c" * 64,
            size_mb=5.0
        )
    )
    
    # The audit log must capture the psychological state (Dissonance)
    packet = node.diode_packet
    
    assert "DISS:0.20" in packet
    assert f"ID:{node.id}" in packet
    assert "SHA:" in packet