import type { Edge, Node } from "@xyflow/react";

export type TreeEdgeType = "parent_child" | "marriage" | "lover" | "sibling";

export type RelationshipType =
  | "child_of"
  | "mother_of"
  | "father_of"
  | "husband_of"
  | "wife_of"
  | "lover_of"
  | "sibling_of";

export interface TreeResource {
  name: string;
  value: string;
}

export interface TreeNode {
  id: number;
  name: string;
  active_from: number | null;
  active_to: number | null;
  resources: TreeResource[];
}

export interface TreeEdge {
  id: number;
  relationship_ids: number[];
  source_id: number;
  target_id: number;
  type: TreeEdgeType;
  relationship_types: RelationshipType[];
  valid_from: number | null;
  valid_to: number | null;
  strength: number;
}

export interface TreeResponse {
  nodes: TreeNode[];
  edges: TreeEdge[];
}

export interface PersonFlowNodeData extends Record<string, unknown> {
  person: TreeNode;
}

export interface RelationshipFlowEdgeData extends Record<string, unknown> {
  relationship: TreeEdge;
}

export type PersonFlowNode = Node<PersonFlowNodeData, "person">;
export type RelationshipFlowEdge = Edge<RelationshipFlowEdgeData>;