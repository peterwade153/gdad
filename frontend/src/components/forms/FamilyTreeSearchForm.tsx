import React, { useState } from 'react';

interface FamilyTreeFormProps {
    initialValue?: string;
    onSubmit: (value: string) => void;
}

export const FamilyTreeForm: React.FC<FamilyTreeFormProps> = ({ initialValue = '', onSubmit }) => {
    const [inputValue, setInputValue] = useState(initialValue);

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (inputValue.trim()) {
            onSubmit(inputValue.trim());
        }
    };

    const isInputEmpty = !inputValue.trim();

    return (
        <form onSubmit={handleSubmit} className="flex items-center gap-3 w-full max-w-2xl justify-center">
            <label 
                className="text-xs font-semibold text-slate-500 uppercase tracking-wider whitespace-nowrap" 
                htmlFor="familytree"
            >
                Identity Number <span className="text-slate-400 font-normal lowercase">(optional):</span>
            </label>
            
            <input
                type="text"
                value={inputValue}
                id="familytree"
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="e.g. GEN2-0003"
                className="flex-1 max-w-sm rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-800 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all placeholder-slate-300 h-[38px]"
            />
            
            <button
                type="submit"
                disabled={isInputEmpty}
                className={`rounded-lg px-5 text-sm font-semibold shadow-sm transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 h-[38px] flex items-center justify-center whitespace-nowrap
                    ${isInputEmpty 
                        ? 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200 shadow-none' 
                        : 'bg-indigo-600 text-white hover:bg-indigo-700 active:bg-indigo-800'
                    }`}
            >
                Search
            </button>
        </form>
    );
};
