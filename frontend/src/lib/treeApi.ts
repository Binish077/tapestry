import type { TreeResponse } from "../types/tree";

export async function fetchTree(signal?: AbortSignal): Promise<TreeResponse> {
  const response = await fetch("/api/tree", { signal });

  if (!response.ok) {
    throw new Error(`Tree request failed (${response.status})`);
  }

  return (await response.json()) as TreeResponse;
}