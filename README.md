# Edubba Protocol: Cognitive Memory Schema v5

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active_Research-success)]()

**A Distributed, Tiered-Memory Architecture for Cognitive Agents.**

The Edubba Protocol is a memory schema designed for **long-horizon, self-hosting agents**. Unlike standard RAG systems that treat memory as flat, static text chunks, this protocol models memory as a **Tiered, Epistemic Graph** with homeostatic properties.

It is explicitly engineered for local-first systems that require **Data Gravity** (mapping memory to physical storage tiers) and **Epistemic Provenance** (preventing hallucination cascades via multi-model consensus).

---

## Core Architecture

### 1. Physical Substrate Layer (`StorageTier`)
The schema enforces "Data Gravity" by mapping memory nodes to specific physical hardware based on access frequency and security requirements:
*   **T0 (Hot RAM):** Causal Graph (NetworkX) for millisecond reasoning.
*   **T1 (Hot NVMe):** Active Vector Index (Qdrant/Milvus).
*   **T2 (Warm Pool):** ZFS Arrays for active project context.
*   **T3/T4 (Cold Archive):** Immutable audit logs and raw interaction history.

### 2. Latent State Context (`LatentStateContext`)
Captures the agent's internal homeostatic state at the moment of memory formation to enable **State-Dependent Retrieval**:
*   **Affect Vector:** 8-dimensional embedding (Plutchik model).
*   **Dissonance Score:** Measures the urge to resolve internal contradictions.
*   **Exploration Rate:** Tracks behavioral volatility during encoding.

### 3. Ensemble Consensus Verification (`ConsensusProvenance`)
Truth is not assumed; it is verified. Each memory node includes a cryptographic audit trail of its establishment:
*   **Contributors:** Logs the specific models (e.g., DeepSeek-R1, Llama-3) involved.
*   **Roles:** Distinguishes between `proposer`, `critic`, `synthesizer`, and `human_oracle`.
*   **Integrity:** A SHA-256 hash ensures the consensus event is immutable.

### 4. Hardware-Enforced Audit (`DataClassification`)
Memories marked `RESTRICTED` trigger a specialized `diode_packet` computed field. This packet is formatted for transmission across unidirectional serial hardware (**Optical Data Diodes**), ensuring an immutable audit trail even if the primary index is compromised.

---

## Usage Example

```python
from src.schema import MemoryNode, NodeType, KnowledgeDomain, ConsensusProvenance

# Instantiate a Verified Memory Node
node = MemoryNode(
    type=NodeType.CONCEPT,
    domains=[KnowledgeDomain.QUANTUM_COMP],
    content_summary="Decoherence scaling in superconducting qubits",
    embedding=[0.05] * 1024,  # BGE-M3 Vector
    
    # Cryptographic Proof of Consensus
    provenance=ConsensusProvenance(
        method="majority_vote",
        contributors=[...], 
        consensus_score=0.92
    ),
    
    # Internal Homeostatic State (The Ghost)
    latent_context={
        "affect_vector": [0.1, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1],
        "dissonance_score": 0.05,
        "exploration_rate": 0.4
    }
)

print(f"Node ID: {node.id}")
print(f"Audit Hash: {node.provenance.integrity_hash}")
```
---

## Terminology Mapping
The Edubba Protocol uses academic terminology to describe components that may correspond to internal cognitive modules in other agentic frameworks.
| Protocol Term           | Functional Definition                | Internal Alias (Legacy) |
| ----------------------- | ------------------------------------ | ----------------------- |
| Tiered Storage Topology | Physical mapping of data to hardware | The Body                |
| Latent State Context    | Snapshot of homeostatic parameters   | The Soul / Ghost        |
| Ensemble Consensus      | Multi-model truth verification       | The Committee           |
| Primary Orchestrator    | The central executive agent          | Ereshkigal              |
| HEAL                    | Hardware-Enforced Audit Log          | Optical Diode           |
| HITL Co-Learning        | Human-in-the-Loop recursive learning | Symbiosis               |
| Dissonance Metric       | Drive to resolve contradiction       | Tension                 |
| CausalEdge              | Typed, directed graph relationship   | Memory Edge             |

---

## Status
This system is functional and actively maintained. It is built atop a bespoke hardware topology (AMD EPYC / Dual-GPU / ZFS) optimized specifically for this architecture. While contributions are welcome, please note that the underlying design assumes a distributed, multi-model runtime environment.

---

## License
MIT License — see LICENSE for details.
