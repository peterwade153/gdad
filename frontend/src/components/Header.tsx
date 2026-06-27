import React from 'react';

interface HeaderProps {
    onViewFamilyTree: () => void;
    onGetRootAscendant: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onViewFamilyTree, onGetRootAscendant }) => {
    return (
        <header className="bg-slate-900 text-white shadow-md border-b border-slate-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                
                <div className="flex-shrink-0 flex items-center gap-2">
                    <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-emerald-400 to-teal-500 bg-clip-text text-transparent">
                        Grand-Daddy Tree
                    </span>
                </div>
                <nav className="flex items-center gap-4">
                    <button
                    type="button"
                    onClick={onViewFamilyTree}
                    className="px-4 py-2 text-sm font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-600 transition-colors duration-200"
                    >
                        View Family Tree
                    </button>
                    
                    <button
                    type="button"
                    onClick={onGetRootAscendant}
                    className="px-4 py-2 text-sm font-medium rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm hover:shadow transition-all duration-200"
                    >
                        Root Ascendant
                    </button>
                </nav>

                </div>
            </div>
        </header>
    );
};
