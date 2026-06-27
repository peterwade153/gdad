import React from 'react';

interface FamilyTreeErrorProps {
    message: string;
    onRetry?: () => void;
}

export const FamilyTreeError: React.FC<FamilyTreeErrorProps> = ({ 
    message, 
    onRetry = () => window.location.reload() 
}) => {
    return (
        <div className="flex h-screen w-screen items-center justify-center bg-slate-50 p-4">
            <div className="w-full max-w-md rounded-xl border border-red-100 bg-white p-6 shadow-md">
                <h3 className="text-lg font-semibold text-red-600">Network Error</h3>
                <p className="mt-2 text-sm text-slate-600">{message}</p>
                <button 
                    onClick={onRetry} 
                    className="mt-4 rounded-lg bg-red-50 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-100"
                >
                    Retry Connection
                </button>
            </div>
        </div>
    );
};
