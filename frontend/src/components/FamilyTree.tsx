import React, { useEffect } from 'react';
import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  BackgroundVariant,
  type Node,
  type Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import type { PersonPayload } from '../types';
import { getLayoutedElements } from '../layoutUtils';
import { PersonNode } from './PersonNode';

interface FamilyTreeGraphProps {
   apiData: PersonPayload[];
}

const nodeTypes = {
   customPerson: PersonNode,
};

export const FamilyTreeGraph: React.FC<FamilyTreeGraphProps> = ({ apiData }) => {
    const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

    // Sync state whenever apiData updates
    useEffect(() => {
        if (!apiData || apiData.length === 0) return;
        
        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(apiData, 'TB');
        
        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
    }, [apiData, setNodes, setEdges]);

    return (
        <div className="flex w-full h-4/5">
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                nodeTypes={nodeTypes}
                fitView={true}
                minZoom={0.2}
                maxZoom={1.5}
            >
            <Controls className="bg-white border border-slate-200 rounded-lg shadow-sm" />
            <Background variant={BackgroundVariant.Dots} gap={16} size={1} color="#cbd5e1" />
        </ReactFlow>
        </div>
    );
};
