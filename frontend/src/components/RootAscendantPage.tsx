import React, { useState, useEffect } from 'react';
import type { RootAscendantPayload } from '../types';
import { FamilyTreeGraph } from './FamilyTree';
import { FamilyTreeError } from './NetworkError';
import { FamilyTreeForm } from './forms/FamilyTreeSearchForm';
import { FamilyTreeLoading } from './Loading';
import { TreePlaceholder } from './Placeholder';

const API_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export const RootAscendantPage: React.FC = () => {
    const [identityNumber, setIdentityNumber] = useState("");
    // Network & Data States
    const [data, setData] = useState<RootAscendantPayload | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!identityNumber) {
            setData(null);
            return;
        }
        const fetchFamilyTree = async () => {
            setData(null);
            setLoading(true);
            setError(null);
            try {
                const response = await fetch(`${API_URL}/root-ascendant/${identityNumber}/`);
                if (!response.ok) {
                    throw new Error('Failed to fetch family tree data.');
                }
                const payload: RootAscendantPayload = await response.json();
                setData(payload);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An unknown error occurred');
            } finally {
                setLoading(false);
            }
        };
        fetchFamilyTree();
    }, [identityNumber]);

    const handleFormSubmit = (value: string) => {
        setIdentityNumber(value.trim());
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
                ) : data?.root_ascendants?.length ? (
                    <div className="w-full h-full rounded-xl border border-slate-200 overflow-hidden relative bg-slate-50">
                        <FamilyTreeGraph apiData={data.root_ascendants} />
                    </div>
                ) : data ? (
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
                ) : (
                    <TreePlaceholder 
                        icon="🌳"
                        iconBgColor="bg-emerald-50"
                        iconTextColor="text-emerald-600"
                        title="Discover Your Root Ascendant"
                        description={
                            <p>
                                Please enter your Identity Number in the search bar above to generate and view the ultimate ancestor.
                            </p>
                        }
                    />
                )}
            </div>
        </div>
    )
};
