import React from 'react';
import { Handle, Position} from '@xyflow/react';
import type { NodeProps, Node } from '@xyflow/react';

type PersonNodeData = {
    label: string;
    birthDate: string | null;
    generation: number;
};

export const PersonNode: React.FC<NodeProps<Node & { data: PersonNodeData }>> = ({ data }) => {
  return (
    <div className="w-[220px] rounded-xl border border-slate-200 bg-white p-3 shadow-md transition-all hover:shadow-lg">
      {/* Top Handle (Target): 
        Using !bg-slate-400 to forcefully override React Flow's default blue handle color
      */}
      <Handle 
        type="target" 
        position={Position.Top} 
        className="!bg-slate-400 !w-2 !h-2 !border-none" 
      />
      
      <div className="flex flex-col gap-1">
        <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
          Gen {data.generation}
        </span>
        <h4 className="truncate font-medium text-slate-800 text-sm">
          {data.label}
        </h4>
        {data.birthDate && (
          <span className="text-xs text-slate-400">
            🎂 {data.birthDate}
          </span>
        )}
      </div>

      <Handle 
        type="source" 
        position={Position.Bottom} 
        className="!bg-slate-400 !w-2 !h-2 !border-none" 
      />
    </div>
  );
};
