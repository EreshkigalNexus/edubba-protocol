# demo.py - Edubba Protocol v5 Reference Implementation
import uuid
from src.schema import (
    MemoryNode, NodeType, KnowledgeDomain, StorageTier, DataClassification,
    ConsensusProvenance, ModelContributor, LatentStateContext, CausalEdge, EdgeRelation
)

def main():
    print("--- Edubba Protocol v5: Symbiote Node Initialization ---")

    # 1. ESTABLISH PROVENANCE (The Committee)
    # Simulating a multi-model consensus event
    provenance = ConsensusProvenance(
        method="unanimous",
        contributors=[
            ModelContributor(
                model="DeepSeek-R1-Full", 
                role="proposer", 
                confidence=0.99, 
                contribution_hash="a1b2c3d4" * 8
            ),
            ModelContributor(
                model="Llama-3-70B", 
                role="critic", 
                confidence=0.95, 
                contribution_hash="e5f6g7h8" * 8
            )
        ],
        consensus_score=0.99
    )

    # 2. CAPTURE LATENT STATE (The Ghost)
    # Snapshotting homeostatic state at creation (State-Dependent Retrieval)
    ghost_state = LatentStateContext(
        affect_vector=[0.1, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1], 
        dissonance_score=0.05, # Low tension
        exploration_rate=0.4   # Stable/Exploitative mode
    )

    # 3. CREATE MEMORY NODE (The Engram)
    node = MemoryNode(
        type=NodeType.CONCEPT,
        domains=[KnowledgeDomain.PHYSICS_QFT, KnowledgeDomain.SYSTEMS],
        content_summary="The Symbiote Architecture integrates biological fidelity with epistemic rigor.",
        embedding=[0.05] * 1024, # Placeholder for bge-m3 embedding
        provenance=provenance,
        latent_context=ghost_state,
        classification=DataClassification.INTERNAL
    )

    # 4. LINK CAUSALITY (The Graph)
    node.edges.append(
        CausalEdge(
            target_id=uuid.uuid4(),
            relation=EdgeRelation.REINFORCES,
            weight=0.9
        )
    )

    print(f"✅ Node Created: {node.id}")
    print(f"🧠 Integrity Hash: {node.provenance.integrity_hash}")
    print(f"👻 Dissonance Score: {node.latent_context.dissonance_score}")
    print(f"🔗 Edge Count: {len(node.edges)}")

if __name__ == "__main__":
    main()