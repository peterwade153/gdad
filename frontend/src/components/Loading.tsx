import React from 'react';

export const FamilyTreeLoading: React.FC = () => {
    return (
        <div className="flex h-screen w-screen flex-col items-center justify-center gap-3 bg-slate-50">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600" />
            <p className="text-sm font-medium text-slate-500">Loading lineage chart...</p>
        </div>
    );
};
