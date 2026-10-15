import type {
  PersonFlowNode,
  RelationshipFlowEdge,
  TreeResponse,
} from "../types/tree";

export interface TreeGraph {
  nodes: PersonFlowNode[];
  edges: RelationshipFlowEdge[];
}

export function adaptTreeToFlow(tree: TreeResponse): TreeGraph {
  return {
    nodes: tree.nodes.map((person) => ({
      id: String(person.id),
      type: "person",
      position: { x: 0, y: 0 },
      data: { person },
    })),
    edges: tree.edges.map((relationship) => ({
      id: `relationship-${relationship.id}`,
      source: String(relationship.source_id),
      target: String(relationship.target_id),
      type: "smoothstep",
      data: { relationship },
    })),
  };
}