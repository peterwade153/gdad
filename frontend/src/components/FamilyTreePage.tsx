import React, { useState, useEffect } from 'react';
import type { Payload } from '../types';
import { FamilyTreeGraph } from './FamilyTree';
import { FamilyTreeError } from './NetworkError';
import { FamilyTreeForm } from './forms/FamilyTreeSearchForm';
import { FamilyTreeLoading } from './Loading';
import { TreePlaceholder } from './Placeholder';

const API_URL = import.meta.env.VITE_API_BASE_URL ?? "";

const getInitialIdentityNumber = (): string | undefined => {
    if (typeof window === 'undefined') return undefined;
    const params = new URLSearchParams(window.location.search);
    return params.get('identity-number')?.trim() || undefined;
};

export const FamilyTreePage: React.FC = () => {
    const [identityNumber, setIdentityNumber] = useState<string | undefined>(() => getInitialIdentityNumber());
    const [maxGeneration, setMaxGeneration] = useState<number>(10);
    // Network & Data States
    const [data, setData] = useState<Payload | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchFamilyTree = async () => {
            setLoading(true);
            setError(null);
            try {
                const queryParams = new URLSearchParams({
                    'max-generation': maxGeneration.toString()
                });
                if (identityNumber) {
                    queryParams.append('identity-number', identityNumber);
                }

                const response = await fetch(`${API_URL}/family-tree/lineage/?${queryParams.toString()}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch family tree data.');
                }
                const payload: Payload = await response.json();
                setData(payload);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An unknown error occurred');
            } finally {
                setLoading(false);
            }
        };
    
        fetchFamilyTree();
    }, [identityNumber, maxGeneration]);

    const handleFormSubmit = (value: string) => {
        setIdentityNumber(value);
    };

    return (
        <div className="flex h-screen w-screen flex-col bg-slate-50 overflow-hidden">
            <div className="flex border-b border-slate-200 bg-white px-6 py-4 shadow-sm z-10 justify-center items-center shrink-0">
                <FamilyTreeForm 
                    initialValue={identityNumber} 
                    onSubmit={handleFormSubmit} 
                />
            </div>
            {/* Main Content Area */}
            <div className="flex-1 relative w-full overflow-hidden min-h-0">
                {loading ? (
                    <FamilyTreeLoading />
                ) : error ? (
                    <FamilyTreeError message={error} onRetry={()=> {setLoading(true);}} />
                ) : data?.people?.length ? (
                    <div className="w-full h-full rounded-xl border border-slate-200 overflow-hidden relative bg-slate-50">
                        <FamilyTreeGraph apiData={data.people} />
                    </div>
                ) : (
                    <TreePlaceholder 
                        icon="🔍"
                        iconBgColor="bg-amber-50"
                        iconTextColor="text-amber-600"
                        title="No Family Tree Found"
                        description={
                            <p>
                                We couldn't find any root ascendant record/s associated with Identity Number
                                <span className="font-semibold text-slate-800">"{identityNumber}"</span>.
                                Please verify the number and try again.
                            </p>
                        }
                    />
                )}
                {/* Pagination */}
                <div className="absolute bottom-15 w-full border-t border-slate-200 p-3 justify-center items-center flex z-20 pointer-events-none">
                    {(() => {
                        const hasGenerationsCount = typeof data?.generations === 'number';
                        const hasReachedEnd = hasGenerationsCount && data?.generations < maxGeneration;
                        return (
                            <button
                                type="button"
                                disabled={hasReachedEnd}
                                onClick={() => setMaxGeneration((prev) => prev + 10)}
                                className={`max-w-xs rounded-lg px-5 py-2 text-sm font-bold shadow-md transition-all pointer-events-auto
                                    ${hasReachedEnd 
                                        ? 'bg-slate-200 text-slate-400 cursor-not-allowed shadow-none border border-slate-300' 
                                        : 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800'
                                    }`}
                            >
                                {hasReachedEnd 
                                    ? `All Generations Loaded (${data?.generations})` 
                                    : `More... (Showing ${maxGeneration} gens)`
                                }
                            </button>
                        );
                    })()}
                </div>
            </div>
        </div>
    );
};
