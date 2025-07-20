import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import { DarkModeProvider } from './contexts/DarkModeContext';
import Header from './components/Header';
import ChatPage from './pages/ChatPage';
import VoicePage from './pages/VoicePage';
import SchedulePage from './pages/SchedulePage';
import KnowledgePage from './pages/KnowledgePage';
import AboutPage from './pages/AboutPage';

function App() {
    return (
        <DarkModeProvider>
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                <Header />
                <main className="container mx-auto px-4 py-8">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <Routes>
                            <Route path="/" element={<ChatPage />} />
                            <Route path="/voice" element={<VoicePage />} />
                            <Route path="/schedule" element={<SchedulePage />} />
                            <Route path="/knowledge" element={<KnowledgePage />} />
                            <Route path="/about" element={<AboutPage />} />
                        </Routes>
                    </motion.div>
                </main>
            </div>
        </DarkModeProvider>
    );
}

export default App; 