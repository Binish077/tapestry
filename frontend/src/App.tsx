import { useEffect, useState } from "react";
import { fetchTree } from "./lib/treeApi";
import { adaptTreeToFlow } from "./lib/treeGraph";
import type { TreeGraph } from "./lib/treeGraph";
import "./App.css";

type TreeState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "empty" }
  | { status: "success"; graph: TreeGraph };

function App() {
  const [treeState, setTreeState] = useState<TreeState>({ status: "loading" });

  useEffect(() => {
    const controller = new AbortController();

    fetchTree(controller.signal)
      .then((tree) => {
        if (tree.nodes.length === 0) {
          setTreeState({ status: "empty" });
          return;
        }

        setTreeState({ status: "success", graph: adaptTreeToFlow(tree) });
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;

        setTreeState({
          status: "error",
          message:
            error instanceof Error ? error.message : "An unknown error occurred",
        });
      });

    return () => controller.abort();
  }, []);

  return (
    <main className="tree-page">
      <header className="tree-header">
        <p className="wordmark">tapestry</p>
        <p className="motto">History, woven</p>
      </header>
      <section className="tree-content" aria-labelledby="tree-title">
        <div className="section-heading">
          <p className="eyebrow">House Targaryen</p>
          <h1 id="tree-title">Lineage</h1>
        </div>
        {treeState.status === "loading" && (
          <p className="tree-message" role="status">Loading family records…</p>
        )}
        {treeState.status === "error" && (
          <p className="tree-message tree-error" role="alert">
            Could not load family records: {treeState.message}
          </p>
        )}
        {treeState.status === "empty" && (
          <p className="tree-message" role="status">
            No family records are available yet.
          </p>
        )}
        {treeState.status === "success" && (
          <div className="tree-message tree-summary" role="status">
            <strong>Family records loaded</strong>
            <span>
              {treeState.graph.nodes.length} people · {treeState.graph.edges.length} relationships
            </span>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;