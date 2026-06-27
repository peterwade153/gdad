import React from 'react';
import type { TreePlaceholderProps } from '../types';

export const TreePlaceholder: React.FC<TreePlaceholderProps> = ({ 
    icon, 
    iconBgColor, 
    iconTextColor, 
    title, 
    description 
}) => (
    <div className="flex flex-col items-center justify-center h-full w-full p-8 text-center bg-slate-50">
        <div className="max-w-md bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
            <div className={`mx-auto flex h-14 w-14 items-center justify-center rounded-full ${iconBgColor} ${iconTextColor} mb-5 text-2xl`}>
                {icon}
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-3 tracking-tight">
                {title}
            </h2>
            <div className="text-sm text-slate-600 font-medium leading-relaxed px-2">
                {description}
            </div>
        </div>
    </div>
);
