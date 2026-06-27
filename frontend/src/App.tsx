import { useState } from 'react';
import './App.css'
import { FamilyTreePage } from './components/FamilyTreePage';
import { RootAscendantPage } from './components/RootAscendant';
import { Header } from './components/Header';

function App() {
   const [currentView, setCurrentView] = useState<'tree' | 'root'>('tree');

    return (
        <div>
            <Header 
                onViewFamilyTree={() => setCurrentView('tree')} 
                onGetRootAscendant={() => setCurrentView('root')} 
            />
            <main>
                {currentView === 'tree' ? (<FamilyTreePage />) : (<RootAscendantPage />)}
            </main>
        </div>
    )
}

export default App
