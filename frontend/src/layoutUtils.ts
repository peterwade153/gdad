import type { Node, Edge } from '@xyflow/react';
import dagre from '@dagrejs/dagre';
import type { PersonPayload } from './types';

const NODE_WIDTH = 220;
const NODE_HEIGHT = 80;

/**
* Transforms flat API data and computes a directed layout using Dagre
*/
export const getLayoutedElements = (
    apiData: PersonPayload[],
    direction: 'TB' | 'LR' = 'TB'
): { nodes: Node[]; edges: Edge[] } => {
    const nodes: Node[] = [];
    const edges: Edge[] = [];
    const existingIds = new Set(apiData.map((p) => p.identity_number));

    // 1. Map API data to standard React Flow elements
    apiData.forEach((person) => {
    const nodeId = person.identity_number;

    // FIX: Using .push() instead of .append()
    nodes.push({
        id: nodeId,
        type: 'customPerson', 
        data: { 
            label: `${person.name} ${person.surname}`,
            birthDate: person.birth_date,
            generation: person.generation,
            identityNumber: person.identity_number,
        },
        position: { x: 0, y: 0 },
    });

    if (person.father_id && existingIds.has(person.father_id)) {
        edges.push({
            id: `e-${person.father_id}-${nodeId}`,
            source: person.father_id,
            target: nodeId,
            className: '!stroke-slate-400 !stroke-2', 
            animated: true,
        });
    }

    if (person.mother_id && existingIds.has(person.mother_id)) {
        edges.push({
            id: `e-${person.mother_id}-${nodeId}`,
            source: person.mother_id,
            target: nodeId,
            className: '!stroke-slate-400 !stroke-2',
            animated: true,
        });
    }
    });

    // 2. Initialize and configure Dagre
    const dagreGraph = new dagre.graphlib.Graph();
    dagreGraph.setDefaultEdgeLabel(() => ({}));
    dagreGraph.setGraph({ rankdir: direction, ranksep: 80, nodesep: 60 });

    nodes.forEach((node) => {
        dagreGraph.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
    });

    edges.forEach((edge) => {
        dagreGraph.setEdge(edge.source, edge.target);
    });

    // 3. Compute layout positions
    dagre.layout(dagreGraph);

    // 4. Assign layout positions back to React Flow nodes
    const layoutedNodes = nodes.map((node) => {
        const nodeWithPosition = dagreGraph.node(node.id);
        return {
            ...node,
            position: {
                x: nodeWithPosition.x - NODE_WIDTH / 2,
                y: nodeWithPosition.y - NODE_HEIGHT / 2,
            },
        };
    });

    return { nodes: layoutedNodes, edges: edges };
};
