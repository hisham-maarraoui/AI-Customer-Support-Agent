import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Search, FileText } from 'lucide-react';

const KnowledgePage = () => {
    return (
        <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
                <motion.h1
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-3xl font-bold text-gray-900 mb-2"
                >
                    Knowledge Base
                </motion.h1>
                <motion.p
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-gray-600"
                >
                    Search through Apple's support documentation and knowledge base
                </motion.p>
            </div>

            <div className="card">
                <div className="text-center py-12">
                    <BookOpen size={64} className="mx-auto mb-4 text-gray-400" />
                    <h2 className="text-xl font-semibold text-gray-900 mb-2">
                        Knowledge Search Coming Soon
                    </h2>
                    <p className="text-gray-600 mb-6">
                        This feature will allow you to search through Apple's comprehensive support documentation, FAQs, and troubleshooting guides.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <Search size={16} />
                            <span>Advanced Search</span>
                        </div>
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <FileText size={16} />
                            <span>Documentation</span>
                        </div>
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                            <BookOpen size={16} />
                            <span>Knowledge Base</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default KnowledgePage; 